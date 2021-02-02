from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from accounts.serializers import UserSerializer
from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(WritableNestedModelSerializer):
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(required=False)

    class Meta:
        model = Product
        fields = '__all__'
