from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True, index = True)
    username = fields.CharField(max_length=255, null = False)
    email = fields.CharField(max_length=255, unique = True, null = False)
    password = fields.CharField(max_length=255, null = True)
    is_verified = fields.BooleanField(default=False)
    joined_date = fields.DatetimeField(default = datetime.utcnow)


class Business(Model):
    id = fields.IntField(pk=True, index = True)
    business_name = fields.CharField(max_length=255, null = False)
    city = fields.CharField(max_length=255, null = True)
    region = fields.CharField(max_length=255, null = True)
    business_desc = fields.TextField(null = True)
    logo = fields.CharField(max_length=255, null = True)
    owner = fields.ForeignKeyField("models.User", related_name="business")


class Product(Model):
    id = fields.IntField(pk=True, index = True)
    name = fields.CharField(max_length=255, null = False, index = True)
    category = fields.CharField(max_length=255, null = False)
    price = fields.DecimalField(max_digits=10, decimal_places=2, null = False)
    product_image = fields.CharField(max_length=255, null = False)
    business = fields.ForeignKeyField("models.Business", related_name="products")


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", ))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password", ))


business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydanticIn = pydantic_model_creator(Business, name="BusinessIn", exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="Product", exclude=("Id", ))
