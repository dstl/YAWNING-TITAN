from typing import Optional

import pytest

from yawning_titan.config.groups.validation import AnyNonZeroGroup
from yawning_titan.config.item_types.float_item import FloatItem
from yawning_titan.config.item_types.int_item import IntItem
from yawning_titan.config.item_types.str_item import StrItem
from yawning_titan.exceptions import ConfigGroupValidationError


class Group(AnyNonZeroGroup):
    """Basic implementation of validation group :class: `~yawning_titan.config.groups.validation.AnyNonZeroGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.a = IntItem(value=0)
        self.b = FloatItem(value=0)
        self.c = FloatItem(value=0)
        super().__init__(doc)


@pytest.fixture
def test_group() -> Group:
    """A test group with a mixture of :class: `~yawning_titan.config.item_types.bool_item.BoolItem`'s and :class: `~yawning_titan.config.groups.core.UseValueGroup`'s."""
    test_group = Group()
    return test_group


@pytest.fixture
def nested_group() -> Group:
    """A nested test group with a mixture of :class: `~yawning_titan.config.item_types.bool_item.BoolItem`'s and :class: `~yawning_titan.config.groups.core.UseValueGroup`'s."""
    test_group = Group()
    return test_group


@pytest.mark.unit_test
def test_all_zero(test_group: Group):
    """Test the validation when no items are above 0."""
    test_group.validate()

    assert not test_group.validation.passed
    assert (
        "At least 1 of a, b, c should be above 0" in test_group.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise test_group.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_all_zero_or_none(test_group: Group):
    """Test the validation when no items are above 0 and some are None."""
    test_group.a.value = None

    test_group.validate()

    assert not test_group.validation.passed
    assert (
        "At least 1 of a, b, c should be above 0" in test_group.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise test_group.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_single_item_above_zero(test_group: Group):
    """Test the validation when a single item is above 0."""
    test_group.a.value = 1

    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_multiple_items_above_zero(test_group: Group):
    """Test the validation when multiple items are above 0."""
    test_group.a.value = 1
    test_group.c.value = 1

    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_non_numeric_type(test_group: Group):
    """Test the validation when an item is not of a numeric type."""
    test_group.a.value = 1
    test_group.c = StrItem("test")

    test_group.validate()

    assert test_group.validation.passed
