from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ProfileDetailAPIView, AddressListCreateAPIView, AddressDetailAPIView, \
    ChangePasswordView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    # Эндпоинт регистрации
    path('register/', RegisterView.as_view(), name='register'),

    # Эндпоинты для получения JWT-токена:
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Эндпоинты данных профиля:
    path('profile/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),

    # Эндпоинты для смены пароля:
    path('auth/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/reset_password/', PasswordResetRequestView.as_view(), name='reset_password'),
    path('auth/reset_password_confirm/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
]
