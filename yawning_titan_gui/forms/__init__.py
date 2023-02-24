from django.forms import widgets


class RangeInput(widgets.NumberInput):
    """Custom widget for range input range input field."""

    input_type = "range"
