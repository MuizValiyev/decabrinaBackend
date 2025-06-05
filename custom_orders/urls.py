from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.DressModelListAPIView.as_view(), name='dressmodel-list'),
    path('textile/', views.TextileListAPIView.as_view(), name='textile-list'),
    path('colors/', views.ColorListAPIView.as_view(), name='color-list'),
    path('sizes/', views.SizeListAPIView.as_view(), name='size-list'),
    path('orders/create/', views.CustomOrderCreateAPIView.as_view(), name='customorder-create'),
]
