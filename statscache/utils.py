import inspect
import pkg_resources
import requests
import concurrent.futures
import time

from statscache.schedule import Schedule
import statscache.plugins

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
    def query(page):
        return session.get(endpoint, params={ 'page': page }).json()


    endpoint = 'https://apps.fedoraproject.org/datagrepper/raw/'
    session = requests.Session()
    session.params = {
        'start': time.mktime(start.timetuple()),
        'order': 'asc',
        'rows_per_page': quantum,
    }
    if stop is not None:
        session.params['end'] = time.mktime(stop.timetuple())

    response = query(1)
    pages = int(response['pages'])
    yield response['raw_messages']
    del response

    executor = concurrent.futures.ThreadPoolExecutor()
    for response in executor.map(query, xrange(2, pages+1)):
        yield response['raw_messages']
    executor.shutdown()


def init_plugins(config):
    """ Initialize all available plugins using the given configuration.

    Plugin classes and collections of plugin classes are searched for at all
    entry-points registered under statscache.plugin. A plugin class is defined
    to be a class that inherits from statscache.plugin.BasePlugin
    """
    def init_plugin(plugin_class):
        if issubclass(plugin_class, statscache.plugins.BasePlugin):
            interval = plugin_class.interval
            if interval not in schedules:
                schedules[interval] = Schedule(interval, epoch)
            plugins.append(plugin_class(schedules[interval], config))

    epoch = config['statscache.consumer.epoch']
    schedules = { None: None }  # reusable Schedule instances
    plugins = []
    for entry_point in pkg_resources.iter_entry_points('statscache.plugin'):
        try:
            entry_object = entry_point.load()
            # the entry-point object is either a plugin or a collection of them
            try:
                for entry_element in entry_object:
                    init_plugin(entry_element)
            except TypeError:
                init_plugin(entry_object)
        except Exception:
            log.exception("Failed to load plugin from %r" % entry_point)
    return plugins
