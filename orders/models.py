from decimal import Decimal
from users.models import CustomUser
from django.db import models

from shop.models import Product


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        if self.product.discount:
            self.total_price = Decimal(self.quantity) * self.product.price - (
                        Decimal(self.quantity) * self.product.price) * (Decimal(self.product.discount) / 100)
        else:
            self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name
