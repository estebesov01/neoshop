from django.contrib.auth.models import User
from django.db import models

from coupon.models import Coupon
from shop.models import Product


class CartItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


