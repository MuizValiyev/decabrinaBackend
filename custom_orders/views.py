from rest_framework import generics
from .models import DressModel, Textile, Color, Size, CustomOrder
from .serializers import (DressModelSerializer, TextileSerializer, ColorSerializer, SizeSerializer, CustomOrderSerializer)

# Справочники

class DressModelListAPIView(generics.ListAPIView):
    queryset = DressModel.objects.all()
    serializer_class = DressModelSerializer

class TextileListAPIView(generics.ListAPIView):
    queryset = Textile.objects.all()
    serializer_class = TextileSerializer

class ColorListAPIView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class SizeListAPIView(generics.ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

# Создание кастомного заказа

class CustomOrderCreateAPIView(generics.CreateAPIView):
    queryset = CustomOrder.objects.all()
    serializer_class = CustomOrderSerializer
