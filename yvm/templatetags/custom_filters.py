from django import template
from django.utils.translation import get_language

register = template.Library()

@register.filter(name='translate_URL')
def translate_URL(string):
    language_code = get_language()
    string = string.replace('/en/', f"/{language_code}/")
    string = string.replace('l=en', f"l={language_code}")
    string = string.replace('lang=en', f"lang={language_code}")
    string = string.replace('_EN', f"_{language_code.upper()}")
    return string



@register.filter
def keyvalue(dico, key):
    return dico.get(key, '')

