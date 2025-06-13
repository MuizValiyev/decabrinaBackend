from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem

import asyncio
from bot.notifications import send_order_notification

class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        order = serializer.save(user=user)

        cart_items = CartItem.objects.filter(user=user, is_selected=True)

        if not cart_items.exists():
            return Response({"detail": "Нет выбранных товаров в корзине."}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                color=item.color,
                textile=item.textile
            )

        cart_items.delete()

        asyncio.run(send_order_notification(order))

        return Response({
            "message": "Заказ успешно оформлен",
            "order_id": order.id
        }, status=status.HTTP_201_CREATED)
