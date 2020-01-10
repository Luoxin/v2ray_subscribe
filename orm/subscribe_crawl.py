import time

from playhouse.sqlite_ext import *

# from playhouse.mysql_ext import *
# from playhouse.postgres_ext import *


class SubscribeCrawl(Model):
    """
       抓取的配置表
    """

    id = IntegerField(primary_key=True)  # id
    created_at = IntegerField(default=time.time(), verbose_name="创建时间")
    updated_at = IntegerField(default=time.time(), verbose_name="更新时间")

    crawl_url = CharField(max_length=1000, unique=True, verbose_name="订阅地址/抓取源地址")

    crawl_type = IntegerField(verbose_name="抓取类型")
    rule = JSONField(verbose_name="抓取规则")
    is_closed = BooleanField(verbose_name="是否禁用规则")
    next_time = IntegerField(verbose_name="下一次的测速时间")
    interval = IntegerField(verbose_name="间隔")
    note = TextField(verbose_name="备注信息")


# @unique
# class SubscribeCrawlType(Enum):
#     Nil = 0
#     Subscription = 1
#     Xpath = 2
