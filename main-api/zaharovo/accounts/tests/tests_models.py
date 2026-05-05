from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile, Address

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        # Создаём пользователя, профиль для него создаётся автоматически через сигнал
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="strongpassword123"
        )

    def test_profile_created_on_user_creation(self):
        # Проверяем, что у пользователя появился профиль
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str(self):
        # Проверяем строковое представление профиля
        self.assertEqual(str(self.user.profile), f"Профиль {self.user.username}")


class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="addressuser",
            email="address@example.com",
            password="strongpassword123",
        )
        self.address = Address.objects.create(
            user=self.user,
            street="Улица Ленина",
            house="10",
            apartment="5A",
            entrance="1",
            floor="2",
            is_default=True,
        )

    def test_address_str(self):
        # Если apartment задано, строковое представление будет включать его
        expected_str = "Улица Ленина, д. 10, кв. 5A"
        self.assertEqual(str(self.address), expected_str)
