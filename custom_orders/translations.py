from modeltranslation.translator import translator, TranslationOptions
from .models import DressModel, Textile, Color, CustomOrder

class DressModelTranslationOptions(TranslationOptions):
    fields = ('name',)

class TextileTranslationOptions(TranslationOptions):
    fields = ('name',)

class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)


class CustomOrderTranslationOptions(TranslationOptions):
    fields = ('comment',)

translator.register(DressModel, DressModelTranslationOptions)
translator.register(Textile, TextileTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(CustomOrder, CustomOrderTranslationOptions)
