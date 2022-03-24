from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Category, Product, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer, ProductDetailSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
    serializer_class = CommentSerializer
