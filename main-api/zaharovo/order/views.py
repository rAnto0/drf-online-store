from rest_framework import generics, permissions, status
from rest_framework.response import Response
from cart.utils import get_cart_from_request
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        cart = get_cart_from_request(request)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"detail": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем заказ
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None
        )

        total_amount = 0
        # Копируем данные из корзины в заказ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price  # фиксируем цену товара на момент заказа
            )
            total_amount += item.quantity * item.product.price

        order.total_amount = total_amount
        order.save()

        # Очистка корзины после создания заказа
        cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
