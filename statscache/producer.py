import datetime

import fedmsg.meta
import moksha.hub.api

import statscache.plugins
import statscache.schedule
import statscache.utils

import logging
log = logging.getLogger("fedmsg")


class StatsProducerBase(moksha.hub.api.PollingProducer):
    """
    An abstract base class for our other producers. Creating a functional
    subclass requires co-ordinating a change in
    statscache.consumer.StatsConsumer to ensure that the appropriate bucket
    exists.
    """
    def __init__(self, hub):
        self.name = type(self).__name__[:-len('Producer')]
        log.debug("%s initializing" % self.name)
        super(StatsProducerBase, self).__init__(hub)

        fedmsg.meta.make_processors(**self.hub.config)

        # set up the cache and connect to the consumer
        self.cache = []
        statscache.utils.find_stats_consumer(self.hub).producers.append(self)

        self.plugins = statscache.utils.init_plugins(self.hub.config)

        uri = self.hub.config['statscache.sqlalchemy.uri']
        statscache.plugins.create_tables(uri)

        log.debug("%s initialized with %r plugins" % (
            self.name, len(self.plugins)))
        self.init_plugins()

    def init_plugins(self):
        """ Allow plugins to initialize themselves using the database """
        session = self.make_session()
        for plugin in self.plugins.values():
            initialize = getattr(plugin, 'initialize', None)
            if initialize is None:
                continue
            plugin.initialize(session)
        session.commit()

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
        timestamp = datetime.datetime.utcnow() # moment that the cache was cleared

        cache = self.cache
        self.cache = []

        n = len(cache)
        log.info("%s called with %i items in the cache." % (self.name, n))

        for plugin in self.plugins.values():
            log.info("  Calling %r" % plugin.name)
            session = self.make_session()
            try:
                plugin.handle(session, timestamp, cache)
                session.commit()
            except:
                log.exception('Error during plugin %r handling.' % plugin)
                session.rollback()


class OneSecondProducer(StatsProducerBase):
    frequency = statscache.plugins.Frequency(second=1)


class FiveSecondProducer(StatsProducerBase):
    frequency = statscache.plugins.Frequency(second=5)


class OneMinuteProducer(StatsProducerBase):
    frequency = statscache.plugins.Frequency(minutes=1)


class OneDayProducer(StatsProducerBase):
    # Every night at midnight (UTC)
    frequency = statscache.plugins.Frequency(days=1)
