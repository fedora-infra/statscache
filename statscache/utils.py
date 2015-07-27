import inspect
import pkg_resources

import statscache.plugins

import logging
log = logging.getLogger("fedmsg")


def find_stats_consumer(hub):
    """ Find the caching StatsConsumer associated with the given hub """
    for cons in hub.consumers:
        if 'StatsConsumer' in str(type(cons)):
            return cons

    raise ValueError('StatsConsumer not found.')


def load_plugins():
    """
    Return all plugin classes and collections of plugin classes registered as
    entry-points under statscache.plugin. A plugin class is defined to be a
    class that inherits from statscache.plugin.BasePlugin
    """
    def is_plugin_class(obj):
        return (inspect.isclass(obj) and
                issubclass(obj, statscache.plugins.BasePlugin))
    plugin_classes = []
    entry_points = pkg_resources.iter_entry_points('statscache.plugin')
    for entry_point in entry_points:
        try:
            # the entry-point is either a plugin or a collection of them
            entry_object = entry_point.load()
            try:
                for entry_elem in entry_object:
                    if is_plugin_class(entry_elem):
                        plugin_classes.append(entry_elem)
            except TypeError:
                if is_plugin_class(entry_object):
                    plugin_classes.append(entry_object)
        except Exception:
            log.exception("Failed to load plugin from %r" % entry_point)
    return plugin_classes


# load the available plugin classes once and save them
plugin_classes = load_plugins()
