from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response

from .models import Category, Product, Comment
from .permissions import IsSupplierOrReadOnly, IsOwnerOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer, ProductDetailSerializer, \
    CommentListSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSupplierOrReadOnly, ]
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSupplierOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        serializer = ProductDetailSerializer(Product.objects.all(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product = ProductSerializer(data=request.data)
        if product.is_valid():
            product.save(supplier=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        serializer = CommentSerializer(Comment.objects.all(), many=True)
        return Response(serializer.data)


