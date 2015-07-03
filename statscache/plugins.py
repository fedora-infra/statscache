import abc
import collections
import json
import time
import datetime

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class BaseModelClass(object):
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime, nullable=False, index=True)


class ScalarModelClass(BaseModelClass):
    scalar = sa.Column(sa.Integer, nullable=False)

    @classmethod
    def to_csv(cls, instances):
        return "\n".join([
            "%0.2f, %i" % (time.mktime(ins.timestamp.timetuple()), ins.scalar)
            for ins in instances
        ])


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

    @classmethod
    def to_csv(cls, instances):
        return "\n".join([
            "%0.2f, %s, %s" % (
                time.mktime(instance.timestamp.timetuple()),
                instance.category, instance.message)
            for instance in instances
        ])

    @classmethod
    def to_json(cls, instances):
        return json.dumps([
            {
                'timestamp': time.mktime(instance.timestamp.timetuple()),
                'category': instance.category,
                'message': instance.message
            } for instance in instances
        ])


class ConstrainedCategorizedLogModelClass(CategorizedLogModelClass):
    category_constraint = sa.Column(sa.UnicodeText, nullable=True)


ScalarModel = declarative_base(cls=ScalarModelClass)
CategorizedModel = declarative_base(cls=CategorizedModelClass)
CategorizedLogModel = declarative_base(cls=CategorizedLogModelClass)
ConstrainedCategorizedLogModel = declarative_base(
    cls=ConstrainedCategorizedLogModelClass)
BaseModel = declarative_base(cls=BaseModelClass)


def init_model(db_url):
    engine = create_engine(db_url)

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


def create_tables(db_url):
    engine = create_engine(db_url, echo=True)
    ScalarModel.metadata.create_all(engine)
    CategorizedModel.metadata.create_all(engine)
    CategorizedLogModel.metadata.create_all(engine)
    ConstrainedCategorizedLogModel.metadata.create_all(engine)
    BaseModel.metadata.create_all(engine)


class BasePlugin(object):
    __meta__ = abc.ABCMeta

    name = None
    summary = None
    description = None
    frequency = None # this can just be None

    datagrepper_endpoint = 'https://apps.fedoraproject.org/datagrepper/raw/'

    def __init__(self, config, model=None):
        self.config = config
        self.model = model or self.make_model()

        required = ['name', 'summary', 'description']
        for attr in required:
            if not getattr(self, attr):
                raise ValueError("%r must define %r" % (self, attr))
        if (not isinstance(self.frequency, Frequency) and
            self.frequency is not None):
            raise TypeError(("The 'frequency' attribute of %r must be an " +
                "an instance of %r if present") % (self, Frequency))

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
        frequency = getattr(self, 'frequency', None)
        if frequency:
            ident += '-{}'.format(frequency)
        return ident

    @abc.abstractmethod
    def handle(self, session, timestamp, messages):
        """ Process messages produced as of the given timestamp """
        pass


class Frequency(datetime.timedelta):
    """ timedelta extension with nicer printing """
    def __init__(self, days=0, hours=0, minutes=0, seconds=0):
        super(Frequency, self).__init__(days=days,
                                        seconds=(hours*60+minutes)*60+seconds)

    @property
    def hours(self):
        return self.seconds // (60*60)

    @property
    def minutes(self):
        return (self.seconds // 60) % 60

    @property
    def mod_seconds(self):
        return self.seconds % 60

    def __str__(self):
        # Pretty-print a timedelta in the format [[[#d]#h]#m]#s
        s = ''
        if self.days:
            s = str(days) + 'd'
        if self.hours:
            s = ''.join([s, str(self.hours), 'h'])
        if self.minutes:
            s = ''.join([s, str(self.minutes), 'm'])
        if self.mod_seconds or not s:
            s = ''.join([s, str(self.mod_seconds), 's'])
        return s

    def __repr__(self):
        kwargs = []
        for (kw, arg) in [('days', self.days),
                          ('hours', self.hours),
                          ('minutes', self.minutes),
                          ('seconds', self.mod_seconds)]:
            if arg:
                kwargs.append('='.join([kw, str(arg)]))
        return ''.join([self.__name__, '(', ','.join(kwargs), ')'])

    def __json__(self):
        return self.total_seconds()

    def __int__(self):
        return self.total_seconds()

    def __float__(self):
        return int(self) + self.microseconds / 1000
