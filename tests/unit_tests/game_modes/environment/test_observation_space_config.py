import pytest

from tests.conftest import not_raises
from yawning_titan.game_modes.components.observation_space import ObservationSpace


@pytest.fixture
def default_observation_space(default_game_mode) -> ObservationSpace:
    """Get observation_space from default game mode."""
    return default_game_mode.blue_can_observe


@pytest.mark.unit_test
def test_default_observation_space_from_legacy(
    default_observation_space: ObservationSpace, legacy_default_game_mode_dict
):
    """Create a observation_space instance using the default config file."""
    observation_space = ObservationSpace()

    with not_raises(Exception):
        observation_space.set_from_dict(
            legacy_default_game_mode_dict["OBSERVATION_SPACE"]
        )
