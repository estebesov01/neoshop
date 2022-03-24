# Create your views here.
from rest_framework import viewsets

from .models import Coupon
from .serializers import CouponSerializer


class CouponView(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
