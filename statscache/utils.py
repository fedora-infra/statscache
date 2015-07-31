import inspect
import pkg_resources

import statscache.plugins

import logging
log = logging.getLogger("fedmsg")


def paginate(queryset, page_num, page_len, url_format):
    """
    Generate data for rendering the current page.

    Args:
        queryset: A SQLAlchemy queryset encompassing all the data to
            be paginated (and nothing else).
        page_num: A positive integer specifying which page to generate.
        page_len: A positive integer specifying how many rows to render
            in each page.
        url_format: A format string with fields for the keys 'page_num'
            and 'page_len'.
    Returns:
        A tuple: (page_items, prev_link, next_link)
        where
            page_items: A list of items to be rendered in the
                current page.
            items_count: Number of remaining items to be paginated
                (including the current page).
            items_total: Total number of items being paginated.
            prev_link: A string for the link to previous page, if there
                is one, else, None.
            next_link: A string for the link to the next page, if there
                is one, else, None.
    """
    items_total = queryset.count()
    queryset = queryset.offset((page_num - 1) * page_len)
    items_count = queryset.count() # remaining items, that is
    page_items = queryset.limit(page_len).all()
    page_items_count = len(page_items)

    next_link = None if items_count - page_len <= 0 else \
                url_format.format(page_num=page_num + 1, page_len=page_len)
    prev_link = None if page_num == 1 else \
                url_format.format(page_num=page_num - 1, page_len=page_len)
    return (page_items, items_count, items_total, prev_link, next_link)


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
