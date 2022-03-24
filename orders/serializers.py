from django.utils import timezone
from rest_framework import serializers

from coupon.models import Coupon
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    order = serializers.IntegerField(source='order.id')

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'total_price']


class OrderListSerializer(serializers.ModelSerializer):
    coupon = serializers.CharField(allow_blank=True)
    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = ['id', 'coupon', 'total_price']

    def get_total_price(self, obj):
        total_price = 0
        now = timezone.now()
        coupon = Order.objects.get(id=obj.id).coupon
        try:
            is_coupon = Coupon.objects.get(code__exact=coupon,
                                           valid_from__lte=now,
                                           valid_to__gte=now,
                                           active=True
                                           )
        except:
            is_coupon = None
        for item in OrderItem.objects.filter(order=obj.id):
                total_price += item.total_price
        if is_coupon:
            total_price = total_price - total_price * (is_coupon.discount/100)
        return total_price
