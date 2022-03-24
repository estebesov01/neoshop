from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import CartItem
from .serializers import CartItemDetailSerializer, CartItemListSerializer


class CartItemView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemDetailSerializer

    def list(self, request, *args, **kwargs):
        serializer = CartItemListSerializer(CartItem.objects.all(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cart_item = CartItemDetailSerializer(data=request.data)
        if cart_item.is_valid():
            cart_item.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(cart_item.errors, status=status.HTTP_400_BAD_REQUEST)
