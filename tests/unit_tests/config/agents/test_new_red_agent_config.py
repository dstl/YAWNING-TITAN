import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.agents.new_red_agent_config import Red


@pytest.fixture
def default_red() -> Red:
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict()["red"])
    return red


def test_default_red_from_legacy(default_red: Red) -> Red:
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict_legacy()["RED"], legacy=True)
    import yaml
    print("G1",yaml.dump(red.to_dict(values_only=True)))
    print("G2",yaml.dump(default_red.to_dict(values_only=True)))
    assert red == default_red
    assert red.to_dict() == default_red.to_dict()
