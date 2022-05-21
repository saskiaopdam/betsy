from unicodedata import name
import models
from peewee import *

db = SqliteDatabase("betsy.db")

User = models.User
Product = models.Product
UserProduct = models.UserProduct
Tag = models.Tag
ProductTag = models.ProductTag
Transaction = models.Transaction


db.create_tables([User, Product, UserProduct,
                  Tag, ProductTag, Transaction])

# create some users
User.create(username="userA", firstname="firstnameA", lastname="lastnameA",
            shipping_address="shiptoA", billing_address="billtoA")
User.create(username="userB", firstname="firstnameB", lastname="lastnameB",
            shipping_address="shiptoB", billing_address="billtoB")
User.create(username="userC", firstname="firstnameC", lastname="lastnameC",
            shipping_address="shiptoC", billing_address="billtoC")


# create some products
Product.create(name="raindrop earrings",
               description="hand painted enamel earrings", price=25.5)
Product.create(name="sunburst earrings",
               description="made with 100 % pure love", price=23.98)
Product.create(name="bridesmaid pajamas",
               description="look cute while remaining modest and comfy", price=50.68)
Product.create(name="women sleepwear pajama",
               description="100 % organic linen(not bleached or dyed fabric)", price=30.33)
Product.create(name="postcard Dog/sausage",
               description="size A6 postcard", price=15.5)
Product.create(name="painting zebra",
               description="pine white wash panel, hanging system included", price=75)
Product.create(name="coffee grinder - wall mounted",
               description="classic coffee grinder in pastel green", price=45)
Product.create(name="pink tea or coffee cups",
               description="coffee or teacups made of white clay finished with a white and pink glaze", price=13.5)
Product.create(name="royal albert",
               description="approx. 1970s Royal Albert demitasse cup & saucer", price=28.59)
Product.create(name="pablo picasso print",
               description="very large exhibition poster (20 years) Gallery Delaive Amsterdam - 1994", price=219)

# create some user-products relations
UserProduct.create(user_id=1, product_id=1, available=50)
UserProduct.create(user_id=1, product_id=2, available=50)
UserProduct.create(user_id=1, product_id=3, available=50)
UserProduct.create(user_id=2, product_id=4, available=50)
UserProduct.create(user_id=2, product_id=5, available=100)
UserProduct.create(user_id=2, product_id=6, available=10)
UserProduct.create(user_id=3, product_id=7, available=1)
UserProduct.create(user_id=3, product_id=8, available=2)
UserProduct.create(user_id=3, product_id=9, available=1)
UserProduct.create(user_id=3, product_id=10, available=1)

# create tags
Tag.create(name="jewellery & accessories")
Tag.create(name="clothing & shoes")
Tag.create(name="home & living")
Tag.create(name="wedding & party")
Tag.create(name="toys & entertainment")
Tag.create(name="art & collectibles")
Tag.create(name="craft supplies & tools")
Tag.create(name="vintage")

# create some products-tag relations
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
