from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Ad)
class AdTranslationOpitions(TranslationOptions):
    fields = ('title', 'description')