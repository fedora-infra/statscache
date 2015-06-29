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


class memoized(object):
    def __init__(self, func):
        self.func = func
        self.results = {}

    def __call__(self, *args, **kwargs):
        key = hash(str(args)) + hash(str(kwargs))
        if self.results.get(key) is None:
            self.results[key] = self.func(*args, **kwargs)
        return self.results[key]


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


@memoized
def init_plugins(config):
    """ Return a mapping of plugin identifiers to initialized plugins """
    plugins = {}
    for plugin_class in plugin_classes:
        try:
            plugin = plugin_class(config)
            plugins[plugin.idx] = plugin
            log.info("Initialized plugin %r" % plugin.idx)
        except Exception:
            log.exception("Failed to initialize plugin %r" % plugin_class)
    return plugins


def get_plugin(idx, config):
    plugins = init_plugins(config)
    return plugins.get(idx)


def get_model(idx, config):
    plugin = get_plugin(idx, config)
    if plugin:
        return plugin.model
    raise KeyError("No such model for %r" % (idx))
