import abc
import datetime
from multiprocessing import cpu_count

from statscache.plugins.schedule import Schedule
from statscache.plugins.models import BaseModel, ScalarModel,\
                                      CategorizedModel, CategorizedLogModel,\
                                      ConstrainedCategorizedLogModel
from statscache.plugins.threads import Queue, Future, asynchronous


class BasePlugin(object):
    """ An abstract base class for plugins

    At a minimum, the class attributes 'name', 'summary', and 'description'
    must be defined, and in most cases 'model' must also. The class attributes
    'interval' and 'backlog_delta' are optional but may be extremely useful to
    plugins.

    The 'interval' attribute may be a 'datetime.timedelta' indicating what sort
    of time windows over which this plugin calculates statistics (e.g., daily
    or weekly). When the statscache framework initializes the plugin, it will
    attach an instance of 'statscache.plugins.Schedule' that is synchronized
    with the framework-wide statistics epoch (i.e., the exact moment as of
    which statistics are being computed) to the instance attribute 'schedule'.
    This prevents the possibility that the plugin's first time window will
    extend before the availability of data.

    The attribute 'backlog_delta' defines the maximum amount of backlog that
    may potentially be useful to a plugin. For instance, if a plugin is only
    interested in messages within some rolling window (e.g., all github or
    pagure messages received in the last seven days), *and* the plugin does not
    expose historical data, then it would be pointless for it to sift through a
    month's worth of data, when only the last seven days' worth would have
    sufficed.
    """
    __meta__ = abc.ABCMeta

    name = None
    summary = None
    description = None

    interval = None # this must be either None or a datetime.timedelta instance
    backlog_delta = None # how far back to process backlog (None is unlimited)
    model = None

    def __init__(self, schedule, config, model=None):
        self.schedule = schedule
        self.config = config
        self.launched = False
        if model:
            self.model = model

        required = ['name', 'summary', 'description']
        for attr in required:
            if not getattr(self, attr):
                raise ValueError("%r must define %r" % (self, attr))

    @property
    def ident(self):
        """
        Stringify this plugin's name to use as a (hopefully) unique identifier
        """
        ident = self.name.lower().replace(" ", "-")

        bad = ['"', "'", '(', ')', '*', '&', '?', ',']
        replacements = dict(zip(bad, [''] * len(bad)))
        for a, b in replacements.items():
            ident = ident.replace(a, b)
        schedule = getattr(self, 'schedule', None)
        if schedule:
            ident += '-{}'.format(schedule)
        return ident

    def launch(self, session):
        """ Launch asynchronous workers, restoring state from model if needed

        This method is not guaranteed to be called before message processing
        begins. Currently, it is invoked after backprocessing has completed.
        The recommended usage pattern is to launch a fixed number of worker
        threads, using the plugin thread API
        """
        self.launched = True

    @abc.abstractmethod
    def process(self, message):
        """ Process a single message, synchronously """
        pass

    @abc.abstractmethod
    def update(self, session):
        """ Update the database model, synchronously """
        pass

    def latest(self, session):
        """ Get the datetime to which the model is up-to-date """
        times = [
            # This is the _actual_ latest datetime
            getattr(session.query(self.model)\
                    .order_by(self.model.timestamp.desc())\
                    .first(), 
                    'timestamp',
                    None)
        ]
        if self.backlog_delta is not None:
            # This will limit how far back to process data, if statscache has
            # been down for longer than self.backlog_delta.
            times.append(datetime.datetime.now() - self.backlog_delta)
        return max(times) # choose the more recent datetime

    def revert(self, when, session):
        """ Revert the model change(s) made as of the given datetime """
        session.query(self.model).filter(self.model.timestamp >= when).delete()


class AsyncPlugin(BasePlugin):
    """ Abstract base class for plugins utilizing asynchronous workers """

    __meta__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(AsyncPlugin, self).__init__(*args, **kwargs)
        self.workers = cpu_count()
        self.queue = Queue(backlog=self.workers) # work queue

    def launch(self, session):
        def spawn(error):
            if error is not None:
                log.exception("error in {!r}: {!r}".format(self.ident, error))
            worker = self.queue.dequeue()
            worker.on_success(self.work)
            worker.on_failure(spawn)

        self.fill(session)

        for _ in xrange(self.workers):
            spawn(None)

        super(AsyncPlugin, self).launch(session)

    @abc.abstractmethod
    def work(self, item):
        """ Perform further processing on the model item, synchronously

        The mechanism for storage of the results of this processing for
        eventual commit by 'self.update()', is completely up to the individual
        plugin implementation. An easy way to manage this is by storing model
        instances on the queue, whose mere mutation will be reflected in the
        next database commit.

        Note that this method is called in its own thread, and may therefore
        utilize blocking I/O without disrupting any other components.
        """
        pass

    @abc.abstractmethod
    def fill(self, session):
        """ Fill the work queue 'self.queue' using the initial model state """
        pass
