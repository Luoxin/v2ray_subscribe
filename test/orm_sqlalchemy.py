from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

base = declarative_base()

engine = create_engine(
    # "sqlite:///subscribe.vdb?check_same_thread=false",
    "sqlite:///:memory:?check_same_thread=false",
    poolclass=QueuePool,
    pool_recycle=3600,
    pool_use_lifo=True,
    pool_pre_ping=True,
    max_overflow=-1,
)


class Person(base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    __mapper_args__ = {"concrete": True}


base.metadata.create_all(engine)
db = sessionmaker(bind=engine)()

db.add(Person(name="name"))
db.commit()

print(db.query(Person).all()[0].__dict__)
