from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from .models import CartItem
from products.models import Product, ProductSize, Color, Textile
from .serializers import (
    CartItemSerializer,
    AddToCartSerializer,
    SelectCartItemsSerializer,
    CartItemsByIdsSerializer
)


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

        cart_item = CartItem.objects.filter(
            user=request.user,
            product=product,
            size=size,
            color=color,
            textile=textile
        ).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                size=size,
                color=color,
                textile=textile
            )

        return Response({'detail': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)


class CartListAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = self.get_serializer(cart_items, many=True)
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
    serializer_class = CartItemsByIdsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data['ids']
        items = CartItem.objects.filter(user=request.user, id__in=ids)
        response_serializer = CartItemSerializer(items, many=True)
        return Response(response_serializer.data)
