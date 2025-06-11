from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category, Textile, Color

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class TextileTranslationOptions(TranslationOptions):
    fields = ('name',)

class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Textile, TextileTranslationOptions)
translator.register(Color, ColorTranslationOptions)
