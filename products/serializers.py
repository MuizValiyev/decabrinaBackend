from rest_framework import serializers
from .models import Category, Product, ProductSize, Textile, Color

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['size_label', 'bust', 'waist', 'hips', 'height']

class TextileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textile
        fields = ['id', 'name']
        ref_name = "ProductsTextileSerializer"  # Уникальное имя для drf-yasg

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    textiles = TextileSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'in_stock', 'sizes', 'textiles', 'colors']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'trends', 'products']
