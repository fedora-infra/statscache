import pkg_resources

import logging
log = logging.getLogger("fedmsg")


def find_stats_consumer(hub):
    for cons in hub.consumers:
        if 'StatsConsumer' in str(type(cons)):
            return cons

    raise ValueError('StatsConsumer not found.')


class memoized(object):
    def __init__(self, func):
        self.func = func
        self.result = None

    def __call__(self, *args, **kwargs):
        if self.result is None:
            self.result = self.func(*args, **kwargs)
        return self.result


@memoized
def load_plugins(frequency, config):
    plugins = []
    entry_points = pkg_resources.iter_entry_points('statscache.plugin')
    for entry_point in entry_points:
        try:
            module = entry_point.load()
            model = module.make_model(frequency)
            plugin = module.Plugin(config, model)
            plugins.append(plugin)
        except Exception:
            log.exception("Failed to load plugin %r" % entry_point)

    return plugins


def get_model(name, frequency, config):
    plugins = load_plugins(frequency, config)
    print len(plugins), "is the num plugins."
    for plugin in plugins:
        if plugin.name == name:
            return plugin.model
    raise KeyError("No such model for %r %r" % (name, frequency))
