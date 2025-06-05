from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({
            "message": "Заказ успешно оформлен",
            "order_id": order.id
        }, status=status.HTTP_201_CREATED)
