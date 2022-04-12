# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Coupon
from .permissions import IsSupplierAndIsOwner
from .serializers import CouponSerializer


class CouponView(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser, ]
