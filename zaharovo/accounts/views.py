from rest_framework import generics, permissions

from .serializers import RegisterSerializer, ProfileSerializer, AddressSerializer
from .models import Address


class RegisterView(generics.CreateAPIView):
    """
    POST /api/register/ – добавление нового пользователя
    """
    serializer_class = RegisterSerializer


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    GET /api/profile/ – получить профиль текущего пользователя
    PUT/PATCH /api/profile/ – обновить профиль текущего пользователя
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращаем профиль, связанный с текущим пользователем
        return self.request.user.profile


class AddressListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/addresses/ – список адресов текущего пользователя
    POST /api/addresses/ – добавление нового адреса
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только адреса, принадлежащие текущему пользователю
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/addresses/<int:pk>/ – детали конкретного адреса
    PUT/PATCH /api/addresses/<int:pk>/ – обновление адреса
    DELETE /api/addresses/<int:pk>/ – удаление адреса
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ограничиваем доступ к адресам текущего пользователя
        return Address.objects.filter(user=self.request.user)
