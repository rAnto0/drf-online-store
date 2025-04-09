from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from order.models import Order, OrderItem
from products.models import Product, Category

User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            username="orderuser",
            email="order@example.com",
            password="password123"
        )
        # Создаем категорию и продукт
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Description for test category"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="Description for test product",
            price=Decimal("100.00"),
            stock=10
        )
        # Создаем заказ для пользователя
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("0.00")
        )
        # Создаем два элемента заказа
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price  # 100.00
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price  # 100.00
        )
        # Обновляем итоговую сумму заказа (2*100 + 1*100 = 300)
        self.order.total_amount = Decimal("300.00")
        self.order.save()

    def test_order_str(self):
        # Проверяем, что __str__ возвращает строку, содержащую слово "Заказ"
        self.assertIn("Заказ", str(self.order))
        self.assertIn(str(self.order.order_id), str(self.order))

    def test_order_total_amount(self):
        # Проверяем, что итоговая сумма заказа соответствует сумме позиций
        expected_total = (self.order_item1.quantity * self.order_item1.price +
                          self.order_item2.quantity * self.order_item2.price)
        self.assertEqual(self.order.total_amount, expected_total)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="orderuser2",
            email="order2@example.com",
            password="password123"
        )
        self.category = Category.objects.create(
            name="Another Category",
            slug="another-category",
            description="Another category description"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Another Product",
            description="Another product description",
            price=Decimal("50.00"),
            stock=5
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("0.00")
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=self.product.price  # 50.00
        )
        self.order.total_amount = Decimal("150.00")
        self.order.save()

    def test_order_item_str(self):
        # Проверяем строковое представление элемента заказа
        expected = f"{self.order_item.quantity} x {self.product.name} в заказе {self.order.order_id}"
        self.assertEqual(str(self.order_item), expected)
