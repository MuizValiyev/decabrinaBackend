from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer, ProductSizeSerializer  # нужно его определить, см. ниже


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # тут вернет всё поле Product
    size = ProductSizeSerializer(read_only=True)  # тут вернет всё поле ProductSize
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'size', 'color', 'textile', 'quantity', 'is_selected']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    size_id = serializers.IntegerField(required=False)
    color_id = serializers.IntegerField(required=False)
    textile_id = serializers.IntegerField(required=False)


class UpdateCartItemQuantitySerializer(serializers.Serializer):
    cart_item_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['+', '-'])
