from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses"
    )
    street = models.CharField("Улица", max_length=255)
    house = models.CharField("Дом", max_length=50)
    apartment = models.CharField("Квартира", max_length=50, blank=True, null=True)
    entrance = models.CharField("Подъезд", max_length=50, blank=True, null=True)
    floor = models.CharField("Этаж", max_length=50, blank=True, null=True)
    is_default = models.BooleanField("Адрес по умолчанию", default=False)

    def __str__(self):
        return f"{self.street}, д. {self.house}" + (
            f", кв. {self.apartment}" if self.apartment else ""
        )
