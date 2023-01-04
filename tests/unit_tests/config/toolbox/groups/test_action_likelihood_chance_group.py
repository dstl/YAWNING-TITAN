import pytest

from yawning_titan.config.toolbox.groups.core import ActionLikelihoodChanceGroup
from yawning_titan.exceptions import ConfigGroupValidationError

@pytest.mark.unit_test
def test_action_likelihood_chance_not_used():
    """Test the ActionLikelihoodGroup when not used."""
    alc = ActionLikelihoodChanceGroup(use=False)
    assert alc.validation.passed
    assert alc.validation.group_passed

@pytest.mark.unit_test
def test_action_likelihood_chance_used_chance_not_set():
    """Test the ActionLikelihoodGroup when used but chance not set."""
    alc = ActionLikelihoodChanceGroup(use=True, likelihood=0.5)
    assert not alc.validation.passed
    with pytest.raises(ConfigGroupValidationError):
        raise alc.validation.fail_exceptions[0]

@pytest.mark.unit_test
def test_action_likelihood_chance_used_likelihood_not_set():
    """Test the ActionLikelihoodGroup when used but likelihood not set."""
    alc = ActionLikelihoodChanceGroup(use=True, chance=0.25)
    assert not alc.validation.passed
    with pytest.raises(ConfigGroupValidationError):
        raise alc.validation.fail_exceptions[0]

@pytest.mark.unit_test
def test_action_likelihood_chance_used_chance_and_likelihood_not_set():
    """Test the ActionLikelihoodGroup when used but chance and likelihood not set."""
    alc = ActionLikelihoodChanceGroup(use=True)
    assert not alc.validation.passed
    with pytest.raises(ConfigGroupValidationError):
        raise alc.validation.fail_exceptions[0]

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

