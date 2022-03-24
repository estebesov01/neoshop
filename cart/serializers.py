from rest_framework import serializers

from shop.serializers import ProductDetailSerializer
from .models import CartItem


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ['user', 'id']


