import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.environment.new_game_rules_config import GameRules
from yawning_titan.exceptions import ConfigGroupValidationError


@pytest.fixture
def default_game_rules() -> GameRules:
    """Create a game rules instance using the default config."""
    game_rules = GameRules()
    game_rules.set_from_dict(get_default_config_dict()["game_rules"])
    return game_rules


@pytest.fixture
def game_rules() -> GameRules:
    """Create a game rules instance."""
    return GameRules()


def test_grace_period_longer_than_game_length(game_rules: GameRules):
    """Test that the grace period cannot exceed the length of the game."""
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


def test_default_game_mode_from_legacy(
    default_game_rules: GameRules, game_rules: GameRules
):
    """Create a game_rules instance using the default config file."""
    game_rules.set_from_dict(
        get_default_config_dict_legacy()["GAME_RULES"], legacy=True
    )
    assert game_rules.to_dict() == default_game_rules.to_dict()
    assert game_rules == default_game_rules
