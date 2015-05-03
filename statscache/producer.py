import datetime

import fedmsg.meta
import moksha.hub.api

import statscache.plugins
import statscache.schedule
import statscache.utils

import logging
log = logging.getLogger("fedmsg")


class StatsProducerBase(moksha.hub.api.PollingProducer):
    """ An abstract base class for our other producers. """
    def __init__(self, hub):
        self.name = type(self).__name__[:-len('Producer')]
        log.debug("%s initializing" % self.name)
        super(StatsProducerBase, self).__init__(hub)

        fedmsg.meta.make_processors(**self.hub.config)

        # Find and save the StatsConsumer instance already created by the hub.
        # We are going to re-use its backends and db session.
        self.sister = statscache.utils.find_stats_consumer(self.hub)

        self.plugins = statscache.utils.load_plugins(
            int(self.frequency), self.hub.config)

        uri = self.hub.config['statscache.sqlalchemy.uri']
        statscache.plugins.create_tables(uri)

        log.debug("%s initialized with %r plugins" % (
            self.name, len(self.plugins)))
        self.init_plugins()

    def init_plugins(self):
        for plugin in self.plugins:
            initialize = getattr(plugin, 'initialize')
            if initialize is None:
                continue
            plugin.initialize(self.make_session())
        session.commit()

    def make_session(self):
        uri = self.hub.config['statscache.sqlalchemy.uri']
        return statscache.plugins.init_model(uri)

    def poll(self):
        now = datetime.datetime.utcnow()

        bucket = self.sister.buckets[self.name]
        self.sister.buckets[self.name] = []

        n = len(bucket)
        log.info("%s called with %i items in the bucket." % (self.name, n))

        for plugin in self.plugins:
            log.info("  Calling %r" % plugin.name)
            session = self.make_session()
            try:
                plugin.handle(session, now, bucket)
                session.commit()
            except:
                log.exception('Error during plugin %r handling.' % plugin)
                session.rollback()


class OneSecondProducer(StatsProducerBase):
    frequency = statscache.schedule.Schedule(second=range(0, 60, 1))


class FiveSecondProducer(StatsProducerBase):
    frequency = statscache.schedule.Schedule(second=range(0, 60, 5))


class OneMinuteProducer(StatsProducerBase):
    frequency = statscache.schedule.Schedule(second=[0])


class OneDayProducer(StatsProducerBase):
    # Every night at midnight (UTC)
    frequency = statscache.schedule.Schedule(second=[0], minute=[0], hour=[0])
