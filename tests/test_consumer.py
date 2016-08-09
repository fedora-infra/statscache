import mock
import os
import json
import unittest

from nose.tools import eq_

import fedmsg

from statscache.utils import datagrep

import statscache.consumer


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

        cls.fixtures = {
            'username': 'apache',
            'i': 4,
            'timestamp': 1467814080,
            'msg_id': u'2016-55d13473-2e48-4b6e-9542-3bc1882152ef',
            'topic': u'org.release-monitoring.prod.anitya.distro.add',
            'msg': {
                'project': None,
                'message': {
                    'agent': 'foobar',
                    'distro': u'CentOS'
                },
                'distro': {
                    'name': 'CentOS'
                }
            }
        }

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
        msg = self.fixtures['msg']
        self.consumer.consume(msg)
        eq_(self.session.Message.query.count(), 1)

    def test_consume(self):
        """Test consume method of StatsConsumer."""
        for plugin in self.consumer.plugins:
            plugin.process = mock.Mock()

        msg = self.fixtures['msg']
        self.consumer.consume(msg)
        # Check that 'process' method of all plugins was called with the
        # same message.
        for plugin in self.consumer.plugins:
            plugin.process.assert_called_with(msg)
