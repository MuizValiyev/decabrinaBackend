from rest_framework import serializers
from .models import CartItem
from products.models import Product


class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_selected']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class SelectCartItemsSerializer(serializers.Serializer):
    selected_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    select_all = serializers.BooleanField(required=False)
