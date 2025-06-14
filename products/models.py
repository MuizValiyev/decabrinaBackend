from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    image = models.ImageField("Изображение", upload_to='image/categories/')
    slug = models.SlugField(unique=True)
    trends = models.BooleanField(default=False, verbose_name='В тренде')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Textile(models.Model):
    name = models.CharField("Название ткани", max_length=100)

    class Meta:
        verbose_name = "Ткань"
        verbose_name_plural = "Ткани"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField("Цвет", max_length=50)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='image/products/')
    price_info = models.CharField(max_length=20)
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    textiles = models.ManyToManyField(Textile, related_name='products', verbose_name="Ткани", blank=True)
    colors = models.ManyToManyField(Color, related_name='products', verbose_name="Цвета", blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name="Товар"
    )
    size_label = models.CharField("Размер", max_length=5, choices=SIZE_CHOICES)
    bust = models.CharField("Грудь", max_length=20)
    waist = models.CharField("Талия", max_length=20)
    hips = models.CharField("Бёдра", max_length=20)
    height = models.CharField("Рост", max_length=20)

    class Meta:
        verbose_name = "Размер товара"
        verbose_name_plural = "Размеры товаров"

    def __str__(self):
        return f"{self.product.name} - {self.size_label}"
