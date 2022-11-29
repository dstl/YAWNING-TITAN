import json

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

# basic helper tags


@register.filter(is_safe=True)
def js(obj):
    """Return argument in javascript markup."""
    return mark_safe(json.dumps(obj))


@register.filter
def to_id(value: str):
    """Replaces spaces with dashes in string argument to form html formatted id."""
    return value.replace(" ", "-")


@register.filter
def get_url(url_name: str):
    """
    Wrapped implementation of Django's reverse url.

    A lookup that returns the url by name
    or empty string when the url does not exist.
    """
    try:
        return reverse(url_name)
    except Exception:
        return ""
