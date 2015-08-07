import inspect
import pkg_resources
import requests
import time

from statscache.frequency import Frequency
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


def datagrep(start, stop, quantum=100):
    """ Yield messages generated in the given time interval from datagrepper

    Messages are ordered ascending by age (from oldest to newest), so that
    models may be kept up-to-date through some point, to allow restart in case
    of failure. Messages are generated in collections of the given quantum at a
    time.
    """
    endpoint = 'https://apps.fedoraproject.org/datagrepper/raw/'
    page = 0
    pages = 1
    arguments = {
        'start': time.mktime(start.timetuple()),
        'page': page,
        'order': 'asc',
        'rows_per_page': quantum,
    }
    if stop is not None:
        arguments['end'] = time.mktime(stop.timetuple()),
    while page < pages:
        page += 1
        arguments['page'] = page
        response = requests.get(endpoint, params=arguments).json()
        # Correct page count, which is always necessary on the first request
        # and possibly also when stop is None
        pages = response['pages']
        yield response['raw_messages']


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
                frequencies[interval] = Frequency(interval, epoch)
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
