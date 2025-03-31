from rest_framework import generics, permissions

from .models import Cart
from .serializers import CartSerializer, CartItemSerializer


def get_cart_from_request(request):
    """Утилитная функция для получения корзины из запроса."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


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
        serializer.save(cart=cart)


class CartItemUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT/PATCH, DELETE /api/cart/items/<int:pk>/ – Работа с конкретным элементом корзины
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        cart = get_cart_from_request(self.request)
        return cart.items.all()
