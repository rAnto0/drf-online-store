from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Category, Product


class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test description"
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name="Test Product 1",
            description="Description 1",
            price=50.00,
            stock=5
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Test Product 2",
            description="Description 2",
            price=100.00,
            stock=8
        )

    def test_get_product_list(self):
        url = reverse('product-list')  # Регистрируется роутером
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # С учетом пагинации, результаты будут в поле 'results'
        self.assertIn('results', response.data)
        # По умолчанию, page_size установлен в 2, и у нас создано 2 продукта
        self.assertEqual(len(response.data['results']), 2)

    def test_get_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Product 1")
        # Поле category должно быть представлено как slug
        self.assertEqual(response.data['category'], self.category.slug)


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test description"
        )

    def test_get_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Здесь, если у нас один объект, он может вернуться как список или словарь,
        # в зависимости от роутера. Обычно роутер DRF возвращает список.
        self.assertEqual(len(response.data), 1)

    def test_get_category_detail(self):
        url = reverse('category-detail', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Category")
