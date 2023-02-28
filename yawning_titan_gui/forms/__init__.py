from django.forms import widgets
from django import forms as django_forms


class RangeInput(widgets.NumberInput):
    """Custom widget for range input range input field."""

    input_type = "range"

def create_doc_meta_form(element_name) -> django_forms.Form:
    class DocMetaDataForm(django_forms.Form):
        name = django_forms.CharField(
            widget=widgets.TextInput(attrs={"class": "form-control"}),
            required=True,
            help_text=f"The name of the {element_name}",
            label="Name",
        )
        description = django_forms.CharField(
            widget=widgets.Textarea(attrs={"rows":5,"class": "form-control"}),
            required=False,
            help_text=f"A description of the {element_name}",
            label="Description",
        )
        author = django_forms.CharField(
            widget=widgets.TextInput(attrs={"class": "form-control"}),
            required=True,
            help_text=f"Your name",
            label="Author",
        )
    return DocMetaDataForm