from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from .models import CartItem
from products.models import Product, ProductSize, Color, Textile
from .serializers import (CartItemSerializer, AddToCartSerializer, UpdateCartItemQuantitySerializer,)


class AddToCartAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        size_id = serializer.validated_data.get('size_id')
        color_id = serializer.validated_data.get('color_id')
        textile_id = serializer.validated_data.get('textile_id')

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(ProductSize, id=size_id) if size_id else None
        color = get_object_or_404(Color, id=color_id) if color_id else None
        textile = get_object_or_404(Textile, id=textile_id) if textile_id else None

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size,
            color=color,
            textile=textile,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'detail': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)


class CartListAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)


class UpdateCartItemQuantityAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateCartItemQuantitySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item = get_object_or_404(CartItem, id=serializer.validated_data['cart_item_id'], user=request.user)
        action = serializer.validated_data['action']

        if action == '+':
            cart_item.quantity += 1
        elif action == '-':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return Response({'detail': 'Количество не может быть меньше 1'}, status=400)

        cart_item.save()
        return Response({'detail': 'Количество обновлено', 'quantity': cart_item.quantity})
