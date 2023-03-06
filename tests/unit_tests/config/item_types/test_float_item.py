import pytest

from yawning_titan.config.item_types.bool_item import BoolProperties
from yawning_titan.config.item_types.float_item import (
    FloatItem,
    FloatProperties,
)
from yawning_titan.config.item_types.int_item import IntProperties
from yawning_titan.config.item_types.str_item import StrProperties
from yawning_titan.exceptions import ConfigItemValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "min_val, max_val, allow_null, inclusive_min, inclusive_max, test_val, passed, fail_reason",
    # fmt: off
    [
        (0.0, 100.0, False, None, True, None, False, "Value None when allow_null is not permitted."),
        (0.0, 100.0, True, None, True, None, True, None),
        (0.0, 100.0, None, None, True, 100.0, True, None),
        (0.0, 100.0, None, None, True, 100.0, True, None),
        (0.0, 100.0, None, None, True, 101.5, False, "Value 101.5 is greater than the max property 100.0."),
        (0.0, 100.0, None, None, False, 100.0, False, "Value 100.0 is equal to the max value 100.0 but the range is not inclusive of this value."),
        (0.0, 100.0, None, None, False, 99.9, True, None),
        (0.0, 100.0, None, True, None, 0.0, True, None),
        (0.0, 100.0, None, None, None, 0.0, False, "Value 0.0 is equal to the min value 0.0 but the range is not inclusive of this value."),
        (0.0, 100.0, None, False, None, 1.0, True, None),
        (0.0, 100.0, None, False, None, 0.0, False, "Value 0.0 is equal to the min value 0.0 but the range is not inclusive of this value."),
        (0.0, 100.0, None, True, None, -1.0, False, "Value -1.0 is less than the min property 0.0."),
        (0.0, 100.0, None, None, True, "100.0", False, "Value 100.0 is of type <class 'str'>, should be <class 'float'> or <class 'int'>."),
    ],
    # fmt: on
)
def test_float_properties_validation(
    min_val,
    max_val,
    allow_null,
    inclusive_min,
    inclusive_max,
    test_val,
    passed,
    fail_reason,
):
    """Tests validation of a float by `FloatProperties`."""
    float_properties = FloatProperties(
        min_val=min_val,
        max_val=max_val,
        allow_null=allow_null,
        inclusive_min=inclusive_min,
        inclusive_max=inclusive_max,
    )

    validation = float_properties.validate(test_val)
    assert validation.passed == passed
    if not validation.passed:
        assert type(validation.fail_exceptions[0]) == ConfigItemValidationError
        assert validation.fail_reasons[0] == fail_reason


@pytest.mark.unit_test
def test_float_item_incorrect_properties_type():
    """Tests instantiation fails with incorrect properties type."""
    with pytest.raises(TypeError):
        FloatItem(value=1.0, properties=BoolProperties())
    with pytest.raises(TypeError):
        FloatItem(value=1.0, properties=IntProperties())
    with pytest.raises(TypeError):
        FloatItem(value=1.0, properties=StrProperties())
