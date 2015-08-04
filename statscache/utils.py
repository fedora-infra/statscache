import inspect
import pkg_resources

import statscache.plugins
from statscache.frequency import Frequency

import logging
log = logging.getLogger("fedmsg")


def find_stats_consumer(hub):
    """ Find the caching StatsConsumer associated with the given hub """
    for cons in hub.consumers:
        if 'StatsConsumer' in str(type(cons)):
            return cons

    raise ValueError('StatsConsumer not found.')


def init_plugins(config):
    """ Initialize all available plugins using the given configuration.

    Plugin classes and collections of plugin classes are searched for at all
    entry-points registered under statscache.plugin. A plugin class is defined
    to be a class that inherits from statscache.plugin.BasePlugin
    """
    def init_plugin(plugin_class):
        if issubclass(plugin_class, statscache.plugins.BasePlugin):
            interval = plugin_class.interval
            if interval not in frequencies:
                frequencies[interval] = Frequency(interval, epoch=epoch)
            plugins.append(plugin_class(frequencies[interval], config))

    epoch = config['statscache.consumer.epoch']
    frequencies = { None: None }  # reusable Frequency instances
    plugins = []
    for entry_point in pkg_resources.iter_entry_points('statscache.plugin'):
        try:
            entry_object = entry_point.load()
            # the entry-point object is either a plugin or a collection of them
            try:
                map(init_plugin, entry_object)
            except TypeError:
                init_plugin(entry_object)
        except Exception:
            log.exception("Failed to load plugin from %r" % entry_point)
    return plugins
