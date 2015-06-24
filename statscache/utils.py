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


@memoized
def load_plugins(config):
    """
    Load all plugin modules registered as entry points under statscache.plugin,
    find all plugin classes contained directly under those modules, and return
    an instantiated copy of each one in a list.
    """
    plugins = {}
    entry_points = pkg_resources.iter_entry_points('statscache.plugin')
    for entry_point in entry_points:
        try:
            module = entry_point.load()
            for item in dir(module):
                attr = getattr(module, item, None)
                if not inspect.isclass(attr):
                    continue
                if issubclass(attr, statscache.plugins.BasePlugin):
                    plugin = attr(config)
                    plugins[plugin.idx] = plugin
        except Exception:
            log.exception("Failed to load plugin %r" % entry_point)

    return plugins


def get_plugin(idx, config):
    plugins = load_plugins(config)
    return plugins.get(idx)


def get_model(idx, config):
    plugin = get_plugin(idx, config)
    if plugin:
        return plugin.model
    raise KeyError("No such model for %r" % (idx))
