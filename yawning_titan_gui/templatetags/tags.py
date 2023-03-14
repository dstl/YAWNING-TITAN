import json
from typing import Any

from django import template
from django.forms import Field
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


# Filter tags
@register.filter(is_safe=True)
def js(obj: Any):
    """Return argument in javascript markup.

    :param obj: An object to be converted to json format.

    :return: Json formatted representation of `obj`
    """
    return mark_safe(json.dumps(obj))


@register.filter
def to_id(value: str):
    """Replaces spaces with dashes in string argument to form html formatted id.

    :param value: A string value to be converted to an standard format html id.

    :return: The original string with spaces replaced with '-'.

    :Example::

    >>> {{'my object a'|to_id}}
    >>> my-object-a
    """
    return value.replace(" ", "-").lower()


@register.filter
def length(obj: Any) -> int:
    """
    Return the length of an object.

    :param obj: An object of unknown length

    :return: The length of `obj`
    """
    return len(obj)


@register.filter
def keys(_dict: dict):
    """
    Return the keys of dictionary as a list.

    :param _dict: a dict
    """
    return list(_dict.keys())


@register.filter
def format_text(text: str):
    """Return the text string with '_' replaced by spaces and first letter capitalized.

    :param text: a text string.
    """
    return text.replace("_", " ").capitalize()


@register.filter
def get_url(url_name: str):
    """
    Wrapped implementation of Django's reverse url.

    A lookup that returns the url by name
    or empty string when the url does not exist.

    :param url_name: The name of the url string as defined in `urls.py`.

    :return: The full url string as defined in `urls.py`
    """
    try:
        return reverse(url_name)
    except Exception:
        return ""


@register.filter
def url_trim(url: str, n: int):
    """Trim url to n parameters.

    :param url: A text string representing a url.
    """
    url_components = url.split("/")
    return "/".join(url_components[: n + 1]) + "/"


# Simple tags
@register.simple_tag
def value_at(_dict: dict, key: Any):
    """Return value of dict at key.

    :param _dict: A dict
    :param key: a key
    """
    return _dict.get(key)


@register.simple_tag
def get_title(field: Field, titles: dict):
    """Return the title label that precedes the given field name.

    :param field: A django form field.
    :param titles: the list of t
    """
    return titles.get(field.name)
