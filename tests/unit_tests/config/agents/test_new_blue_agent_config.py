import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.agents.new_blue_agent_config import Blue


@pytest.fixture
def default_blue() -> Blue:
    """Create a blue agent using the default config."""
    blue = Blue()
    blue.set_from_dict(get_default_config_dict()["blue"])
    return blue

def test_reconnect_isolate_config(default_blue: Blue):
    """Tests use isolate node while reconnect node is False."""
    default_blue.action_set.isolate_node.value = True
    default_blue.action_set.reconnect_node.value = False

    default_blue.validate()

    # assert that the error message is as expected
    assert (
        "Blue should be able to reconnect or isolate nodes if the other is true."
        in default_blue.action_set.validation.fail_reasons
    )

    default_blue.action_set.isolate_node.value = False
    default_blue.action_set.reconnect_node.value = True

    default_blue.validate()

    assert (
        "Blue should be able to reconnect or isolate nodes if the other is true."
        in default_blue.action_set.validation.fail_reasons
    )


def test_no_max_number_deceptive_nodes(default_blue: Blue):
    """Tests using deceptive nodes but there being 0 as the max number."""
    default_blue.action_set.deceptive_nodes.use.value = True
    default_blue.action_set.deceptive_nodes.max_number = 0

    default_blue.validate()
    # assert that the error message is as expected
    assert (
        "if the blue agent can use deceptive nodes then it must be able to create at least 1."
        in default_blue.action_set.deceptive_nodes.validation.fail_reasons
    )


def test_default_blue_from_legacy(default_blue: Blue):
    """Create a blue agent using the default config file."""
    blue = Blue()

    blue.set_from_dict(get_default_config_dict_legacy()["BLUE"], legacy=True)
    assert blue == default_blue
    assert blue.to_dict() == default_blue.to_dict()
