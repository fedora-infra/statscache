import inspect
import pkg_resources
import requests
import concurrent.futures
import time

from statscache.plugins import BasePlugin, Schedule
import statscache.plugins.models as models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import logging
log = logging.getLogger("fedmsg")


def find_stats_consumer(hub):
    """ Find the caching StatsConsumer associated with the given hub """
    for cons in hub.consumers:
        if 'StatsConsumer' in str(type(cons)):
            return cons

    raise ValueError('StatsConsumer not found.')


def datagrep(start, stop, workers=1, profile=False, quantum=100):
    """ Yield messages generated in the given time interval from datagrepper

    Messages are ordered ascending by age (from oldest to newest), so that
    models may be kept up-to-date through some point, to allow restart in case
    of failure. Messages are generated in collections of the given quantum at a
    time.
    """
    endpoint = 'https://apps.fedoraproject.org/datagrepper/raw/'
    session = requests.Session()
    session.params = {
        'start': time.mktime(start.timetuple()),
        'order': 'asc',
        'rows_per_page': quantum,
    }
    if stop is not None:
        session.params['end'] = time.mktime(stop.timetuple())
    query = lambda page: session.get(endpoint, params={ 'page': page })

    # Manually perform the first request in order to get the page count and
    # (hopefully) spawn some persistent connections prior to entering the
    # executor map.
    data = query(1).json()
    yield data['raw_messages']
    pages = int(data['pages'])
    del data

    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        # Uncomment the lines of code in this block to log profiling data
        page = 1
        net_time = time.time()
        for response in executor.map(query, xrange(2, pages+1)):
            if profile:
                net_time = time.time() - net_time
                cpu_time = time.time()
            yield response.json()['raw_messages']
            if profile:
                page += 1
                cpu_time = time.time() - cpu_time
                log.info("Processed page {}/{}: {}ms NET {}ms CPU".format(
                    page,
                    pages,
                    int(net_time * 1000),
                    int(cpu_time * 1000)
                ))
                net_time = time.time()


def init_plugins(config):
    """ Initialize all available plugins using the given configuration.

    Plugin classes and collections of plugin classes are searched for at all
    entry-points registered under statscache.plugin. A plugin class is defined
    to be a class that inherits from statscache.plugin.BasePlugin
    """
    def init_plugin(plugin_class):
        if issubclass(plugin_class, BasePlugin):
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


def init_model(db_url):
    engine = create_engine(db_url)

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


def create_tables(db_url):
    engine = create_engine(db_url, echo=True)
    models.ScalarModel.metadata.create_all(engine)
    models.CategorizedModel.metadata.create_all(engine)
    models.CategorizedLogModel.metadata.create_all(engine)
    models.ConstrainedCategorizedLogModel.metadata.create_all(engine)
    models.BaseModel.metadata.create_all(engine)
