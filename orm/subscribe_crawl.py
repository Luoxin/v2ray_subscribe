import time
from enum import unique, Enum

from orm import *


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

    class Meta:
        database = db
        db_name = "subscribe_vmss"

    def save(self, *args, **kwargs):
        """覆写save方法, update_time字段自动更新, 实例对象需要在update成功之后调用save()"""
        if self._get_pk_value() is None:
            # this is a create operation, set the date_created field
            self.created_at = time.time()

        self.updated_at = time.time()

        return super(SubscribeCrawl, self).save(*args, **kwargs)


@unique
class SubscribeCrawlType(Enum):
    Nil = 0
    Subscription = 1
    Xpath = 2
