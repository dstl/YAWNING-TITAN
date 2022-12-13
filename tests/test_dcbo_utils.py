from typing import List

import pytest

from yawning_titan.integrations.dcbo.utils import init_dcbo_agent


@pytest.mark.parametrize(("probabs"), [([0.8, 0.3]), ([100, 20000]), ([0.2, 0.3])])
def test_init_dcbo_agent_assertion_error(probabs: List[float]):
    """
    Test to ensure that when two initial probability values that are either less than or greater than 1 raise AssertionError.

    Args:
        probabs: A pair of probability values
    """
    with pytest.raises(ValueError):
        init_dcbo_agent(probabs)


def test_base_dcbo_agent():
    """Test to check that the default pair of action probabilities are created correctly."""
    agent = init_dcbo_agent(None)
    assert agent.probabilities == [0.5, 0.5]


@pytest.mark.parametrize(
    ("probabs"),
    [([0.8, 0.2]), ([0.3, 0.7]), ([0.1, 0.9]), ([0.75, 0.25]), ([0.34, 0.66])],
)
def test_dcbo_agent_with_initial_probabs(probabs):
    """
    Test to check that when a pair of action probabilities are provided that sum to 1, they are created correctly.

    Args:
        probabs: A pair of probability values that equal 1
    """
    agent = init_dcbo_agent(probabs)
    assert agent.probabilities == probabs
