import models
from peewee import *

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


User = models.User
Product = models.Product
UserProduct = models.UserProduct
Tag = models.Tag
ProductTag = models.ProductTag
Purchase = models.Purchase


def search(term):

    product_name = fn.Lower(Product.name)
    product_description = fn.Lower(Product.description)
    search_term = fn.Lower(term)

    products = (
        Product.select()
        .where(product_name.contains(search_term) | product_description.contains(search_term))
    )

    return [product for product in products]


def list_user_products(user_id):

    products = (Product
                .select()
                .join(UserProduct)
                .join(User)
                .where(User.id == user_id))

    return [product for product in products]


def list_products_per_tag(tag_id):

    products = (Product
                .select()
                .join(ProductTag)
                .join(Tag)
                .where(Tag.id == tag_id))

    return [product for product in products]


# def add_product_to_catalog(user_id, product):
# changed parameter "product" into "product_id"
def add_product_to_catalog(user_id, product_id):
    UserProduct.create(user=user_id, product=product_id)


def update_stock(product_id, new_quantity):
    product = Product.get(Product.id == product_id)
    product.in_stock = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    Purchase.create(product=product_id, buyer=buyer_id, quantity=quantity)


def remove_product(product_id):
    products = (UserProduct
                .select()
                .where(UserProduct.product_id == product_id))
    for product in products:
        product.delete_instance()
