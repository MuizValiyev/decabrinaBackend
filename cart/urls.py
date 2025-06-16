from django.urls import path
from .views import AddToCartAPIView, CartListAPIView, UpdateCartItemQuantityAPIView, DeleteCartItemAPIView

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('update-quantity/', UpdateCartItemQuantityAPIView.as_view(), name='update-cart-item-quantity'),
    path('cart/delete/<int:cart_item_id>/', DeleteCartItemAPIView.as_view(), name='cart-delete'),
]