from django.db import models
from django.conf import settings
from products.models import Product, ProductSize, Color, Textile

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Размер")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Цвет")
    textile = models.ForeignKey(Textile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ткань")
    
    quantity = models.PositiveIntegerField(default=1)
    is_selected = models.BooleanField(default=True)

    def __str__(self):
        options = []
        if self.size:
            options.append(str(self.size))
        if self.color:
            options.append(str(self.color))
        if self.textile:
            options.append(str(self.textile))
        options_str = ", ".join(options)
        return f"{self.user.first_name} - {self.product.name} ({options_str}) x{self.quantity}"
