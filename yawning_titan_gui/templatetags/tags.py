import json
from typing import Any

from django import template
from django.forms import Field
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

# Filter tags
@register.filter(is_safe=True)
def js(obj):
    """Return argument in javascript markup."""
    return mark_safe(json.dumps(obj))


@register.filter
def to_id(value: str):
    """Replaces spaces with dashes in string argument to form html formatted id."""
    return value.replace(" ", "-")


@register.filter
def length(obj: Any):
    "Return the length of an object."
    return len(obj)


@register.filter
def keys(_dict: dict):
    """Return the keys of dictionary as a list"""
    return list(_dict.keys())


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


@register.filter
def url_trim(url: str, n: int):
    """Trim url to n parameters."""
    url_components = url.split("/")
    return "/".join(url_components[: n + 1]) + "/"


# Simple tags
@register.simple_tag
def value_at(_dict: dict, key: Any):
    """Return value of dict at key."""
    return _dict.get(key)


@register.simple_tag
def label_subsection(field: Field, subsection_labels: dict):
    """
    Return the subsection label that precedes the given field name.
    """
    return subsection_labels.get(field.name)
