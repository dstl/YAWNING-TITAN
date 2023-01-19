import pytest

from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.float_item import FloatProperties
from yawning_titan.config.item_types.int_item import IntProperties
from yawning_titan.exceptions import ConfigItemValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "allow_null, test_val, passed, fail_reason",
    [
        (True, None, True, None),
        (False, None, False, "Value None when allow_null is not permitted."),
    ],
)
def test_bool_item_validation(allow_null, test_val, passed, fail_reason):
    """Tests validation of a bool by `BoolProperties`."""
    bool_properties = BoolProperties(allow_null=allow_null)
    bool_item = BoolItem(value=test_val, properties=bool_properties)

    validation = bool_item.validation

    assert validation.passed == passed
    if not validation.passed:
        assert type(validation.fail_exception) == ConfigItemValidationError
        assert validation.fail_reason == fail_reason


def test_bool_item_incorrect_properties_type():
    """Tests instantiation fails with incorrect properties type."""
    with pytest.raises(TypeError):
        BoolItem(value=True, properties=IntProperties())
    with pytest.raises(TypeError):
        BoolItem(value=True, properties=FloatProperties())
