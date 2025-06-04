from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import CartItem
from products.models import Product
from .serializers import (CartItemSerializer, AddToCartSerializer, SelectCartItemsSerializer)


class AddToCartAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'detail': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)


class CartListAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)


class SelectCartItemsAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SelectCartItemsSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        selected_ids = serializer.validated_data.get('selected_ids', [])
        select_all = serializer.validated_data.get('select_all', None)

        items = CartItem.objects.filter(user=request.user)

        if select_all is not None:
            items.update(is_selected=select_all)
        else:
            for item in items:
                item.is_selected = item.id in selected_ids
                item.save()

        return Response({'detail': 'Выбор обновлен'})


class CartItemsByIdsAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ids = request.data.get('ids', [])
        items = CartItem.objects.filter(user=request.user, id__in=ids)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
