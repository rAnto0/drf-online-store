"""
URL configuration for zaharovo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet, CategoryViewSet
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    # Основные эндпоинты
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Эндпоинты приложения accounts:
    path("api/accounts/", include("accounts.urls")),
    # Эндпоинты приложения cart
    path("api/cart/", include("cart.urls")),
    # Эндпоинты приложения order
    path("api/order/", include("order.urls")),
]

urlpatterns += doc_urls
