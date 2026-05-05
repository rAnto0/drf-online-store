from rest_framework import generics, permissions

from .models import CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import get_cart_from_request


class CartDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/cart/ – Получить корзину текущего пользователя
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return get_cart_from_request(self.request)


class CartItemAddAPIView(generics.CreateAPIView):
    """
    POST /api/cart/items/ – Добавить товар в корзину
    """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        cart = get_cart_from_request(self.request)
        product = serializer.validated_data.get("product")
        quantity = serializer.validated_data.get("quantity", 1)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )
        # Если элемент уже существует, просто увеличиваем количество
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Присваиваем сохранённый объект сериализатору,
        # чтобы стандартный метод create() вернул данные с id и другими полями
        serializer.instance = cart_item


class CartItemUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT/PATCH, DELETE /api/cart/items/<int:pk>/ – Работа с конкретным элементом корзины
    """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        cart = get_cart_from_request(self.request)
        return cart.items.all()
