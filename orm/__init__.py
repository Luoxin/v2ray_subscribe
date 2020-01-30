from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from enum import unique, Enum

from conf.conf import get_conf
import utils


base = declarative_base()

engine = create_engine(
    get_conf("DB_URL"),
    poolclass=QueuePool,
    pool_recycle=3600,
    pool_use_lifo=True,
    pool_pre_ping=True,
    max_overflow=-1,
)

# class BaseModel(_base):
#     """Base Class """
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     created = Column(DateTime, nullable=False)
#
#     @classmethod
#     def __declare_last__(cls):
#         cls.entries = db.relationship(_engine, viewonly=True)
#
#     def attach_entries(self, entries):
#         for entry in entries:
#             self.entries.append(entry)
#             entry.post = self
#             db.session.add(entry)


from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

base.metadata.create_all(engine)
db = sessionmaker(bind=engine)
