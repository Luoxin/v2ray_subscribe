from enum import Enum, unique

from sqlalchemy import Column, Integer, String, Boolean, JSON, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 连接数据库
from sqlalchemy.orm import sessionmaker

from conf.conf import LOG_DEBUG, DB_URL

# 基本类
Base = declarative_base()


# 连接的表
class SubscribeVmss(Base):
    __tablename__ = 'subscribe_vmss'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)  # id
    created_at = Column(Integer)  # 开始时间
    updated_at = Column(Integer)  # 更新时间

    url = Column(String, unique=True)  # 地址
    speed = Column(Float)  # 速度
    type = Column(String, index=True)  # 类型
    health_points = Column(Integer)  # 生命值
    next_time = Column(Integer)  # 下一次的测速时间
    interval = Column(Integer)  # 间隔

    crawl_id = Column(Integer)  # 关联的 SubscribeCrawl 的 id

    last_state = Column(Integer, default=0)  # 最后一次测试的状态


# 抓取的配置表
class SubscribeCrawl(Base):
    __tablename__ = 'subscribe_crawl'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)  # id
    created_at = Column(Integer)  # 开始时间
    updated_at = Column(Integer)  # 更新时间

    url = Column(String, unique=True)  # 地址
    type = Column(Integer)  # 类型
    rule = Column(JSON)  # 规则
    is_closed = Column(Boolean)  # 是否关闭
    next_time = Column(Integer)  # 下一次的测速时间
    interval = Column(Integer)  # 间隔

    note = Column(String)  # 备注信息


class SubscribeAuthentication(Base):
    __tablename__ = 'subscribe_authentication'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)  # id

    secret_key = Column(String, unique=True)  # 秘钥

    uuid = Column(String, unique=True)  # 秘钥

    level = Column(Integer)  # 级别
    rule = Column(JSON)  # 限制规则

    note = Column(String)  # 备注信息


@unique
class SubscribeCrawlType(Enum):
    Nil = 0
    Subscription = 1
    Xpath = 2


@unique
class SubscribeAuthenticationLevel(Enum):
    Nil = 0
    SuperAdmin = 1


@unique
class SubscribeLastVmssState(Enum):
    Nil = 0  # 默认正常
    SysError = 1  # 系统错误
    TimeoutError = 2  # 超时
    ConnectionError = 3  # 连接失败


engine = create_engine(DB_URL, echo=LOG_DEBUG,
                       client_encoding="utf8",
                       pool_pre_ping=True,
                       pool_recycle=3600)

# 创建表
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

# # new_data = SubscribeCrawl(url="aaa")
# get_data = session.query(SubscribeVmss).filter(SubscribeVmss.next_time < time.time()).first()

# print(session.query(SubscribeVmss).order_by(SubscribeVmss.speed.desc()).first())
# print(session.query(SubscribeVmss).filter(SubscribeVmss.health_points > 0).count())
