import datetime
from collections import defaultdict

import fedmsg.meta
import moksha.hub.api

import statscache.plugins
import statscache.frequency
import statscache.utils

import logging
log = logging.getLogger("fedmsg")


class StatsProducerBase(moksha.hub.api.PollingProducer):
    """
    An abstract base class for dynamically generated producers. Subclasses need
    only define 'frequency' and 'plugin_classes' attributes as well as define a
    unique class name for themselves.
    """
    def __init__(self, hub):
        log.debug("%s initializing" % type(self).__name__)
        super(StatsProducerBase, self).__init__(hub)

        fedmsg.meta.make_processors(**self.hub.config)

        # set up the cache and connect to the consumer
        self.cache = []
        statscache.utils.find_stats_consumer(self.hub).register(self)

        log.debug("%s initialized with %r plugins" % (
            type(self).__name__, len(self.plugin_classes)))

        # Loop over all our plugins twice, pausing in the middle to create
        # their db tables if necessary.
        self.plugins = []
        for plugin_class in self.plugin_classes:
            plugin = plugin_class(self.frequency, self.hub.config)
            self.plugins.append(plugin)
            log.info("Instantiated plugin %r" % plugin.ident)

        # Create any absent db tables (were new plugins installed?)
        uri = self.hub.config['statscache.sqlalchemy.uri']
        statscache.plugins.create_tables(uri)

        # Finally, call the initialize method of any plugins that have one.
        # This typically makes long queries to datagrepper for historical
        # information.
        session = self.make_session()
        for plugin in self.plugins:
            try:
                initialize = getattr(plugin, 'initialize', None)
                if initialize is not None:
                    plugin.initialize(session)
                    session.commit()
                log.info("Initialized plugin %r" % plugin.ident)
            except Exception:
                log.exception("Failed to initialize plugin %r" % plugin)
                # TODO -- if the plugin fails to initialize we should remove it
                # from `self.plugins`.
                session.rollback()

    def make_session(self):
        """ Initiate database connection """
        uri = self.hub.config['statscache.sqlalchemy.uri']
        return statscache.plugins.init_model(uri)

    def buffer(self, message):
        self.cache.append(message)

    def poll(self):
        """
        Empty the cache and distribute the contents to each plugin for
        processing.
        """
        cache = self.cache
        self.cache = []

        n = len(cache)
        log.info("%s called with %i cached items." % (type(self).__name__, n))

        for plugin in self.plugins:
            log.info("  Calling %r" % plugin.ident)
            session = self.make_session()
            try:
                plugin.handle(session, cache)
                session.commit()
            except:
                log.exception('Error during plugin %r handling.' % plugin)
                session.rollback()


def factory():
    """
    Producer class factory based on the frequencies of the available plugin
    classes.
    """
    plugins_by_interval = defaultdict(list)
    for plugin_class in statscache.utils.plugin_classes:
        interval = plugin_class.interval
        if isinstance(interval, datetime.timedelta):
            plugins_by_interval[interval].append(plugin_class)

    for interval, plugin_classes in plugins_by_interval.items():
        class StatsProducerAnon(StatsProducerBase):
            """ Dynamically generated class for a specific frequency """
            pass # we need to programmatically set class attributes
        frequency = statscache.frequency.Frequency(interval)
        StatsProducerAnon.frequency = frequency
        StatsProducerAnon.plugin_classes = plugin_classes
        StatsProducerAnon.__name__ = 'StatsProducer' + str(frequency)
        yield StatsProducerAnon
    return

producers = factory()
