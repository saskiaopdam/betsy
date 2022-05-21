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
    # requirement: "quantity" fullfilled at UserProduct with "available"
    name = CharField()
    description = TextField()
    price = DecimalField(decimal_places=2, auto_round=True)

    class Meta:
        constraints = [Check('price > 0')]


class UserProduct(BaseModel):
    """
    available:
    After a transaction, multiple users can become the owners of the same product, and have different quantities of it on stock.
    """
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    available = IntegerField()


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class Transaction(BaseModel):
    product = ForeignKeyField(Product)
    buyer = ForeignKeyField(User)
    seller = ForeignKeyField(User)
    quantity = IntegerField()
    date = DateField(formats='%Y-%m-%d')
