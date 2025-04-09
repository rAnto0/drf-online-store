from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from products.models import Product, Category

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cartuser", email="cart@example.com", password="password123")
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_str_with_user(self):
        expected = f"Корзина пользователя {self.user.username}"
        self.assertEqual(str(self.cart), expected)

    def test_cart_str_without_user(self):
        cart = Cart.objects.create(session_key="abc123")
        expected = "Корзина с session_key abc123"
        self.assertEqual(str(cart), expected)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category", description="desc")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="Test product description",
            price=Decimal("100.00"),
            stock=5
        )
        self.user = User.objects.create_user(username="cartuser2", email="cart2@example.com", password="password123")
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_str(self):
        expected = f"2 x {self.product.name}"
        self.assertEqual(str(self.cart_item), expected)
