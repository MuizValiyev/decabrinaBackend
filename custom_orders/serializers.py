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
        ref_name = "CustomOrdersTextileSerializer"  # Уникальное имя для drf-yasg


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']
        ref_name = "CustomOrdersColorSerializer"  # уникальное имя для drf_yasg

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'label']

class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = [
            'id', 'model', 'textile', 'color', 'size',
            'bust', 'waist', 'hips', 'height', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']
