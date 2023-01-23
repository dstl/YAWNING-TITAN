import pytest

from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup
from yawning_titan.exceptions import ConfigGroupValidationError


@pytest.mark.unit_test
def test_restrict_range_not_used():
    """Test the :class:`~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` when not used."""
    restrict = RestrictRangeGroup(restrict=False)
    assert restrict.validation.passed
    assert restrict.validation.group_passed


@pytest.mark.unit_test
def test_restrict_range_valid_input():
    """Test the :class:`~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` when not used with a valid input."""
    restrict = RestrictRangeGroup(restrict=True, min=1, max=5)
    assert restrict.validation.passed
    assert restrict.validation.group_passed


@pytest.mark.unit_test
def test_restrict_range_min_greater_than_max():
    """Test the :class:`~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` with the minimum value greater than the maximum."""
    restrict = RestrictRangeGroup(restrict=True, min=5, max=1)
    assert not restrict.validation.passed
    with pytest.raises(ConfigGroupValidationError):
        raise restrict.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_restrict_range_no_range():
    """Test the :class:`~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` with no range set."""
    restrict = RestrictRangeGroup(restrict=True)
    assert not restrict.validation.passed
    with pytest.raises(ConfigGroupValidationError):
        raise restrict.validation.fail_exceptions[0]
