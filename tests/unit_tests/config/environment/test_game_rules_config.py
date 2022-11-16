from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.environment.game_rules_config import GameRulesConfig


def get_config_dict() -> Dict:
    """Return the GAME_RULES config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["GAME_RULES"]


def test_read_valid_config():
    """Tests creation of `GameRulesConfig` from valid config."""
    config_dict = get_config_dict()
    game_rules = GameRulesConfig.create(config_dict)
    assert game_rules.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT
        (
            "node_vulnerability_lower_bound",
            True,
            "'node_vulnerability_lower_bound' needs to be of type: <class 'float'> or "
            "<class 'int'>",
        ),
        (
            "node_vulnerability_upper_bound",
            True,
            "'node_vulnerability_upper_bound' needs to be of type: <class 'float'> or "
            "<class 'int'>",
        ),
        (
            "percentage_of_nodes_compromised_equals_loss",
            True,
            "'percentage_of_nodes_compromised_equals_loss' needs to be of type: <class 'float'> or "
            "<class 'int'>",
        ),
        # INT
        (
            "min_number_of_network_nodes",
            0.5,
            "'min_number_of_network_nodes' needs to be of type: <class 'int'>",
        ),
        ("max_steps", 0.5, "'max_steps' needs to be of type: <class 'int'>"),
        (
            "number_of_high_value_nodes",
            0.5,
            "'number_of_high_value_nodes' needs to be of type: <class 'int'>",
        ),
        (
            "number_of_entry_nodes",
            0.5,
            "'number_of_entry_nodes' needs to be of type: <class 'int'>",
        ),
        (
            "grace_period_length",
            0.5,
            "'grace_period_length' needs to be of type: <class 'int'>",
        ),
        # BOOLEAN
        (
            "lose_when_all_nodes_lost",
            0.5,
            "'lose_when_all_nodes_lost' needs to be of type: <class 'bool'>",
        ),
        (
            "lose_when_n_percent_of_nodes_lost",
            0.5,
            "'lose_when_n_percent_of_nodes_lost' needs to be of type: <class 'bool'>",
        ),
        (
            "lose_when_high_value_node_lost",
            0.5,
            "'lose_when_high_value_node_lost' needs to be of type: <class 'bool'>",
        ),
        (
            "lose_when_target_node_lost",
            0.5,
            "'lose_when_target_node_lost' needs to be of type: <class 'bool'>",
        ),
        (
            "choose_high_value_nodes_placement_at_random",
            0.5,
            "'choose_high_value_nodes_placement_at_random' needs to be of type: <class 'bool'>",
        ),
        (
            "choose_high_value_nodes_furthest_away_from_entry",
            0.5,
            "'choose_high_value_nodes_furthest_away_from_entry' needs to be of type: <class 'bool'>",
        ),
        (
            "choose_entry_nodes_randomly",
            0.5,
            "'choose_entry_nodes_randomly' needs to be of type: <class 'bool'>",
        ),
        (
            "prefer_central_nodes_for_entry_nodes",
            0.5,
            "'prefer_central_nodes_for_entry_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "prefer_edge_nodes_for_entry_nodes",
            0.5,
            "'prefer_edge_nodes_for_entry_nodes' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests invalid types."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        GameRulesConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # BETWEEN 0 AND 1
        (
            "node_vulnerability_lower_bound",
            -0.5,
            "'node_vulnerability_lower_bound' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "node_vulnerability_lower_bound",
            1.1,
            "'node_vulnerability_lower_bound' Needs to have a value less than: 1 (inclusive)",
        ),
        # MORE THAN OR EQUAL TO 0 BUT LESS THAN MIN NUM OF NODES
        (
            "number_of_high_value_nodes",
            -1,
            "'number_of_high_value_nodes' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "number_of_high_value_nodes",
            19,
            "'number_of_high_value_nodes' Needs to have a value less than: 18 (inclusive)",
        ),
        (
            "number_of_entry_nodes",
            -1,
            "'number_of_entry_nodes' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "number_of_entry_nodes",
            19,
            "'number_of_entry_nodes' Needs to have a value less than: 18 (inclusive)",
        ),
        # BETWEEN 0 AND 100
        (
            "grace_period_length",
            -1,
            "'grace_period_length' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "grace_period_length",
            101,
            "'grace_period_length' Needs to have a value less than: 100 (inclusive)",
        ),
        # MAX STEPS
        (
            "max_steps",
            -1,
            "'max_steps' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "max_steps",
            10000001,
            "'max_steps' Needs to have a value less than: 10000000 (inclusive)",
        ),
    ],
)
def test_invalid_config_range(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation using invalid values."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        GameRulesConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err
