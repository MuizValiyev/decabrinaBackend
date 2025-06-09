from modeltranslation.translator import TranslationOptions, translator
from .models import Category, Textile, Color, Product

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class TextileTranslationOptions(TranslationOptions):
    fields = ('name',)

class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'textiles', 'colors',)

translator.register(Category, CategoryTranslationOptions)
translator.register(Textile, TextileTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Product, ProductTranslationOptions)