from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from cart.models import CartItem
from .models import Order, OrderItem
from .permissions import IsOwner
from .serializers import OrderListSerializer, OrderItemSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


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
        if request.user.is_staff:
            serializer = OrderListSerializer(Order.objects.all(), many=True)

            return Response(serializer.data)
        else:
            serializer = OrderListSerializer(Order.objects.filter(user=request.user), many=True)
            return Response(serializer.data)


class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = OrderItemSerializer(OrderItem.objects.all(), many=True)
            return Response(serializer.data)
        else:
            serializer = OrderItemSerializer(OrderItem.objects.filter(user=request.user), many=True)
            return Response(serializer.data)
