from enum import unique, Enum

from orm import *


class SubscribeCrawl(BaseModel):
    """
       抓取的配置表
    """
    __tablename__ = "subscribe_crawl"


    crawl_url = Column(String, max_length=1000, verbose_name="订阅地址/抓取源地址")

    crawl_type = IntegerField(verbose_name="抓取类型")
    rule = JSONField(verbose_name="抓取规则")
    is_closed = BooleanField(verbose_name="是否禁用")
    next_at = IntegerField(verbose_name="下一次的测速时间")
    interval = IntegerField(verbose_name="间隔")
    note = TextField(verbose_name="备注信息")

    class Meta:
        db_table = "subscribe_crawl"


@unique
class SubscribeCrawlType(Enum):
    Nil = 0
    Subscription = 1
    Xpath = 2
