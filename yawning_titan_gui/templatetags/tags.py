import json
from typing import Any

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


@register.simple_tag
def value_at(_dict: dict, key: Any):
    """Return value of dict at key"""
    return _dict.get(key)


@register.filter
def next_key(_dict: dict, key: int):
    """
    Get the next key in a dictionary.

    Use key_index + 1 if there is a subsequent key
    otherwise return first key.
    """
    keys = list(_dict.keys())
    key_index = keys.index(key)
    if key_index < (len(keys) - 1):
        return keys[key_index + 1]
    return keys[0]


@register.filter
def url_trim(url: str, n: int):
    """Trim url to n parameters"""
    url_components = url.split("/")
    return "/".join(url_components[: n + 1]) + "/"
