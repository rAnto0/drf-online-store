from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category

User = get_user_model()


class CartAPITest(APITestCase):
    def setUp(self):
        # Создаем авторизованного пользователя и аутентифицируем его
        self.user = User.objects.create_user(username="cartuser", email="cart@example.com", password="password123")
        self.client.force_authenticate(user=self.user)

        # Создаем категорию и продукт для корзины
        self.category = Category.objects.create(name="Test Category", slug="test-category", description="desc")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="Test product description",
            price=Decimal("100.00"),
            stock=5
        )

        # Получаем URL для корзины и для добавления элементов
        self.cart_detail_url = reverse('cart-detail')  # /api/cart/
        self.cart_item_add_url = reverse('cart-item-add')  # /api/cart/items/

    def test_get_empty_cart(self):
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Предполагаем, что если корзина пуста, items будет пустым списком
        self.assertEqual(response.data['items'], [])

    def test_add_cart_item_new(self):
        # Добавляем товар в корзину, если его еще нет
        data = {
            "product_id": self.product.id,
            "quantity": 2
        }
        response = self.client.post(self.cart_item_add_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что элемент появился в корзине
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['quantity'], 2)

    def test_add_cart_item_existing(self):
        # Сначала добавим товар
        data = {
            "product_id": self.product.id,
            "quantity": 2
        }
        self.client.post(self.cart_item_add_url, data, format='json')
        # Попробуем добавить тот же товар еще раз, например, с quantity 1
        data = {
            "product_id": self.product.id,
            "quantity": 1
        }
        response = self.client.post(self.cart_item_add_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что общее количество увеличилось (2 + 1 = 3)
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.data['items'][0]['quantity'], 3)

    def test_add_cart_item_exceed_stock(self):
        # Попробуем добавить количество, превышающее stock (stock = 5)
        data = {
            "product_id": self.product.id,
            "quantity": 4
        }
        # Сначала добавим 2 шт.
        self.client.post(self.cart_item_add_url, {"product_id": self.product.id, "quantity": 2}, format='json')
        # Теперь попробуем добавить еще 4 шт., что в сумме даст 6, что больше 5
        response = self.client.post(self.cart_item_add_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя добавить", str(response.data))

    def test_update_cart_item(self):
        # Добавим элемент в корзину
        data = {"product_id": self.product.id, "quantity": 2}
        response = self.client.post(self.cart_item_add_url, data, format='json')
        cart_item_id = response.data['id']
        update_url = reverse('cart-item-detail', kwargs={'pk': cart_item_id})
        # Обновляем количество на 3
        response = self.client.patch(update_url, {"quantity": 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 3)

    def test_delete_cart_item(self):
        # Добавляем элемент
        data = {"product_id": self.product.id, "quantity": 2}
        response = self.client.post(self.cart_item_add_url, data, format='json')
        cart_item_id = response.data['id']
        delete_url = reverse('cart-item-detail', kwargs={'pk': cart_item_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # После удаления корзина должна быть пустой
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.data['items'], [])
