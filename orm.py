from enum import Enum, unique

from sqlalchemy import Column, Integer, String, Boolean, JSON, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 连接数据库
from sqlalchemy.orm import sessionmaker

from conf.conf import LOG_DEBUG, DB_URL

engine = create_engine(DB_URL, echo=LOG_DEBUG,
                       client_encoding="utf8")

# 基本类
Base = declarative_base()


# 连接的表
class SubscribeVmss(Base):
    __tablename__ = 'subscribe_vmss'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)  # id
    url = Column(String, unique=True)  # 地址
    speed = Column(Integer)  # 速度
    type = Column(String, index=True)  # 类型
    health_points = Column(Integer)  # 生命值
    next_time = Column(Integer)  # 下一次的测速时间
    interval = Column(Integer)  # 间隔
    created_at = Column(Integer)  # 开始时间
    updated_at = Column(Integer)  # 更新时间


# 抓取的配置表
class SubscribeCrawl(Base):
    __tablename__ = 'subscribe_crawl'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)  # id
    url = Column(String, unique=True)  # 地址
    type = Column(Integer)  # 类型
    rule = Column(JSON)  # 规则
    is_closed = Column(Boolean)  # 是否关闭
    next_time = Column(Integer)  # 下一次的测速时间
    interval = Column(Integer)  # 间隔
    created_at = Column(Integer)  # 开始时间
    updated_at = Column(Integer)  # 更新时间


@unique
class SubscribeCrawlType(Enum):
    Nil = 0
    Subscription = 1
    Xpath = 2


# 创建表
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

# # new_data = SubscribeCrawl(url="aaa")
# get_data = session.query(SubscribeVmss).filter(SubscribeVmss.next_time < time.time()).first()

# print(session.query(SubscribeVmss).order_by(SubscribeVmss.speed.desc()).first())
# print(session.query(SubscribeVmss).filter(SubscribeVmss.health_points > 0).count())