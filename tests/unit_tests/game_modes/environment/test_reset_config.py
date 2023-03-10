import pytest

from tests.conftest import not_raises
from yawning_titan.game_modes.components.reset import Reset


@pytest.fixture
def default_reset(default_game_mode) -> Reset:
    """Create a game rules instance using the default config."""
    return default_game_mode.on_reset


@pytest.mark.unit_test
def test_default_reset_from_legacy(default_reset: Reset, legacy_default_game_mode_dict):
    """Create a reset instance using the default config file."""
    reset = Reset()
    with not_raises(Exception):
        reset.set_from_dict(legacy_default_game_mode_dict["RESET"], legacy=True)
