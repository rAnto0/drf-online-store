from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly


class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50


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
    pagination_class = ProductPagination
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['category__slug']  # Фильтрация по слагу категории
    search_fields = ['name', 'description']  # Поиск по имени и описанию
    ordering_fields = ['price', 'name']  # Сортировка


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
    permission_classes = [IsAdminOrReadOnly]
