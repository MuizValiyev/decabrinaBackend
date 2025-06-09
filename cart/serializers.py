from rest_framework import serializers
from .models import CartItem
from products.models import Product, ProductSize, Color, Textile


class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'
        ref_name = 'CartProductSizeSerializer'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color  
        fields = '__all__'
        ref_name = 'CartColorSerializer'


class TextileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textile
        fields = ['id', 'name']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    textile = TextileSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'size', 'color', 'textile', 'quantity', 'is_selected']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    size_id = serializers.IntegerField(required=False, allow_null=True)
    color_id = serializers.IntegerField(required=False, allow_null=True)
    textile_id = serializers.IntegerField(required=False, allow_null=True)


class SelectCartItemsSerializer(serializers.Serializer):
    selected_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    select_all = serializers.BooleanField(required=False)


class CartItemsByIdsSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField()
    )
