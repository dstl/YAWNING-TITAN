import pytest

from yawning_titan.config.toolbox.float_item import FloatProperties
from yawning_titan.exceptions import ConfigItemValidationError


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "min_val, max_val, allow_null, exclusive_min, exclusive_max, test_val, passed, fail_reason",
    [
        (
            0.0,
            100.0,
            False,
            None,
            False,
            None,
            False,
            "Value None when allow_null is not permitted.",
        ),
        (0.0, 100.0, True, None, False, None, True, None),
        (0.0, 100.0, None, None, False, 100.0, True, None),
        (0.0, 100.0, None, None, None, 100.0, True, None),
        (
            0.0,
            100.0,
            None,
            None,
            False,
            101.5,
            False,
            "Value 101.5 is greater than the max property 100.0.",
        ),
        (
            0.0,
            100.0,
            None,
            None,
            True,
            100.0,
            False,
            "Value 100.0 is greater than the max property 99.0 (max=100.0 exclusive of this value).",
        ),
        (0.0, 100.0, None, None, True, 99.9, True, None),
        (0.0, 100.0, None, False, None, 0.0, True, None),
        (0.0, 100.0, None, None, None, 0.0, True, None),
        (0.0, 100.0, None, True, None, 1.0, True, None),
        (
            0.0,
            100.0,
            None,
            True,
            None,
            0.0,
            False,
            "Value 0.0 is less than the min property 1.0 (min=0.0 exclusive of this value).",
        ),
        (
            0.0,
            100.0,
            None,
            False,
            None,
            -1.0,
            False,
            "Value -1.0 is less than the min property 0.0.",
        ),
        (
            0.0,
            100.0,
            None,
            None,
            False,
            "100.0",
            False,
            "Value 100.0 is of type <class 'str'>, not <class 'float'>.",
        ),
    ],
)
def test_float_properties__validation(
    min_val,
    max_val,
    allow_null,
    exclusive_min,
    exclusive_max,
    test_val,
    passed,
    fail_reason,
):
    """Tests validation of a float by `FloatProperties`."""
    float_properties = FloatProperties(
        min_val=min_val,
        max_val=max_val,
        allow_null=allow_null,
        exclusive_min=exclusive_min,
        exclusive_max=exclusive_max,
    )

    validation = float_properties.validate(test_val)
    print(validation)
    assert validation.passed == passed
    if not validation.passed:
        assert type(validation.fail_exception) == ConfigItemValidationError
        assert validation.fail_reason == fail_reason
