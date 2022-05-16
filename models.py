from enum import unique
from peewee import *

db = SqliteDatabase("betsy.db")


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(unique=True)
    email = CharField()
    city = CharField()
    country = CharField()
    ideal = BooleanField()
    visa = BooleanField()
    mastercard = BooleanField()
    americanexpress = BooleanField()
    paypal = BooleanField()


class Product(BaseModel):
    name = CharField()
    description = TextField()
    price = DecimalField(decimal_places=2, auto_round=True)
    in_stock = IntegerField()

    class Meta:
        constraints = [Check('price > 0')]


class UserProduct(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)


class Tag(BaseModel):
    label = CharField(unique=True)


class ProductTag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


# class Purchase(BaseModel):
#     buyer = ForeignKeyField(User)
#     product = ForeignKeyField(Product)
#     quantity = IntegerField()


def create_tables():
    with db:
        db.create_tables([User, Product, UserProduct,
                         Tag, ProductTag])
