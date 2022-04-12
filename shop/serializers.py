from rest_framework import serializers

from .models import Category, Product, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['supplier']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'price', 'discount', 'available', 'supplier']


class FilterCommentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(replies=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    product = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ['rate', 'created', 'product', 'content', 'author', 'children']


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['rate', 'product', 'content', 'replies', 'user']
