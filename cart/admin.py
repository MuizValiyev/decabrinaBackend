from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_cart', 'product', 'size', 'color', 'textile', 'quantity', 'is_selected')
    list_filter = ('is_selected', 'size', 'color', 'textile')
    search_fields = ('user__username', 'product__name')

    def get_cart(self, obj):
        return obj.user.cart
    get_cart.short_description = 'Cart'


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
