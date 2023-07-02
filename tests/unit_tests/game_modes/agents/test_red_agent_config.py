import pytest

from tests.conftest import not_raises
from yawning_titan.exceptions import ConfigGroupValidationError
from yawning_titan.game_modes.components.red_agent import Red, TargetNodeGroup


@pytest.fixture
def default_red(default_game_mode) -> Red:
    """Get red from default game mode."""
    return default_game_mode.red


# -- Tier 0 groups ---


@pytest.mark.unit_test
def test_setting_target_without_using():
    """Test setting a target node for red but not using this target mechanism."""
    target = TargetNodeGroup(use=False, target="2")

    assert not target.validation.group_passed
    assert (
        "Red is set to target 2, if the red agent is set to a specific node then the element must have `used` set to True"
        in target.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise target.validation.fail_exceptions[0]


# --- Tier 2 group ---


@pytest.mark.unit_test
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


@pytest.mark.unit_test
def test_default_red_from_legacy(default_red: Red, legacy_default_game_mode_dict):
    """Create a red agent using the default config file."""
    red = Red()

    with not_raises(Exception):
        red.set_from_dict(legacy_default_game_mode_dict["RED"], legacy=True)
