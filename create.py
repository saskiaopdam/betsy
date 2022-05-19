import models
from peewee import *

db = SqliteDatabase("betsy.db")

User = models.User
Product = models.Product
UserProduct = models.UserProduct
Tag = models.Tag
ProductTag = models.ProductTag
Purchase = models.Purchase

# db.connect()

# db.create_tables([User, Product, UserProduct,
#                   Tag, ProductTag, Purchase])


def create_tables():
    with db:
        db.create_tables([User, Product, UserProduct,
                         Tag, ProductTag, Purchase])


create_tables()

# create fake users
User.create(username="userA", firstname="firstnameA", lastname="lastnameA",
            shipping_address="shiptoA", billing_address="billtoA")
User.create(username="userB", firstname="firstnameB", lastname="lastnameB",
            shipping_address="shiptoB", billing_address="billtoB")
User.create(username="userC", firstname="firstnameC", lastname="lastnameC",
            shipping_address="shiptoC", billing_address="billtoC")


# create fake products
Product.create(name="raindrop earrings",
               description="hand painted enamel earrings", price=25.5, quantity=40)
Product.create(name="sunburst earrings",
               description="made with 100 % pure love", price=23.98, quantity=20)
Product.create(name="bridesmaid pajamas",
               description="look cute while remaining modest and comfy", price=50.68, quantity=10)
Product.create(name="women sleepwear pajama",
               description="100 % organic linen(not bleached or dyed fabric)", price=30.33, quantity=50)
Product.create(name="postcard Dog/sausage",
               description="size A6 postcard", price=15.5, quantity=100)
Product.create(name="painting zebra",
               description="pine white wash panel, hanging system included", price=75, quantity=100)
Product.create(name="coffee grinder - wall mounted",
               description="classic coffee grinder in pastel green", price=45, quantity=30)
Product.create(name="pink tea or coffee cups",
               description="coffee or teacups made of white clay finished with a white and pink glaze", price=13.5, quantity=20)
Product.create(name="royal albert",
               description="approx. 1970s Royal Albert demitasse cup & saucer", price=28.59, quantity=1)
Product.create(name="pablo picasso print",
               description="very large exhibition poster(20 years) Gallery Delaive Amsterdam - 1994", price=219, quantity=1)

# create fake user-products relations
UserProduct.create(user_id=1, product_id=1)
UserProduct.create(user_id=1, product_id=2)
UserProduct.create(user_id=1, product_id=3)
UserProduct.create(user_id=2, product_id=4)
UserProduct.create(user_id=2, product_id=5)
UserProduct.create(user_id=2, product_id=6)
UserProduct.create(user_id=3, product_id=7)
UserProduct.create(user_id=3, product_id=8)
UserProduct.create(user_id=3, product_id=9)
UserProduct.create(user_id=3, product_id=10)

# create tags
Tag.create(label="jewellery & accessories")
Tag.create(label="clothing & shoes")
Tag.create(label="home & living")
Tag.create(label="wedding & party")
Tag.create(label="toys & entertainment")
Tag.create(label="art & collectibles")
Tag.create(label="craft supplies & tools")
Tag.create(label="vintage")

# create fake products-tag relations
ProductTag.create(product_id=1, tag_id=1)
ProductTag.create(product_id=1, tag_id=4)
ProductTag.create(product_id=2, tag_id=1)
ProductTag.create(product_id=2, tag_id=4)
ProductTag.create(product_id=3, tag_id=2)
ProductTag.create(product_id=3, tag_id=4)
ProductTag.create(product_id=4, tag_id=2)
ProductTag.create(product_id=5, tag_id=6)
ProductTag.create(product_id=6, tag_id=3)
ProductTag.create(product_id=6, tag_id=6)
ProductTag.create(product_id=7, tag_id=3)
ProductTag.create(product_id=7, tag_id=8)
ProductTag.create(product_id=8, tag_id=3)
ProductTag.create(product_id=9, tag_id=3)
ProductTag.create(product_id=9, tag_id=8)
ProductTag.create(product_id=10, tag_id=3)
ProductTag.create(product_id=10, tag_id=6)
ProductTag.create(product_id=10, tag_id=8)
