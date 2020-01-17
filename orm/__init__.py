from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from conf.conf import get_conf


BaseModel = declarative_base()

_engine = create_engine(
        get_conf("DB_URL"),
        pool_pre_ping=True,
        pool_recycle=3600,
)


from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

BaseModel.metadata.create_all(_engine)
db = sessionmaker(bind=_engine)()

