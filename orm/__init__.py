from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from enum import unique, Enum
import time
from conf import global_variable
import utils

base = declarative_base()

engine = create_engine(
            global_variable.get_conf_str("DB_URL", default="sqlite:///subscribe.vdb?check_same_thread=false"),
            poolclass=QueuePool,
            pool_recycle=3600,
            pool_use_lifo=True,
            pool_pre_ping=True,
            max_overflow=-1,
        )

from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

base.metadata.create_all(engine)

global_variable.init_db(engine)
