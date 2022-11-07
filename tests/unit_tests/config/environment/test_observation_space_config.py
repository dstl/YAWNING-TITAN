from typing import Dict, Any

import pytest

from tests.unit_tests.config.config_test_utils import read_yaml_file
from tests.unit_tests.config.environment import TEST_OBSERVATION_SPACE_CONFIG_PATH
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig


def get_config_dict() -> Dict:
    return read_yaml_file(TEST_OBSERVATION_SPACE_CONFIG_PATH)


def test_read_valid_config():
    obs_space = ObservationSpaceConfig.create(get_config_dict())

    assert obs_space.obs_compromised_status is True

    assert obs_space.obs_node_vuln_status is True

    assert obs_space.obs_node_connections is True

    assert obs_space.obs_avg_vuln is False

    assert obs_space.obs_graph_connectivity is True

    assert obs_space.obs_attack_sources is True

    assert obs_space.obs_attack_targets is True

    assert obs_space.obs_special_nodes is True

    assert obs_space.obs_red_agent_skill is True


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        ("compromised_status", "fail",
         "'compromised_status' needs to be of type: <class 'bool'>"),
        ("vulnerabilities", "fail",
         "'vulnerabilities' needs to be of type: <class 'bool'>"),
        ("node_connections", "fail",
         "'node_connections' needs to be of type: <class 'bool'>"),
        ("average_vulnerability", "fail",
         "'average_vulnerability' needs to be of type: <class 'bool'>"),
        ("graph_connectivity", "fail",
         "'graph_connectivity' needs to be of type: <class 'bool'>"),
        ("attacking_nodes", "fail",
         "'attacking_nodes' needs to be of type: <class 'bool'>"),
        ("attacked_nodes", "fail",
         "'attacked_nodes' needs to be of type: <class 'bool'>"),
        ("special_nodes", "fail",
         "'special_nodes' needs to be of type: <class 'bool'>"),
        ("red_agent_skill", "fail",
         "'red_agent_skill' needs to be of type: <class 'bool'>"),
    ]
)
def test_invalid_config_type(config_item_to_test: str, config_value: Any, expected_err: str):
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        ObservationSpaceConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


def test_at_least_one_option_selected():
    with pytest.raises(ValueError) as err_info:
        ObservationSpaceConfig.create({
            "compromised_status": False,
            "vulnerabilities": False,
            "node_connections": False,
            "average_vulnerability": False,
            "graph_connectivity": False,
            "attacking_nodes": False,
            "attacked_nodes": False,
            "special_nodes": False,
            "red_agent_skill": False
        })

    # assert that the error message is as expected
    assert err_info.value.args[0] == "At least one option from OBSERVATION_SPACE must be enabled. The observation space must contain at least one item"
