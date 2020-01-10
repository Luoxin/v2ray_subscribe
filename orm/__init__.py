from datetime import date

from peewee import *

db = SqliteDatabase("people.db")


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
