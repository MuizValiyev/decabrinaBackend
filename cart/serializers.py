from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'size', 'color', 'textile',
            'quantity', 'is_selected'
        ]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    size_id = serializers.IntegerField(required=False)
    color_id = serializers.IntegerField(required=False)
    textile_id = serializers.IntegerField(required=False)


class UpdateCartItemQuantitySerializer(serializers.Serializer):
    cart_item_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['+', '-'])
