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


def list_users():

    users = User.select()
    print(f'Users:')
    for user in users:
        print (f'- user id: {user.id}, username: "{user.username}", first name: "{user.firstname}", last name: "{user.lastname}", shipping address: "{user.shipping_address}", billing address: "{user.billing_address}"')


def list_products():

    products = Product.select()
    print(f'Products:')
    for product in products:
        print(f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}')


def list_user_products(username):
    user = User.get(User.username == username)
    
    products = (Product
                .select()
                .join(UserProduct)
                .join(User)
                .where(User.username == username))

    print(f'{username} owns the following products:')

    for product in products:
        available = UserProduct.get((UserProduct.user_id == user.id) & (UserProduct.product_id == product.id)).available

        print(f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}, available: {available}')


def list_tags():

    tags = Tag.select()
    print(f'Tags:')
    for tag in tags:
        print (f'- tag id: {tag.id}, name: "{tag.name}"')


def list_products_per_tag(tagname):

    products = (Product
                .select()
                .join(ProductTag)
                .join(Tag)
                .where(Tag.name == tagname))

    print(f'Products tagged "{tagname}":')

    for product in products:
        print(f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}')


# search for term in product name or product description
def search(term):

    product_name = fn.Lower(Product.name)
    product_description = fn.Lower(Product.description)
    search_term = fn.Lower(term)

    products = (
        Product.select()
        .where(product_name.contains(search_term) | product_description.contains(search_term))
    )

    print(f'The term "{term}" was found in the following products:')

    for product in products:
        print(f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}')


# TRANSACTION - purchase of a product


# if quantity of product owned by user changes
def update_stock(product_id, quantity):
    # in userproduct table
    # seller: quantity - sold amount
    # buyer: quantity + bought amount
    try:
        # product = Product.get(Product.id == product_id)
        # product.quantity = product
        # product.save()
        return True
    except:
        return False


# if seller runs out of the product
def remove_product_from_catalog(user_id, product_id):
    try:
        product = UserProduct.get((UserProduct.user_id == user_id) & (
                            UserProduct.product_id == product_id))
        product.delete_instance()
        print(f'Success: {product_id.name} removed from catalog.')
    except:
        print(f'Error: {product_id.name} not removed from catalog.')


# if buyer gets the product for the first time
def add_product_to_catalog(user_id, product_id, available):
    try:
        UserProduct.create(user=user_id, product=product_id, available=available)
        print(f'Success: {product_id.name} added to catalog.')
    except:
        print(f'Error: {product_id.name} not added to catalog.')


def purchase(product_id, buyer_id, seller_id, quantity, date):
    # register the transaction
    Purchase.create(product=product_id, buyer=buyer_id, seller=seller_id, quantity=quantity, date=date)

    # update quantity owned by seller
    update_stock()

    # update quantity owned by buyer
    update_stock()

    # if seller runs out of the product
    remove_product_from_catalog(seller_id, product_id)

    # if buyer gets the product for the first time
    add_product_to_catalog(buyer_id, product_id)
