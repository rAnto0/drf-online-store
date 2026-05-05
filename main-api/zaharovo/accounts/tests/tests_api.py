from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile, Address

User = get_user_model()


class RegistrationAPITest(APITestCase):
    def test_registration_creates_user_and_profile(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user = User.objects.get(username="newuser")
        # Проверяем, что профиль создан автоматически
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, Profile)


class ProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser", email="profile@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("profile-detail")  # /api/accounts/profile/

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "profileuser")
        self.assertEqual(response.data["email"], "profile@example.com")

    def test_update_profile_email_and_other_fields(self):
        data = {
            "email": "updated@example.com",
            "birth_date": "1990-01-01",
            "phone": "1234567890",
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(
            self.user.profile.birth_date.strftime("%Y-%m-%d"), "1990-01-01"
        )
        self.assertEqual(self.user.profile.phone, "1234567890")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")


class AddressAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="addressuser", email="address@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("address-list")  # /api/accounts/addresses/

    def test_create_address(self):
        data = {
            "street": "Береговая",
            "house": "1Б",
            "apartment": "471",
            "entrance": "5",
            "floor": "17",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Address.objects.filter(user=self.user, street="Береговая").exists()
        )

    def test_get_addresses(self):
        # Создадим два адреса для пользователя
        Address.objects.create(user=self.user, street="Улица 1", house="10")
        Address.objects.create(user=self.user, street="Улица 2", house="20")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Предполагаем, что возвращается список адресов
        self.assertEqual(len(response.data), 2)
