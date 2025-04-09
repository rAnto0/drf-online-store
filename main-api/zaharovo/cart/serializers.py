from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from .models import CartItem, Cart
from .utils import get_cart_from_request


class CartItemSerializer(serializers.ModelSerializer):
    # Для создания товара в корзине, можно использовать только id продукта
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

    def validate(self, data):
        product = data.get('product')
        new_quantity = data.get('quantity', 1)
        request = self.context.get('request')

        cart = get_cart_from_request(request)

        # Пытаемся найти существующий элемент для данного продукта в корзине
        try:
            existing_item = cart.items.get(product=product)
            total_quantity = existing_item.quantity + new_quantity
        except CartItem.DoesNotExist:
            total_quantity = new_quantity

        if product and total_quantity > product.stock:
            raise serializers.ValidationError(f"Нельзя добавить {total_quantity} шт., доступно только {product.stock}.")
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'created_at', 'items']
        read_only_fields = ['user', 'session_key', 'created_at', 'items']