from django.db import models
from django.conf import settings

class DressModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Textile(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Size(models.Model):
    label = models.CharField(max_length=10)  # например: S, M, L, 42, 44

    def __str__(self):
        return self.label

class CustomOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_orders')
    model = models.ForeignKey(DressModel, on_delete=models.SET_NULL, null=True, blank=True)
    textile = models.ForeignKey(Textile, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)

    bust = models.DecimalField("Обхват груди (см)", max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField("Обхват талии (см)", max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField("Обхват бедер (см)", max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField("Рост (см)", max_digits=5, decimal_places=2, null=True, blank=True)

    comment = models.TextField("Комментарий", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Order #{self.pk}"
