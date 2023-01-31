import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.game_modes.components.reset import Reset


@pytest.fixture
def default_reset() -> Reset:
    """Create a game rules instance using the default config."""
    reset = Reset()
    reset.set_from_dict(get_default_config_dict()["on_reset"])
    return reset


def test_default_reset_from_legacy(default_reset: Reset):
    """Create a reset instance using the default config file."""
    reset = Reset()

    reset.set_from_dict(get_default_config_dict_legacy()["RESET"], legacy=True)
    assert reset.to_dict() == default_reset.to_dict()
    assert reset == default_reset
