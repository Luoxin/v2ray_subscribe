# https://www.jianshu.com/p/84e667320ab3
from datetime import date
from playhouse.shortcuts import model_to_dict, dict_to_model
import traceback

from peewee import *

db = SqliteDatabase("people.db")


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db


class Pet(Model):
    owner = ForeignKeyField(Person, backref="pets")
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Pet])

# # insert
# uncle_bob = Person(name="Bob1", birthday=date(1960, 1, 15))
# uncle_bob.save()  # bob is now stored in the database
#
# # insert
# Person.create(name="Bob", birthday=date(1960, 1, 15))
#
# # insert
# person = Person.insert(name="Bob", birthday=date(1960, 1, 15)).execute()
#
# # select
# grandma = Person.select().where(Person.name == "Bob").get()
# print(grandma)
#
# # select
# grandma = Person.get(Person.name == "Bob")
# print(grandma)
#
# # select
query = Person.select().where(Person.name == "Bob").order_by(Person.name)
for person in query:
    print(person.name, person.birthday)

# # 把数据对象转成字典
# user = Person.create(name="jack")
# u = model_to_dict(user)
# print(u)


# try:
#     data = Person.select().where(Person.name == "Bob").get()
# except DoesNotExist:
#     print("捕获成功")
# except:
#     traceback.print_exc()
