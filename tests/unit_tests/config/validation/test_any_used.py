from typing import Optional

import pytest

from yawning_titan.config.groups.core import UseValueGroup
from yawning_titan.config.groups.validation import AnyUsedGroup
from yawning_titan.config.item_types.bool_item import BoolItem
from yawning_titan.exceptions import ConfigGroupValidationError


class Group(AnyUsedGroup):
    """Basic implementation of validation group :class: `~yawning_titan.config.groups.validation.AnyUsedGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.a = BoolItem(value=False)
        self.b = BoolItem(value=False)
        self.c = UseValueGroup(use=False, value=0.5)
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
def test_use_value_used(test_group: Group):
    """Test the validation when a :class: `~yawning_titan.config.groups.core.UseValueGroup` is used."""
    test_group.c.use.value = True
    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_use_value_used_and_bool_item_true(test_group: Group):
    """Test the validation when a :class: `~yawning_titan.config.groups.core.UseValueGroup` is used and :class: `~yawning_titan.config.item_types.bool_item.BoolItem`."""
    test_group.c.use.value = True
    test_group.b.value = True
    test_group.validate()

    assert test_group.validation.passed


@pytest.mark.unit_test
def test_none_used(test_group: Group):
    """Test the validation when no elements are used."""
    test_group.validate()

    assert not test_group.validation.passed
    assert "At least 1 of a, b, c should be used" in test_group.validation.fail_reasons

    with pytest.raises(ConfigGroupValidationError):
        raise test_group.validation.fail_exceptions[0]
