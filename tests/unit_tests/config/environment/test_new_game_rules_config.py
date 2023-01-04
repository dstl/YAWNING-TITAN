import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.environment.new_game_rules_config import GameRules

@pytest.fixture
def default_game_rules() -> GameRules:
    """Create a game rules instance using the default config."""
    game_rules = GameRules()
    game_rules.set_from_dict(get_default_config_dict()["game_rules"])
    return game_rules

def test_default_game_mode_from_legacy(default_game_rules: GameRules):
    """Create a game_rules instance using the default config file."""
    game_rules = GameRules()

    game_rules.set_from_dict(get_default_config_dict_legacy()["GAME_RULES"], legacy=True)
    assert game_rules.to_dict() == default_game_rules.to_dict()
    assert game_rules == default_game_rules