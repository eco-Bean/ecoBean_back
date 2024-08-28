# store/models.py

from django.db import models
from users.models import users  # Assuming you have a Users model
# from .models import Product


class Product(models.Model):
    name = models.TextField()  # Product name
    price = models.IntegerField()  # Product price

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'product'


class User_Product_mapping(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)  # User who purchased the product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Purchased product

    def __str__(self):
        return f"{self.user.nickname} - {self.product.name}"
    class Meta:
        db_table = 'user_product_mapping'