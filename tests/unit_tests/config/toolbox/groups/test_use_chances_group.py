import pytest

from yawning_titan.config.toolbox.groups.core import ChanceGroup, UseChancesGroup


@pytest.mark.unit_test
def test_chance_group_not_used():
    """Test the UseChancesGroup when not used."""
    alc = UseChancesGroup(use=False)

    assert alc.validation.passed
    assert alc.validation.group_passed


@pytest.mark.unit_test
def test_chance_group_valid_used():
    """Test the UseChancesGroup when used and valid."""
    alc = UseChancesGroup(
        use=True, chance=ChanceGroup(standard_node=0.5, deceptive_node=0.6)
    )

    assert alc.validation.passed
    assert alc.validation.group_passed


@pytest.mark.unit_test
def test_chance_group_fail_used_item_fail():
    """Tests UseChancesGroup when the group validation passes but an item fails the group."""
    alc = UseChancesGroup(
        use="F", chance=ChanceGroup(standard_node=0.5, deceptive_node=0.6)
    )

    assert alc.validation.passed
    assert not alc.validation.group_passed


@pytest.mark.unit_test
def test_chance_group_fail_used_group_fail():
    """Tests UseChancesGroup when the group validation fails but item validation passes."""
    alc = UseChancesGroup(
        use=True, chance=ChanceGroup(standard_node=0.5, deceptive_node=0.5)
    )

    assert not alc.validation.passed
    assert alc.validation.group_passed
