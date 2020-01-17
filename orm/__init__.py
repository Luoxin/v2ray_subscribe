from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import sessionmaker

from conf.conf import get_conf

_base = declarative_base()

_engine = create_engine(
    get_conf("DB_URL"),
    pool_pre_ping=True,
    pool_recycle=3600,
)


class Post(object):
        pass


class BaseModel(_base):
    """Base Class """

    id = Column(Integer, primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)

    @classmethod
    def __declare_last__(cls):
        cls.entries = db.relationship(_engine, viewonly=True)

    def attach_entries(self, entries):
        for entry in entries:
            self.entries.append(entry)
            entry.post = self
            db.session.add(entry)


from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

_base.metadata.create_all(_engine)
db = sessionmaker(bind=_engine)()
