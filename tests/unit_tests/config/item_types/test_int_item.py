import pytest

from yawning_titan.config.item_types.bool_item import BoolProperties
from yawning_titan.config.item_types.float_item import FloatProperties
from yawning_titan.config.item_types.int_item import IntItem, IntProperties, Parity
from yawning_titan.config.item_types.str_item import StrProperties
from yawning_titan.exceptions import ConfigItemValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "min_val, max_val, allow_null, parity, inclusive_min, inclusive_max, test_val, passed, fail_reason",
    # fmt: off
    [
        (0, 100, False, None, None, None, None, False,
         "Value None when allow_null is not permitted."),
        (0, 100, True, None, None, False, None, True, None),
        (0, 100, None, None, None, True, 100, True, None),
        (0, 100, None, None, None, None, 100, False,
         "Value 100 is equal to the max value 100 but the range is not inclusive of this value."),
        (0, 100, None, None, None, True, 101, False,
         "Value 101 is greater than the max property 100."),
        (0, 100, None, None, None, False, 100, False,
         "Value 100 is equal to the max value 100 but the range is not inclusive of this value."),
        (0, 100, None, None, None, False, 99, True, None),
        (0, 100, None, None, True, None, 0, True, None),
        (0, 100, None, None, None, None, 0, False,
         'Value 0 is equal to the min value 0 but the range is not inclusive of this value.'),
        (0, 100, None, None, False, None, 1, True, None),
        (0, 100, None, None, False, None, 0, False,
         "Value 0 is equal to the min value 0 but the range is not inclusive of this value."),
        (0, 100, None, None, False, None, -1, False,
         "Value -1 is less than the min property 0."),
        (0, 100, None, Parity.EVEN, None, True, 100, True, None),
        (0, 100, None, Parity.EVEN, None, None, 99, False,
         "Value 99 is not even."),
        (0, 100, None, Parity.ODD, None, None, 99, True, None),
        (0, 100, None, Parity.ODD, None, None, 100, False,
         "Value 100 is not odd."),
        (0, 100, None, None, None, False, "100", False,
         "Value 100 is of type <class 'str'>, should be <class 'int'>."),
    ],
    # fmt: on
)
def test_int_properties_validation(
    min_val,
    max_val,
    allow_null,
    parity,
    inclusive_min,
    inclusive_max,
    test_val,
    passed,
    fail_reason,
):
    """Tests validation of an integer by `IntProperties`."""
    int_properties = IntProperties(
        min_val=min_val,
        max_val=max_val,
        allow_null=allow_null,
        parity=parity,
        inclusive_min=inclusive_min,
        inclusive_max=inclusive_max,
    )

    validation = int_properties.validate(test_val)
    assert validation.passed == passed
    if not validation.passed:
        assert type(validation.fail_exceptions[0]) == ConfigItemValidationError
        assert fail_reason in validation.fail_reasons


@pytest.mark.unit_test
def test_int_item_incorrect_properties_type():
    """Tests instantiation fails with incorrect properties type."""
    with pytest.raises(TypeError):
        IntItem(value=1, properties=BoolProperties())
    with pytest.raises(TypeError):
        IntItem(value=1, properties=FloatProperties())
    with pytest.raises(TypeError):
        IntItem(value=1, properties=StrProperties())
