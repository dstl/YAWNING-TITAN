import pytest

from yawning_titan.config.item_types.bool_item import BoolProperties
from yawning_titan.exceptions import ConfigValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "allow_null, test_val, passed, fail_reason",
    [
        (True, None, True, None),
        (False, None, False, "Value None when allow_null is not permitted.")
    ]
)
def test_bool_properties_validation(allow_null, test_val, passed, fail_reason):
    """Tests validation of a bool by `BoolProperties`."""
    bool_properties = BoolProperties(allow_null=allow_null)

    validation = bool_properties.validate(test_val)
    print(validation)
    assert validation.passed == passed
    if not validation.passed:
        print("")
        print(validation.fail_reason)
        assert type(validation.fail_exception) == ConfigValidationError
        assert validation.fail_reason == fail_reason
