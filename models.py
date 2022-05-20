from enum import unique
from peewee import *

db = SqliteDatabase("betsy.db")


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    firstname = CharField()
    lastname = CharField()
    shipping_address = CharField()
    billing_address = CharField()


class Product(BaseModel):
    name = CharField()
    description = TextField()
    price = DecimalField(decimal_places=2, auto_round=True)

    class Meta:
        constraints = [Check('price > 0')]


class UserProduct(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    available = IntegerField()


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class Purchase(BaseModel):
    product = ForeignKeyField(Product)
    buyer = ForeignKeyField(User)
    seller = ForeignKeyField(User)
    quantity = IntegerField()
    date = DateField()
