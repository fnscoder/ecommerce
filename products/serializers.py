from rest_framework import serializers

from accounts.serializers import UserSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
