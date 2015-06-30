import copy

import fedmsg.consumers

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
        log.debug("statscache consumer initialized")
        self.producers = []

    def consume(self, raw_msg):
        """ Receive a message and enqueue it onto each bucket """
        topic, msg = raw_msg['topic'], raw_msg['body']
        log.info("Got message %r", topic)
        for producer in self.producers:
            producer.buffer(copy.deepcopy(msg))

    def stop(self):
        log.info("Cleaning up StatsConsumer.")
        super(StatsConsumer, self).stop()
