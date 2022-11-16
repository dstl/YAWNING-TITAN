from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.environment.observation_space_config import (
    ObservationSpaceConfig,
)


def get_config_dict() -> Dict:
    """Return the Observation Space config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["OBSERVATION_SPACE"]


def test_read_valid_config():
    """Tests that a valid config can be created."""
    config_dict = get_config_dict()
    observations_space = ObservationSpaceConfig.create(config_dict)
    assert observations_space.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        (
            "compromised_status",
            "fail",
            "'compromised_status' needs to be of type: <class 'bool'>",
        ),
        (
            "vulnerabilities",
            "fail",
            "'vulnerabilities' needs to be of type: <class 'bool'>",
        ),
        (
            "node_connections",
            "fail",
            "'node_connections' needs to be of type: <class 'bool'>",
        ),
        (
            "average_vulnerability",
            "fail",
            "'average_vulnerability' needs to be of type: <class 'bool'>",
        ),
        (
            "graph_connectivity",
            "fail",
            "'graph_connectivity' needs to be of type: <class 'bool'>",
        ),
        (
            "attacking_nodes",
            "fail",
            "'attacking_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "attacked_nodes",
            "fail",
            "'attacked_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "special_nodes",
            "fail",
            "'special_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "red_agent_skill",
            "fail",
            "'red_agent_skill' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests an invalid config type."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        ObservationSpaceConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


def test_at_least_one_option_selected():
    """Tests at least one observation space option being selected requirement."""
    with pytest.raises(ValueError) as err_info:
        ObservationSpaceConfig.create(
            {
                "compromised_status": False,
                "vulnerabilities": False,
                "node_connections": False,
                "average_vulnerability": False,
                "graph_connectivity": False,
                "attacking_nodes": False,
                "attacked_nodes": False,
                "special_nodes": False,
                "red_agent_skill": False,
            }
        )

    # assert that the error message is as expected
    assert (
        err_info.value.args[0]
        == "At least one option from OBSERVATION_SPACE must be enabled. The "
        "observation space must contain at least one item "
    )
