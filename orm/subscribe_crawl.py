from peewee import *

class SubscribeCrawl(Model):
    """
       抓取的配置表
    """
    id = IntegerField()  # id
    created_at = Column(Integer, server_default=str(int(time.time())))  # 开始时间
    updated_at = Column(
        Integer, server_default=str(int(time.time())), onupdate=str(int(time.time()))
    )  # 更新时间

    url = Column(String, unique=True)  # 地址
    type = Column(Integer)  # 类型
    rule = Column(JSON)  # 规则
    is_closed = Column(Boolean)  # 是否关闭
    next_time = Column(Integer)  # 下一次的测速时间
    interval = Column(Integer)  # 间隔

    note = Column(String)  # 备注信息