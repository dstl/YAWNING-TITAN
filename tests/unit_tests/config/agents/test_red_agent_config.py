from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.red_agent_config import RedAgentConfig


def get_config_dict() -> Dict:
    """Return the RED config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["RED"]


def test_read_valid_config():
    """Tests creation of `RedAgent` with valid config."""
    config_dict = get_config_dict()
    red_agent = RedAgentConfig.create(config_dict)
    assert red_agent.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT TYPES
        (
            "chance_for_red_to_spread",
            True,
            "'chance_for_red_to_spread' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_for_red_to_random_compromise",
            True,
            "'chance_for_red_to_random_compromise' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "red_skill",
            True,
            "'red_skill' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "spread_action_likelihood",
            True,
            "'spread_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "random_infect_action_likelihood",
            True,
            "'random_infect_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "basic_attack_action_likelihood",
            True,
            "'basic_attack_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "do_nothing_action_likelihood",
            True,
            "'do_nothing_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "move_action_likelihood",
            True,
            "'move_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_spread_to_connected_node",
            True,
            "'chance_to_spread_to_connected_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_spread_to_unconnected_node",
            True,
            "'chance_to_spread_to_unconnected_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        # INT TYPES
        (
            "zero_day_start_amount",
            True,
            "'zero_day_start_amount' needs to be of type: <class 'int'>",
        ),
        (
            "days_required_for_zero_day",
            True,
            "'days_required_for_zero_day' needs to be of type: <class 'int'>",
        ),
        # BOOLEANS
        (
            "red_uses_skill",
            "fail",
            "'red_uses_skill' needs to be of type: <class 'bool'>",
        ),
        (
            "red_ignores_defences",
            "fail",
            "'red_ignores_defences' needs to be of type: <class 'bool'>",
        ),
        (
            "red_always_succeeds",
            "fail",
            "'red_always_succeeds' needs to be of type: <class 'bool'>",
        ),
        (
            "red_can_only_attack_from_red_agent_node",
            "fail",
            "'red_can_only_attack_from_red_agent_node' needs to be of type: <class 'bool'>",
        ),
        (
            "red_can_attack_from_any_red_node",
            "fail",
            "'red_can_attack_from_any_red_node' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_spread_action",
            "fail",
            "'red_uses_spread_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_random_infect_action",
            "fail",
            "'red_uses_random_infect_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_zero_day_action",
            "fail",
            "'red_uses_zero_day_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_basic_attack_action",
            "fail",
            "'red_uses_basic_attack_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_do_nothing_action",
            "fail",
            "'red_uses_do_nothing_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_uses_move_action",
            "fail",
            "'red_uses_move_action' needs to be of type: <class 'bool'>",
        ),
        (
            "red_chooses_target_at_random",
            "fail",
            "'red_chooses_target_at_random' needs to be of type: <class 'bool'>",
        ),
        (
            "red_prioritises_connected_nodes",
            "fail",
            "'red_prioritises_connected_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "red_prioritises_un_connected_nodes",
            "fail",
            "'red_prioritises_un_connected_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "red_prioritises_vulnerable_nodes",
            "fail",
            "'red_prioritises_vulnerable_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "red_prioritises_resilient_nodes",
            "fail",
            "'red_prioritises_resilient_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "red_can_naturally_spread",
            "fail",
            "'red_can_naturally_spread' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation of `RedAgent` with invalid data type."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        RedAgentConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # BETWEEN 0 and 1
        ("red_skill", 2, "'red_skill' Needs to have a value less than: 1 (inclusive)"),
        (
            "red_skill",
            -1,
            "'red_skill' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_for_red_to_spread",
            2,
            "'chance_for_red_to_spread' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_for_red_to_spread",
            -1,
            "'chance_for_red_to_spread' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_for_red_to_random_compromise",
            2,
            "'chance_for_red_to_random_compromise' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_for_red_to_random_compromise",
            -1,
            "'chance_for_red_to_random_compromise' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_spread_to_connected_node",
            2,
            "'chance_to_spread_to_connected_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_spread_to_connected_node",
            -1,
            "'chance_to_spread_to_connected_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_spread_to_unconnected_node",
            2,
            "'chance_to_spread_to_unconnected_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_spread_to_unconnected_node",
            -1,
            "'chance_to_spread_to_unconnected_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        # GREATER THAN 0
        (
            "spread_action_likelihood",
            -1,
            "'spread_action_likelihood' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "random_infect_action_likelihood",
            -1,
            "'random_infect_action_likelihood' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "basic_attack_action_likelihood",
            -1,
            "'basic_attack_action_likelihood' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "do_nothing_action_likelihood",
            -1,
            "'do_nothing_action_likelihood' Needs to have a value greater than: 0 (not inclusive)",
        ),
        (
            "move_action_likelihood",
            -1,
            "'move_action_likelihood' Needs to have a value greater than: 0 (not inclusive)",
        ),
        # GREATER THAN OR EQUAL TO 0
        (
            "zero_day_start_amount",
            -1,
            "'zero_day_start_amount' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "days_required_for_zero_day",
            -1,
            "'days_required_for_zero_day' Needs to have a value greater than: 0 (inclusive)",
        ),
    ],
)
def test_invalid_config_range(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation of `RedAgent` with invalid config."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        RedAgentConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err
