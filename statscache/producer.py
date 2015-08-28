import datetime
from collections import defaultdict

import moksha.hub.api

import statscache.utils

import logging
log = logging.getLogger("fedmsg")


class StatsProducer(moksha.hub.api.PollingProducer):
    """
    This class periodically visits all the plugins to request that they update
    their database models.
    """

    def __init__(self, hub):
        log.debug("statscache producer initializing")
        self.frequency = hub.config['statscache.producer.frequency']
        super(StatsProducer, self).__init__(hub)

        # grab the list of plugins from the consumer
        self.plugins = statscache.utils.find_stats_consumer(self.hub).plugins

        log.debug("statscache producer initialized")

    def make_session(self):
        """ Initiate database connection """
        uri = self.hub.config['statscache.sqlalchemy.uri']
        return statscache.utils.init_model(uri)

    def poll(self):
        """ Commit the accumulated database updates of each plugin """
        session = self.make_session()
        for plugin in self.plugins:
            try:
                plugin.update(session)
                log.info("Updating model for %r" % plugin.ident)
            except:
                log.exception("Error during model update for %r" % plugin)
                session.rollback()
