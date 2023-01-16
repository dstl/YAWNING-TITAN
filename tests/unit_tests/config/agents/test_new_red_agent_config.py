import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.agents.new_red_agent_config import Red, TargetNodeGroup
from yawning_titan.exceptions import ConfigGroupValidationError


@pytest.fixture
def default_red() -> Red:
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict()["red"])
    return red


# -- Tier 0 groups ---


def test_setting_target_without_using():
    """Test setting a target node for red but not using this target mechanism."""
    target = TargetNodeGroup(use=False, target="2")

    assert not target.validation.group_passed
    assert (
        "Red is set to target 2, if the target is set to a specific node then the element must have `used` set to True"
        in target.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise target.validation.fail_exceptions[0]


# --- Tier 2 group ---


def test_targeting_vulnerable_nodes_when_defences_are_ignored():
    """Test targeting vulnerable nodes while also ignoring defences."""
    red = Red()

    red.agent_attack.ignores_defences.value = True
    red.target_mechanism.prioritise_resilient_nodes.value = True

    red.validate()

    assert not red.validation.group_passed

    assert (
        "If the red agent ignores defences then targeting based on this trait is impossible as it is ignored."
        in red.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise red.validation.fail_exceptions[0]


def test_default_red_from_legacy(default_red: Red):
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict_legacy()["RED"], legacy=True)

    assert red == default_red
    assert red.to_dict() == default_red.to_dict()
