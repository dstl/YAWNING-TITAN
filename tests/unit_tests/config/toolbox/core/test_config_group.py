from pathlib import Path

import pytest

from tests.conftest import Group, GroupTier2


@pytest.mark.unit_test
def test_to_dict(test_group: Group):
    """Test the to_dict method produces a dictionary with the values as set."""
    d1 = test_group.to_dict(values_only=True)
    d2 = test_group.to_dict()
    assert d1 == {"a": False, "b": 1, "c": "test"}
    assert d2 == {
        "a": {"value": False, "properties": {}},
        "b": {"value": 1, "properties": {}},
        "c": {"value": "test", "properties": {}},
    }


@pytest.mark.unit_test
def test_set_config_item_to_value(test_group: Group):
    """Test the to_dict method produces a dictionary with the values as set."""
    test_group.a = "test"
    assert test_group.a.value == "test"


@pytest.mark.unit_test
def test_create_from_legacy(test_group: Group):
    """Test the group can be created using legacy config names."""
    d1 = {"legacy_a": True, "legacy_b": 2, "legacy_c": "set"}
    test_group.set_from_dict(config_dict=d1, legacy=True)

    d2 = test_group.to_dict(values_only=True)
    assert d2 == {"a": True, "b": 2, "c": "set"}


@pytest.mark.unit_test
def test_stringify(test_group: Group):
    """
    Test the group can represent itself as a string.

    The string should contain the groups class name,
    the validation failure reasons and exceptions together with the names and values of each of its elements.
    This should all be wrapped in parentheses.
    """
    s = test_group.stringify()
    assert (
        s
        == "Group(a=False, b=1, c=test, doc=None, validation=ConfigGroupValidation(passed=True, fail_reasons=[], fail_exceptions=[]))"
    )


@pytest.mark.unit_test
def test_repeat_item_validation(test_group: Group):
    """Test validating a group then modifying its items and re-validating."""
    test_group.a.value = "test"
    test_group.validate()

    test_group.a.value = 1
    test_group.validate()

    assert test_group.a.validation.fail_reasons == [
        "Value 1 is of type <class 'int'>, should be <class 'bool'>."
    ]


@pytest.mark.unit_test
def test_repeat_group_validation(multi_tier_test_group: GroupTier2):
    """Test validating a group then modifying its sub-groups and re-validating."""
    multi_tier_test_group.tier_1.bool.value = True
    multi_tier_test_group.tier_1.float.value = 2

    multi_tier_test_group.validate()

    multi_tier_test_group.tier_1.bool.value = True
    multi_tier_test_group.tier_1.float.value = -1

    multi_tier_test_group.validate()

    assert multi_tier_test_group.tier_1.validation.fail_reasons == [
        "test error tier 1 b"
    ]


@pytest.mark.unit_test
def test_multi_tier_group_validation_passed(multi_tier_test_group: GroupTier2):
    """Test the element and group validation works for groups with multiple nested tiers."""
    multi_tier_test_group.validate()
    assert multi_tier_test_group.validation.passed


@pytest.mark.unit_test
def test_multi_tier_group_tier_1_validation_group_failed(
    multi_tier_test_group: GroupTier2,
):
    """Test the element and group validation works for groups with multiple nested tiers."""
    multi_tier_test_group.tier_1.bool.value = True
    multi_tier_test_group.tier_1.float.value = 2

    multi_tier_test_group.validate()

    assert not multi_tier_test_group.validation.passed
    assert multi_tier_test_group.validation.group_passed
    assert not multi_tier_test_group.validation.elements_passed


@pytest.mark.unit_test
def test_multi_tier_group_tier_2_validation_group_failed(
    multi_tier_test_group: GroupTier2,
):
    """Test the element and group validation works for groups with multiple nested tiers."""
    multi_tier_test_group.bool.value = True
    multi_tier_test_group.int.value = 2

    multi_tier_test_group.validate()

    assert not multi_tier_test_group.validation.passed
    assert not multi_tier_test_group.validation.group_passed
    assert multi_tier_test_group.validation.elements_passed


@pytest.mark.unit_test
def test_multi_tier_group_tier_2_item_failed(multi_tier_test_group: GroupTier2):
    """Test the element and group validation works for groups with multiple nested tiers."""
    multi_tier_test_group.bool.value = "test"

    multi_tier_test_group.validate()

    assert not multi_tier_test_group.validation.passed
    assert multi_tier_test_group.validation.group_passed
    assert not multi_tier_test_group.validation.elements_passed


@pytest.mark.unit_test
def test_multi_tier_group_tier_1_item_failed(multi_tier_test_group: GroupTier2):
    """Test the element and group validation works for groups with multiple nested tiers."""
    multi_tier_test_group.tier_1.bool.value = "test"

    multi_tier_test_group.validate()

    assert not multi_tier_test_group.validation.passed
    assert multi_tier_test_group.validation.group_passed
    assert not multi_tier_test_group.validation.elements_passed


@pytest.mark.unit_test
def test_yaml_round_trip(test_group: Group, tmp_path: Path):
    """Test that the items can be stored in a yaml file and subsequently reloaded."""
    d1 = test_group.to_dict()

    test_group.to_yaml(tmp_path / "yaml_out.yaml")
    test_group.set_from_yaml(tmp_path / "yaml_out.yaml")

    d2 = test_group.to_dict()

    assert d1 == d2
