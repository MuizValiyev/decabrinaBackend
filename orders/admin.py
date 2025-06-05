from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'city', 'address', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('phone', 'city', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('phone', 'city', 'address')
        }),
        ('Дополнительно', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Order,OrderAdmin)