from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, ProfileSerializer, AddressSerializer, ChangePasswordSerializer, \
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .models import Address


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/ – добавление нового пользователя
    """
    serializer_class = RegisterSerializer


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    GET /api/accounts/profile/ – получить профиль текущего пользователя
    PUT/PATCH /api/accounts/profile/ – обновить профиль текущего пользователя
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращаем профиль, связанный с текущим пользователем
        return self.request.user.profile


class AddressListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/accounts/addresses/ – список адресов текущего пользователя
    POST /api/accounts/addresses/ – добавление нового адреса
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
    GET /api/accounts/addresses/<int:pk>/ – детали конкретного адреса
    PUT/PATCH /api/accounts/addresses/<int:pk>/ – обновление адреса
    DELETE /api/accounts/addresses/<int:pk>/ – удаление адреса
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ограничиваем доступ к адресам текущего пользователя
        return Address.objects.filter(user=self.request.user)


class ChangePasswordView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/accounts/auth/change_password/ - смена пароля(авторизованного пользователя)
    """
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Меняем пароль
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"detail": "Пароль успешно изменён"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    POST /api/accounts/auth/reset_password/ - запрос на email сменить пароль
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Отправка email происходит здесь
        return Response({"detail": "Инструкции по сбросу пароля отправлены на указанный email."},
                        status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    POST /api/accounts/auth/reset_password_confirm/ - подтверждение данных(uid, token), смена пароля если данные верны
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно изменён."}, status=status.HTTP_200_OK)
