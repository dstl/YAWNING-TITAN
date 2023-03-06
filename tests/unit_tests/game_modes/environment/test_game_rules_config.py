import pytest

from tests.conftest import not_raises
from yawning_titan.exceptions import ConfigGroupValidationError
from yawning_titan.game_modes.components.game_rules import GameRules


@pytest.fixture
def default_game_rules(default_game_mode) -> GameRules:
    """Get game_rules from default game mode."""
    return default_game_mode.game_rules


@pytest.mark.unit_test
def test_grace_period_longer_than_game_length():
    """Test that the grace period cannot exceed the length of the game."""
    game_rules = GameRules()
    game_rules.grace_period_length.value = 100
    game_rules.max_steps.value = 50

    game_rules.validate()

    assert not game_rules.validation.group_passed
    assert (
        "The grace period cannot be the entire length of the game"
        in game_rules.validation.fail_reasons
    )

    with pytest.raises(ConfigGroupValidationError):
        raise game_rules.validation.fail_exceptions[0]  #


@pytest.mark.unit_test
def test_default_game_rules_from_legacy(
    default_game_rules: GameRules, legacy_default_game_mode_dict
):
    """Create a game_rules instance using the default config file."""
    game_rules = GameRules()

    with not_raises(Exception):
        game_rules.set_from_dict(
            legacy_default_game_mode_dict["GAME_RULES"], legacy=True
        )
