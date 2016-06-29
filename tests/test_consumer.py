import mock
import os
import json
import unittest

from nose.tools import eq_

import fedmsg

from statscache.utils import datagrep

import statscache.consumer

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'fixtures.json')


class TestStatsConsumer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import fedmsg.config
        import fedmsg.meta

        cls.uri = "sqlite:////var/tmp/statscache-test.sqlite"

        config = fedmsg.config.load_config([], None)
        fedmsg.meta.make_processors(**config)
        config['statscache.sqlalchemy.uri'] = cls.uri
        cls.fedmsg_config = config

        with open(TESTDATA_FILENAME, 'r') as fobj:
            cls.fixtures = json.load(fobj)

    def setUp(self):
        class FakeHub(object):
            config = self.fedmsg_config

            def subscribe(*args, **kwargs):
                pass

        statscache.consumer.StatsConsumer._initialized = True
        self.consumer = statscache.consumer.StatsConsumer(FakeHub())

        self.session = statscache.utils.init_model(self.uri)

    @mock.patch('statscache.utils.datagrep', return_value=[])
    def test_plugins(self, func):
        self.fixtures = self.fixtures[0]
        for cnt, msg in enumerate(self.fixtures):
            self.consumer.consume(msg)

        eq_(self.session.Message.query.count(), 1)
