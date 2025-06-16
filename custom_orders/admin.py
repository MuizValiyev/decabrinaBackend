from django.contrib import admin
from .models import DressModel, Textile, Color, Size, CustomOrder


class DressModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class TextileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'label']
    search_fields = ['label']


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'textile', 'color', 'size', 'created_at']
    list_filter = ['model', 'textile', 'color', 'size', 'created_at']
    search_fields = ['comment']
    readonly_fields = ['created_at']


admin.site.register(DressModel,DressModelAdmin)
admin.site.register(Textile,TextileAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(CustomOrder,CustomOrderAdmin)