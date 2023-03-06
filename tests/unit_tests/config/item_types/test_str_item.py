import pytest

from yawning_titan.config.item_types.bool_item import BoolProperties
from yawning_titan.config.item_types.float_item import FloatProperties
from yawning_titan.config.item_types.int_item import IntProperties
from yawning_titan.config.item_types.str_item import StrItem, StrProperties
from yawning_titan.exceptions import ConfigItemValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "allow_null, options, test_val, passed, fail_reason",
    [
        (True, None, None, True, None),
        (True, None, "1", True, None),
        (True, ["a", "b", "c"], "a", True, None),
        (True, [1, 2, 3], "1", False, "Value 1 should be one of 1, 2, 3"),
        (True, ["a", "b", "c"], "d", False, "Value d should be one of a, b, c"),
        (False, None, None, False, "Value None when allow_null is not permitted."),
        (
            False,
            None,
            1,
            False,
            "Value 1 is of type <class 'int'>, should be <class 'str'>.",
        ),
    ],
)
def test_bool_properties_validation(allow_null, options, test_val, passed, fail_reason):
    """Tests validation of a bool by `BoolProperties`."""
    str_properties = StrProperties(allow_null=allow_null, options=options)

    validation = str_properties.validate(test_val)
    assert validation.passed == passed
    if not validation.passed:
        assert type(validation.fail_exceptions[0]) == ConfigItemValidationError
        assert fail_reason in validation.fail_reasons


@pytest.mark.unit_test
def test_str_item_incorrect_properties_type():
    """Tests instantiation fails with incorrect properties type."""
    with pytest.raises(TypeError):
        StrItem(value=True, properties=IntProperties())
    with pytest.raises(TypeError):
        StrItem(value=True, properties=FloatProperties())
    with pytest.raises(TypeError):
        StrItem(value=True, properties=BoolProperties())
