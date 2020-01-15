# db_url = get_conf("DB_URL")
from playhouse.db_url import connect

from urllib.parse import urlparse

from conf.conf import get_conf
from utils import now

url = get_conf("DB_URL")

scheme = urlparse(url).scheme
if "mysql" in scheme:
    from playhouse.mysql_ext import *
elif "postgres" in scheme:
    from playhouse.postgres_ext import *
elif "sqlite" in scheme:
    from playhouse.sqlite_ext import *
else:
    from peewee import *

db = connect(get_conf("DB_URL"))

from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

db.create_tables([SubscribeCrawl, SubscribeVmss])
