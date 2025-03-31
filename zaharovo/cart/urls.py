from django.urls import path

from .views import CartDetailAPIView, CartItemAddAPIView, CartItemUpdateDeleteAPIView

urlpatterns = [
    path('', CartDetailAPIView.as_view(), name='cart-detail'),
    path('items/', CartItemAddAPIView.as_view(), name='cart-item-add'),
    path('items/<int:pk>/', CartItemUpdateDeleteAPIView.as_view(), name='cart-item-detail'),
]
