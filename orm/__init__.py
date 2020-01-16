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


class BaseModel(Model):
    id = IntegerField(primary_key=True)  # id
    created_at = IntegerField(default=now(), verbose_name="创建时间")
    updated_at = IntegerField(default=now(), verbose_name="更新时间")

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        """覆写save方法, update_time字段自动更新, 实例对象需要在update成功之后调用save()"""
        if self.id is None or self.id == 0:
            # this is a create operation, set the date_created field
            self.created_at = now()

        self.updated_at = now()

        return super(BaseModel, self).save(*args, **kwargs)


from orm.subscribe_crawl import SubscribeCrawl
from orm.subscribe_vmss import SubscribeVmss

db.create_tables([SubscribeCrawl, SubscribeVmss])
