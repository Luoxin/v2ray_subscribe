from datetime import date

from peewee import *

db = SqliteDatabase("people.db")


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db


# # 抓取的配置表
# class SubscribeCrawl(Base):
#     __tablename__ = "subscribe_crawl"  # 表的名字
#
#     # 定义各字段
#     id = Column(Integer, primary_key=True)  # id
#     created_at = Column(Integer, server_default=str(int(time.time())))  # 开始时间
#     updated_at = Column(
#         Integer, server_default=str(int(time.time())), onupdate=str(int(time.time()))
#     )  # 更新时间
#
#     url = Column(String, unique=True)  # 地址
#     type = Column(Integer)  # 类型
#     rule = Column(JSON)  # 规则
#     is_closed = Column(Boolean)  # 是否关闭
#     next_time = Column(Integer)  # 下一次的测速时间
#     interval = Column(Integer)  # 间隔
#
#     note = Column(String)  # 备注信息
#
# class SubscribeAuthentication(Base):
#     __tablename__ = "subscribe_authentication"  # 表的名字
#
#     # 定义各字段
#     id = Column(Integer, primary_key=True)  # id
#
#     secret_key = Column(String, unique=True)  # 秘钥
#
#     uuid = Column(String, unique=True)  # 秘钥
#
#     level = Column(Integer)  # 级别
#     rule = Column(JSON)  # 限制规则
#
#     note = Column(String)  # 备注信息
#
# @unique
# class SubscribeCrawlType(Enum):
#     Nil = 0
#     Subscription = 1
#     Xpath = 2
#
# @unique
# class SubscribeAuthenticationLevel(Enum):
#     Nil = 0
#     SuperAdmin = 1
#
# @unique
# class SubscribeLastVmssState(Enum):
#     Nil = 0  # 默认正常
#     SysError = 1  # 系统错误
#     TimeoutError = 2  # 超时
#     ConnectionError = 3  # 连接失败
#
# if DB_URL.startswith("sqlite"):
#     engine = create_engine(
#         DB_URL,
#         echo=SQLALCHEMY_DEBUG,
#         pool_pre_ping=True,
#         pool_recycle=3600,
#         # pool_size=10,
#         # pool_timeout=5
#     )
# else:
#     engine = create_engine(
#         DB_URL,
#         echo=SQLALCHEMY_DEBUG,
#         pool_pre_ping=True,
#         pool_recycle=3600,
#         # pool_size=10,
#         # pool_timeout=5
#     )
#
