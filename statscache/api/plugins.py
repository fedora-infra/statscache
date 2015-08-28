import abc
import collections
import json
import time
import datetime
from functools import partial

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute


class BaseModelClass(object):
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime, nullable=False, index=True)

    @classmethod
    def columns(cls):
        """ Return list of column attribute names """
        return [attr for (attr, obj) in cls.__dict__.iteritems()
                                     if isinstance(obj, InstrumentedAttribute)]

    @classmethod
    def to_json(cls, instances):
        """ Default JSON serializer """
        def serialize(obj):
            serializable = [dict, list, str, int, float, bool, None.__class__]
            if True in map(partial(isinstance, obj), serializable):
                return obj
            elif isinstance(obj, datetime.datetime):
                return time.mktime(obj.timetuple())
            else:
                return str(obj)
        columns = filter(lambda col: col != 'id', cls.columns())
        return json.dumps([
            { col: serialize(getattr(ins, col)) for col in columns }
            for ins in instances
        ])

    @classmethod
    def to_csv(cls, instances):
        """ Default CSV serializer """
        def serialize(obj):
            if isinstance(obj, datetime.datetime):
                return str(time.mktime(obj.timetuple()))
            else:
                return str(obj)
        def concat(xs, ys):
            xs.extend(ys)
            return xs
        columns = filter(lambda col: col != 'id', cls.columns())
        columns.remove('timestamp')
        columns.sort()
        columns.insert(0, 'timestamp')
        return '\n'.join(concat(
            [','.join(columns)],
            [
                ','.join([
                    serialize(getattr(ins, col))
                    for col in columns
                ])
                for ins in instances
            ]
        ))


class ScalarModelClass(BaseModelClass):
    scalar = sa.Column(sa.Integer, nullable=False)


class CategorizedModelClass(BaseModelClass):
    category = sa.Column(sa.UnicodeText, nullable=False)
    scalar = sa.Column(sa.Integer, nullable=False)

    @classmethod
    def collate(cls, instances):
        categories = set([i.category for i in instances])

        results = collections.OrderedDict()
        for instance in instances:
            tstamp = time.mktime(instance.timestamp.timetuple())
            if tstamp not in results:
                results[tstamp] = collections.OrderedDict(zip(
                    categories, [0] * len(categories)))
            results[tstamp][instance.category] = instance.scalar

        return results

    @classmethod
    def to_csv(cls, instances):
        results = cls.collate(instances)
        return "\n".join([
            "%0.2f, %s" % (tstamp, ", ".join(map(str, result.values())))
            for tstamp, result in results.items()
        ])


class CategorizedLogModelClass(BaseModelClass):
    category = sa.Column(sa.UnicodeText, nullable=False, index=True)
    message = sa.Column(sa.UnicodeText, nullable=False)


class ConstrainedCategorizedLogModelClass(CategorizedLogModelClass):
    category_constraint = sa.Column(sa.UnicodeText, nullable=True)


ScalarModel = declarative_base(cls=ScalarModelClass)
CategorizedModel = declarative_base(cls=CategorizedModelClass)
CategorizedLogModel = declarative_base(cls=CategorizedLogModelClass)
ConstrainedCategorizedLogModel = declarative_base(
    cls=ConstrainedCategorizedLogModelClass)
BaseModel = declarative_base(cls=BaseModelClass)


class BasePlugin(object):
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