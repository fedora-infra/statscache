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
        self.results = {}

    def __call__(self, *args, **kwargs):
        key = hash(str(args)) + hash(str(kwargs))
        if self.results.get(key) is None:
            self.results[key] = self.func(*args, **kwargs)
        return self.results[key]


@memoized
def load_plugins(frequency, config):
    plugins = []
    entry_points = pkg_resources.iter_entry_points('statscache.plugin')
    for entry_point in entry_points:
        try:
            module = entry_point.load()
            module_frequencies = getattr(module, 'FREQUENCIES')
            if module_frequencies is not None and \
                    frequency not in module_frequencies:
                continue
            model = module.make_model(frequency)
            plugin = module.Plugin(config, model)
            plugins.append(plugin)
        except Exception:
            log.exception("Failed to load plugin %r" % entry_point)

    return plugins


def get_model(idx, frequency, config):
    plugins = load_plugins(frequency, config)
    for plugin in reversed(plugins):
        if plugin.idx == idx:
            return plugin.model
    raise KeyError("No such model for %r %r" % (idx, frequency))
