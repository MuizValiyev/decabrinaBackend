from modeltranslation.translator import translator, TranslationOptions
from products.models import Product, Color, Textile

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'price_info',)

class TextileTranslationOptions(TranslationOptions):
    fields = ('name',)

class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Product, ProductTranslationOptions)
translator.register(Textile, TextileTranslationOptions)
translator.register(Color, ColorTranslationOptions)

