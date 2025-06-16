from rest_framework import generics, permissions
from .models import DressModel, Textile, Color, Size, CustomOrder
from .serializers import (
    DressModelSerializer, TextileSerializer, ColorSerializer, SizeSerializer, CustomOrderSerializer
)
from asgiref.sync import async_to_sync
from bot.notifications import send_custom_order_notification

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

class CustomOrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomOrder.objects.all()
    serializer_class = CustomOrderSerializer

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        async_to_sync(send_custom_order_notification)(order)
