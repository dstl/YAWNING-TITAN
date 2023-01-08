import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.environment.new_observation_space_config import (
    ObservationSpace,
)


@pytest.fixture
def default_observation_space() -> ObservationSpace:
    """Create an observation_space instance using the default config."""
    observation_space = ObservationSpace()
    observation_space.set_from_dict(get_default_config_dict()["blue_can_observe"])
    return observation_space


def test_default_observation_space_from_legacy(
    default_observation_space: ObservationSpace,
):
    """Create a observation_space instance using the default config file."""
    observation_space = ObservationSpace()

    observation_space.set_from_dict(
        get_default_config_dict_legacy()["OBSERVATION_SPACE"], legacy=True
    )
    assert observation_space.to_dict() == default_observation_space.to_dict()
    assert observation_space == default_observation_space
