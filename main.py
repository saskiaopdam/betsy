import models
from peewee import *

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


User = models.User
Product = models.Product
UserProduct = models.UserProduct
Tag = models.Tag
ProductTag = models.ProductTag
Transaction = models.Transaction


# QUERIES - optional and required


# optional
def list_users():

    users = User.select()

    # for user in users:
    #     # print(user.__dict__)
    #     print(user.__dict__['__data__'].items())

    #     dict = user.__dict__['__data__']

    #     for key, value in dict.items():
    #         print(key, value)

    print(f'Users:')
    for user in users:
        print(f'- user id: {user.id}, username: "{user.username}", first name: "{user.firstname}", last name: "{user.lastname}", shipping address: "{user.shipping_address}", billing address: "{user.billing_address}"')


# optional
def list_products():

    products = Product.select()
    print(f'Products:')
    for product in products:
        print(
            f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}')


# required
def list_user_products(username):
    user = User.get(User.username == username)

    products = (Product
                .select()
                .join(UserProduct)
                .join(User)
                .where(User.username == username))

    print(f'{username} owns the following products:')

    for product in products:
        available = UserProduct.get((UserProduct.user_id == user.id) & (
            UserProduct.product_id == product.id)).available

        print(
            f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}, available: {available}')


# optional
def list_tags():

    tags = Tag.select()
    print(f'Tags:')
    for tag in tags:
        print(f'- tag id: {tag.id}, name: "{tag.name}"')


# required
def list_products_per_tag(tagname):

    products = (Product
                .select()
                .join(ProductTag)
                .join(Tag)
                .where(Tag.name == tagname))

    print(f'Products tagged "{tagname}":')

    for product in products:
        """
        sellers: 

        After a transaction, multiple users can become the owners of the same product, and have different quantities of it on stock.

        When filtering the products on tag the user will want to know who the seller or sellers are.
        """
        sellers = (User
                   .select()
                   .join(UserProduct)
                   .where(UserProduct.product_id == product.id)
                   )
        seller_names = [seller.username for seller in sellers]

        print(
            f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}, sellers: {seller_names}')


# optional
def list_transactions():

    transactions = Transaction.select()
    print(f'Transaction:')
    for transaction in transactions:
        product = Product.get(Product.id == transaction.product)
        buyer = User.get(User.id == transaction.buyer)
        seller = User.get(User.id == transaction.seller)

        print(f'- transaction id: {transaction.id}, product: "{product.name}", buyer: "{buyer.username}", seller: "{seller.username}", quantity: {transaction.quantity}, date: {transaction.date}')


# required
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
        print(
            f'- product id: {product.id}, name: "{product.name}", description: "{product.description}", price: \u20ac{product.price}')


# required
def add_product_to_catalog(username, product_name, available):
    # when? if user x starts offering a product for sale
    user_id = User.get(User.username == username).id
    product_id = Product.get(Product.name == product_name).id

    try:
        already_listed = UserProduct.get((UserProduct.user_id == user_id) & (
            UserProduct.product_id == product_id))
        print(f'"{product_name}" is already listed')
    except DoesNotExist:
        try:
            UserProduct.create(user=user_id, product=product_id,
                               available=available)
            print(f'Success: "{product_name}" added to catalog.')
        except:
            print(f'Error: "{product_name}" not added to catalog.')


# required
def remove_product_from_catalog(username, product_name):
    # when? if user x stops offering a product for sale
    user_id = User.get(User.username == username).id
    product_id = Product.get(Product.name == product_name).id
    try:
        userproduct = UserProduct.get((UserProduct.user_id == user_id) & (
            UserProduct.product_id == product_id))
        userproduct.delete_instance()
        print(f'Success: {product_name} removed from catalog.')
    except:
        print(f'Error: {product_name} not removed from catalog.')


# required
def update_stock(username, product_name, new_quantity):
    # when? when a user changes stock on his/her own account
    user_id = User.get(User.username == username).id
    product_id = Product.get(Product.name == product_name).id
    try:
        userproduct = UserProduct.get((UserProduct.user_id == user_id) & (
            UserProduct.product_id == product_id))
        userproduct.available = new_quantity
        userproduct.save()
        print(f'Stock has been updated.')
    except:
        print(f'Stock could not be updated.')


# helper for purchase()
def decrement_seller_stock(username, product_name, quantity):
    # when? when a user sells a product
    user_id = User.get(User.username == username).id
    product_id = Product.get(Product.name == product_name).id
    try:
        userproduct = UserProduct.get((UserProduct.user_id == user_id) & (
            UserProduct.product_id == product_id))
        userproduct.available -= quantity
        userproduct.save()
        print(f'Seller stock has been decremented.')
    except:
        print(f'Seller stock could not be decremented.')


# helper for purchase()
def increment_buyer_stock(username, product_name, quantity):
    # when? when a user buyes a product
    user_id = User.get(User.username == username).id
    product_id = Product.get(Product.name == product_name).id

    try:
        userproduct = UserProduct.get((UserProduct.user_id == user_id) & (
            UserProduct.product_id == product_id))
        userproduct.available += quantity
        userproduct.save()
        print(f'Buyer stock has been incremented.')

    except DoesNotExist:
        add_product_to_catalog(username, product_name, quantity)


# required
def purchase(product_name, buyer_username, seller_username, quantity, date):

    product = Product.get(Product.name == product_name)
    buyer = User.get(User.username == buyer_username)
    seller = User.get(User.username == seller_username)

    def checkout():
        # register the transaction
        Transaction.create(product=product.id, buyer=buyer.id,
                           seller=seller.id, quantity=quantity, date=date)

        # update quantity owned by seller
        decrement_seller_stock(seller_username, product_name, quantity)

        # check if product listed with buyer
        increment_buyer_stock(buyer_username, product_name, quantity)

    def admit_for_checkout():
        try:
            # check if seller owns this product and has enough on stock
            available = UserProduct.get((UserProduct.user_id == seller.id) & (
                UserProduct.product_id == product.id)).available
            ordered = quantity

            enough_on_stock = available >= ordered
            if enough_on_stock:
                print("proceed to checkout")
                checkout()
            else:
                print(f'{seller.username} does not have enough on stock')

        except DoesNotExist:
            print(f'{seller.username} does not own {product.name}')

    admit_for_checkout()
