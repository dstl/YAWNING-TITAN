import pytest

from yawning_titan.config.toolbox.base.groups import ActionLikelihoodChanceGroup


@pytest.mark.unit_test
def test_action_likelihood_chance_not_used():
    """Test the ActionLikelihoodGroup when not used."""
    alc = ActionLikelihoodChanceGroup(use=False)

    assert alc.validation.passed
    assert alc.validation.group_passed


@pytest.mark.unit_test
def test_action_likelihood_chance_valid_used():
    """Test the ActionLikelihoodGroup when used and valid."""
    alc = ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=0.25)

    assert alc.validation.passed
    assert alc.validation.group_passed


@pytest.mark.unit_test
def test_action_likelihood_chance_group_fail_used():
    """Tests ActionLikelihoodGroup when the group validation passes but an item fails the group."""
    alc = ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=-5)

    assert alc.validation.passed
    assert not alc.validation.group_passed
