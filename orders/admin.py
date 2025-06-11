from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  
    readonly_fields = ('product', 'quantity', 'size', 'color', 'textile')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'city', 'address', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('phone', 'city', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'user')
    inlines = [OrderItemInline]  

    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'city', 'address')
        }),
        ('Дополнительно', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Order, OrderAdmin)
