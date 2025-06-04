from django.contrib import admin
from .models import Category, Product, ProductSize



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name')
    search_fields = ('name',)
    ordering = ['id']



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price_info', 'in_stock', 'price')
    search_fields = ('name', 'description')
    list_filter = ('category', 'in_stock')
    ordering = ['id']
    autocomplete_fields = ['category']


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size_label', 'bust', 'waist', 'hips', 'height')
    list_filter = ('size_label', 'product')
    search_fields = ('product__name', 'bust', 'waist', 'hips', 'height')
    ordering = ['product', 'size_label']

admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)