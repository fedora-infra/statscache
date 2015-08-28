import abc
import datetime

from statscache.plugins.schedule import Schedule
from statscache.plugins.models import BaseModel, ScalarModel,\
									  CategorizedModel, CategorizedLogModel,\
									  ConstrainedCategorizedLogModel


class BasePlugin(object):
	""" An abstract base class for plugins """
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

    @abc.abstractmethod
    def process(self, message):
        """ Process a message """
        pass

    @abc.abstractmethod
    def update(self, session):
        """ Update the model using the database session """
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
