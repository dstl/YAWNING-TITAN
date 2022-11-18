from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
import json

register = template.Library()

#basic helper tags

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter
def to_id(value:str):
    return value.replace(" ","-")

@register.filter
def get_url(url_name:str):
    try:
        return reverse(url_name)
    except Exception:
        return ""