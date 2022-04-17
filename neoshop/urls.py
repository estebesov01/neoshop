from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.contrib import admin
from cart.views import CartItemView
from orders.views import OrderView, OrderItemView
from shop.views import CategoryView, ProductView, CommentView
from coupon.views import CouponView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'category', CategoryView)
router.register(r'product', ProductView)
router.register(r'cartitem', CartItemView)
router.register(r'order', OrderView)
router.register(r'order_item', OrderItemView)
router.register(r'coupon', CouponView)
router.register(r'comment', CommentView)

# The API URLs are now determined automatically by the router.

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('user/', include('djoser.urls'), name='user'),
    path('auth/', include('rest_framework.urls'), name='auth'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
