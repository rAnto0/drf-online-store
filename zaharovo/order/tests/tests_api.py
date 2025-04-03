from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from products.models import Product, Category
from order.models import Order, OrderItem
from cart.models import Cart, CartItem

User = get_user_model()


class OrderAPITest(APITestCase):
    def setUp(self):
        # Создаем пользователя и авторизуем его
        self.user = User.objects.create_user(
            username="orderuser",
            email="order@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем категорию и продукт
        self.category = Category.objects.create(
            name="Order Category",
            slug="order-category",
            description="Test category for orders"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Order Product",
            description="Product description",
            price=Decimal("50.00"),
            stock=10
        )

        # URL для создания заказа
        self.create_order_url = reverse('order-create')
        # URL для получения списка заказов
        self.order_list_url = reverse('order-list')

    def test_create_order_empty_cart(self):
        """
        Проверяем, что если корзина пуста, оформление заказа возвращает ошибку.
        """
        response = self.client.post(self.create_order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Корзина пуста.")

    def test_create_order_with_items(self):
        """
        Проверяем оформление заказа: данные из корзины копируются в заказ,
        сумма вычисляется, и корзина очищается.
        """
        # Создаем корзину для пользователя
        cart = Cart.objects.create(user=self.user)
        # Добавляем в корзину 2 единицы продукта (при цене 50.00 => итог 100.00)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        response = self.client.post(self.create_order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что заказ создан и итоговая сумма равна 100.00
        order_data = response.data
        self.assertEqual(order_data["total_amount"], "100.00")
        # Проверяем, что заказ содержит 1 элемент с количеством 2
        self.assertEqual(len(order_data["items"]), 1)
        self.assertEqual(order_data["items"][0]["quantity"], 2)

        # Проверяем, что корзина очищена
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 0)

    def test_order_list(self):
        """
        Проверяем, что после создания заказа он появляется в списке заказов пользователя.
        """
        # Создаем заказ вручную для пользователя
        order = Order.objects.create(user=self.user, total_amount=Decimal("150.00"))
        OrderItem.objects.create(order=order, product=self.product, quantity=3, price=self.product.price)

        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ожидаем, что в списке заказов будет 1 заказ
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total_amount"], "150.00")
