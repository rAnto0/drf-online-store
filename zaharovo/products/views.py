from rest_framework.viewsets import ModelViewSet

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(ModelViewSet):
    """
    API-эндпоинты для товаров:
    - GET /api/products/ — список товаров (можно фильтровать, например, по категории через query-параметры)
    - GET /api/products/<int:pk>/ — детали товара по id
    - POST /api/products/ — создание нового товара
    - PUT/PATCH /api/products/<int:pk>/ — обновление товара
    - DELETE /api/products/<int:pk>/ — удаление товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    """
    API-эндпоинты для категорий:
    - GET /api/categories/ — список категорий
    - GET /api/categories/<slug:slug>/ — детали категории по slug
    - POST /api/categories/ — создание новой категории
    - PUT/PATCH /api/categories/<slug:slug>/ — обновление категории
    - DELETE /api/categories/<slug:slug>/ — удаление категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'  # Используем slug для идентификации вместо id
