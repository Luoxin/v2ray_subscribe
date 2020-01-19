import utils
from orm import *


class SubscribeCrawl(base):
    __tablename__ = "subscribe_crawl"

    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, server_default=str(utils.now()))
    updated_at = Column(
        Integer, server_default=str(int(utils.now())), onupdate=str(int(utils.now()))
    )

    crawl_url = Column(String(1000), unique=True, comment="订阅地址/抓取源地址")

    crawl_type = Column(Integer, index=True, comment="抓取类型")
    rule = Column(JSON, comment="抓取规则")
    is_closed = Column(Boolean, comment="是否禁用")
    next_at = Column(Integer, comment="下一次的测速时间")
    interval = Column(Integer, comment="间隔")
    note = Column(Text, comment="备注信息")

    __table_args__ = {"comment": "抓取的配置表"}  # 添加索引和表注释


@unique
class SubscribeCrawlType(Enum):
    Nil = 0
    Subscription = 1
    Xpath = 2
