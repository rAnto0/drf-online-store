from django.test import TestCase
from products.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test description"
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test description"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="Test product description",
            price=99.99,
            stock=10
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_in_stock_property(self):
        # Если stock > 0, in_stock должна возвращать True
        self.assertTrue(self.product.in_stock)
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)
