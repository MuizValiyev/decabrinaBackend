from rest_framework import serializers
from .models import DressModel, Textile, Color, Size, CustomOrder

class DressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DressModel
        fields = ['id', 'name']

class TextileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textile
        fields = ['id', 'name']
        ref_name = "CustomOrdersTextileSerializer"

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']
        ref_name = "CustomOrdersColorSerializer"

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'label']

class CustomOrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = CustomOrder
        fields = [
            'id', 'model', 'textile', 'color', 'size',
            'phone', 'city', 'address',
            'bust', 'waist', 'hips', 'height', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']
