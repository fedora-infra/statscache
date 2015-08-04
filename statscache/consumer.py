import copy

import fedmsg.consumers
import statscache.utils

import logging
log = logging.getLogger("fedmsg")

class StatsConsumer(fedmsg.consumers.FedmsgConsumer):
    """
    This consumer class propagates copies of incoming messages to the producers
    to cache for later processing.
    """
    topic = '*'
    config_key = 'statscache.consumer.enabled'

    def __init__(self, *args, **kwargs):
        """ Instantiate the consumer and a default list of buckets """
        log.debug("statscache consumer initializing")
        super(StatsConsumer, self).__init__(*args, **kwargs)

        # Instantiate plugins
        self.plugins = statscache.utils.init_plugins(self.hub.config)
        log.info("instantiated plugins: " +
            ', '.join([plugin.ident for plugin in self.plugins])
        )

        # Create any absent db tables (were new plugins installed?)
        uri = self.hub.config['statscache.sqlalchemy.uri']
        statscache.plugins.create_tables(uri)

        # Prepare to process backlogged fedmsg traffic
        session = statscache.plugins.init_model(uri)

        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'initialize'):
                    plugin.initialize(session)
                log.info("Initialized plugin %r" % plugin.ident)
            except Exception as e:
                log.exception(
                    "Failed to initialize plugin %r: %s" % (plugin.ident, e)
                )
                session.rollback()

        log.debug("statscache consumer initialized")

    def consume(self, raw_msg):
        """ Receive a message and enqueue it onto each bucket """
        topic, msg = raw_msg['topic'], raw_msg['body']
        log.info("Got message %r", topic)
        for plugin in self.plugins:
            plugin.process(copy.deepcopy(msg))

    def stop(self):
        log.info("Cleaning up StatsConsumer.")
        super(StatsConsumer, self).stop()
