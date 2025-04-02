from django.urls import path
from .views import CreateOrderAPIView, OrderListAPIView

urlpatterns = [
    path('create/', CreateOrderAPIView.as_view(), name='order-create'),
    path('list/', OrderListAPIView.as_view(), name='order-list'),
]
