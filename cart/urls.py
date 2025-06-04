from django.urls import path
from .views import (AddToCartAPIView, CartListAPIView, SelectCartItemsAPIView, CartItemsByIdsAPIView)

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('select/', SelectCartItemsAPIView.as_view(), name='select-cart-items'),
    path('by-ids/', CartItemsByIdsAPIView.as_view(), name='cart-items-by-ids'),
]