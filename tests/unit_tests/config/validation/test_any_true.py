from typing import Optional

import pytest

from yawning_titan.config.groups.validation import AnyTrueGroup
from yawning_titan.config.item_types.bool_item import BoolItem
from yawning_titan.config.item_types.str_item import StrItem
from yawning_titan.exceptions import ConfigGroupValidationError


class Group(AnyTrueGroup):
    """Basic implementation of validation group :class: `~yawning_titan.config.groups.validation.AnyTrueGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.a = BoolItem(value=False)
        self.b = BoolItem(value=False)
        self.c = BoolItem(value=False)
        super().__init__(doc)


@pytest.fixture
def test_group() -> Group:
    """A test group with a mixture of :class: `~yawning_titan.config.item_types.bool_item.BoolItem`'s and :class: `~yawning_titan.config.groups.core.UseValueGroup`'s."""
    test_group = Group()
    return test_group


@pytest.mark.unit_test
def test_bool_item_true(test_group: Group):
    """Test the validation when a :class: `~yawning_titan.config.item_types.bool_item.BoolItem` is True."""
    test_group.a.value = True
    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_bool_item_multiple_true(test_group: Group):
    """Test the validation when a :class: `~yawning_titan.config.item_types.bool_item.BoolItem` is True."""
    test_group.b.value = True
    test_group.c.value = True
    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_none_used(test_group: Group):
    """Test the validation when no elements are used."""
    test_group.validate()

    assert not test_group.validation.passed
    assert "At least 1 of a, b, c should be True" in test_group.validation.fail_reasons

    with pytest.raises(ConfigGroupValidationError):
        raise test_group.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_non_numeric_type(test_group: Group):
    """Test the validation when an item is not of a numeric type."""
    test_group.a.value = True
    test_group.c = StrItem("test")

    test_group.validate()

    assert test_group.validation.passed
