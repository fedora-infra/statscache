import abc
import time

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
    def to_csv(self, instances):
        return "\n".join([
            "%0.2f, %i" % (time.mktime(ins.timestamp.timetuple()), ins.scalar)
            for ins in instances
        ])


#BaseModel = declarative_base(cls=BaseModelClass)
ScalarModel = declarative_base(cls=ScalarModelClass)
#CategorizedModel = declarative_base(cls=ScalarModelClass)


def init_model(db_url):
    engine = create_engine(db_url)

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


def create_tables(db_url):
    engine = create_engine(db_url, echo=True)
    #BaseModel.metadata.create_all(engine)
    ScalarModel.metadata.create_all(engine)


class BasePlugin(object):
    __meta__ = abc.ABCMeta

    name = None
    summary = None
    description = None

    def __init__(self, config, model):
        self.config = config
        self.model = model

        required = ['name', 'summary', 'description']
        for attr in required:
            if not getattr(self, attr):
                raise ValueError("%r must define %r" % (self, attr))

    @abc.abstractmethod
    def handle(session, timestamp, messages):
        pass
