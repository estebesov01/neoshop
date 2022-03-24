from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderItemSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    def create(self, request, *args, **kwargs):
        order = OrderListSerializer(data=request.data)
        if order.is_valid():
            if CartItem.objects.filter(user=self.request.user).count() == 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            order.save(user=self.request.user)
            for item in CartItem.objects.filter(user=self.request.user):
                OrderItem.objects.create(order_id=order.instance.id,
                                         user_id=item.user_id,
                                         quantity=item.quantity,
                                         product_id=item.product_id
                                         )
            CartItem.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serializer = OrderListSerializer(Order.objects.all(), many=True)
        return Response(serializer.data)


class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
