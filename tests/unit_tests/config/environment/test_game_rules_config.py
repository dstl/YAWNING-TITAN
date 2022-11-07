from typing import Dict, Any

import pytest

from tests.unit_tests.config.config_test_utils import read_yaml_file
from tests.unit_tests.config.environment import TEST_GAME_RULES_CONFIG_PATH
from yawning_titan.config.environment.game_rules_config import GameRulesConfig


def get_config_dict() -> Dict:
    return read_yaml_file(TEST_GAME_RULES_CONFIG_PATH)


def test_read_valid_config():
    game_rules = GameRulesConfig.create(get_config_dict())

    assert game_rules.gr_min_number_of_network_nodes == 18

    assert game_rules.gr_node_vuln_lower == 0.2

    assert game_rules.gr_node_vuln_upper == 0.8

    assert game_rules.gr_max_steps == 1000

    assert game_rules.gr_loss_total_compromise is False

    assert game_rules.gr_loss_pc_nodes_compromised is False

    assert game_rules.gr_loss_pc_node_compromised_pc == 0.8

    assert game_rules.gr_number_of_high_value_targets == 1

    assert game_rules.gr_loss_hvt is True

    assert game_rules.gr_loss_hvt_random_placement is False

    assert game_rules.gr_loss_hvt_furthest_away is True

    assert game_rules.gr_random_entry_nodes is True

    assert game_rules.gr_num_entry_nodes == 3

    assert game_rules.gr_prefer_central_entry is True

    assert game_rules.gr_prefer_edge_nodes is False

    assert game_rules.gr_grace_period == 0


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT
        ("node_vulnerability_lower_bound", True,
         "'node_vulnerability_lower_bound' needs to be of type: <class 'float'> or "
         "<class 'int'>"),
        ("node_vulnerability_upper_bound", True,
         "'node_vulnerability_upper_bound' needs to be of type: <class 'float'> or "
         "<class 'int'>"),
        ("percentage_of_nodes_compromised_equals_loss", True,
         "'percentage_of_nodes_compromised_equals_loss' needs to be of type: <class 'float'> or "
         "<class 'int'>"),
        # INT
        ("min_number_of_network_nodes", 0.5,
         "'min_number_of_network_nodes' needs to be of type: <class 'int'>"),
        ("max_steps", 0.5,
         "'max_steps' needs to be of type: <class 'int'>"),
        ("number_of_high_value_targets", 0.5,
         "'number_of_high_value_targets' needs to be of type: <class 'int'>"),
        ("number_of_entry_nodes", 0.5,
         "'number_of_entry_nodes' needs to be of type: <class 'int'>"),
        ("grace_period_length", 0.5,
         "'grace_period_length' needs to be of type: <class 'int'>"),
        # BOOLEAN
        ("lose_when_all_nodes_lost", 0.5,
         "'lose_when_all_nodes_lost' needs to be of type: <class 'bool'>"),
        ("lose_when_n_percent_of_nodes_lost", 0.5,
         "'lose_when_n_percent_of_nodes_lost' needs to be of type: <class 'bool'>"),
        ("lose_when_high_value_target_lost", 0.5,
         "'lose_when_high_value_target_lost' needs to be of type: <class 'bool'>"),
        ("choose_high_value_targets_placement_at_random", 0.5,
         "'choose_high_value_targets_placement_at_random' needs to be of type: <class 'bool'>"),
        ("choose_high_value_targets_furthest_away_from_entry", 0.5,
         "'choose_high_value_targets_furthest_away_from_entry' needs to be of type: <class 'bool'>"),
        ("choose_entry_nodes_randomly", 0.5,
         "'choose_entry_nodes_randomly' needs to be of type: <class 'bool'>"),
        ("prefer_central_nodes_for_entry_nodes", 0.5,
         "'prefer_central_nodes_for_entry_nodes' needs to be of type: <class 'bool'>"),
        ("prefer_edge_nodes_for_entry_nodes", 0.5,
         "'prefer_edge_nodes_for_entry_nodes' needs to be of type: <class 'bool'>"),
    ]
)
def test_invalid_config_type(config_item_to_test: str, config_value: Any, expected_err: str):
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
        ("node_vulnerability_lower_bound", -0.5,
         "'node_vulnerability_lower_bound' Needs to have a value greater than: 0 (inclusive)"),
        ("node_vulnerability_lower_bound", 1.1,
         "'node_vulnerability_lower_bound' Needs to have a value less than: 1 (inclusive)"),

        # MORE THAN OR EQUAL TO 0 BUT LESS THAN MIN NUM OF NODES
        ("number_of_high_value_targets", -1,
         "'number_of_high_value_targets' Needs to have a value greater than: 0 (inclusive)"),
        ("number_of_high_value_targets", 19,
         "'number_of_high_value_targets' Needs to have a value less than: 18 (inclusive)"),
        ("number_of_entry_nodes", -1,
         "'number_of_entry_nodes' Needs to have a value greater than: 0 (not inclusive)"),
        ("number_of_entry_nodes", 19,
         "'number_of_entry_nodes' Needs to have a value less than: 18 (inclusive)"),

        # BETWEEN 0 AND 100
        ("grace_period_length", -1,
         "'grace_period_length' Needs to have a value greater than: 0 (inclusive)"),
        ("grace_period_length", 101,
         "'grace_period_length' Needs to have a value less than: 100 (inclusive)"),

        # MAX STEPS
        ("max_steps", -1,
         "'max_steps' Needs to have a value greater than: 0 (not inclusive)"),
        ("max_steps", 10000001,
         "'max_steps' Needs to have a value less than: 10000000 (inclusive)"),
    ]
)
def test_invalid_config_range(config_item_to_test: str, config_value: Any, expected_err: str):
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        GameRulesConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err
