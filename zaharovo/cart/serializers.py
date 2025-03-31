from rest_framework import serializers

from products.models import Product
from .models import CartItem, Cart
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    # Для создания товара в корзине, можно использовать только id продукта
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'created_at', 'items']
        read_only_fields = ['user', 'session_key', 'created_at', 'items']