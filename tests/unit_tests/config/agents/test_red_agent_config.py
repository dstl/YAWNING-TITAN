from typing import Dict, Any

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.red_agent_config import RedAgentConfig


def get_config_dict() -> Dict:
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["RED"]


def test_read_valid_config():
    red_agent = RedAgentConfig.create(get_config_dict())

    # red_skill
    assert red_agent.red_skill == 0.5

    # red_uses_skill
    assert red_agent.red_use_skill is True

    # red_ignores_defences
    assert red_agent.red_ignore_defences is False

    # red_always_succeeds
    assert red_agent.red_always_succeeds is False

    # red_can_only_attack_from_red_agent_node
    assert red_agent.red_attack_from_current_position is False

    # red_can_attack_from_any_red_node
    assert red_agent.red_attack_from_any_node is True

    # red_can_naturally_spread
    assert red_agent.red_naturally_spread is True

    # chance_to_spread_to_connected_node
    assert red_agent.red_chance_to_spread_to_connected_node == 0.01

    # chance_to_spread_to_unconnected_node
    assert red_agent.red_chance_to_spread_to_unconnected_node == 0.005

    # red_uses_spread_action
    assert red_agent.red_spread_action is False

    # spread_action_likelihood
    assert red_agent.red_spread_action_likelihood == 1

    # chance_for_red_to_spread
    assert red_agent.red_spread_success_chance == 0.1

    # red_uses_random_infect_action
    assert red_agent.red_random_infection_action is False

    # random_infect_action_likelihood
    assert red_agent.red_random_infection_likelihood == 1

    # chance_for_red_to_random_compromise
    assert red_agent.red_random_infection_success_chance == 0.1

    # red_uses_basic_attack_action
    assert red_agent.red_basic_attack_action is True

    # basic_attack_action_likelihood
    assert red_agent.red_basic_attack_likelihood == 1

    # red_uses_do_nothing_action
    assert red_agent.red_do_nothing_action is True

    # do_nothing_action_likelihood
    assert red_agent.red_do_nothing_likelihood == 1

    # red_uses_move_action
    assert red_agent.red_move_action is False

    # move_action_likelihood
    assert red_agent.red_move_action_likelihood == 1

    # red_uses_zero_day_action
    assert red_agent.red_zero_day_action is True

    # zero_day_start_amount
    assert red_agent.red_zero_day_start_amount == 1

    # days_required_for_zero_day
    assert red_agent.red_zero_day_days_required_to_create == 10

    # red_chooses_target_at_random
    assert red_agent.red_targeting_random is False

    # red_prioritises_connected_nodes
    assert red_agent.red_targeting_prioritise_connected_nodes is True

    # red_prioritises_un_connected_nodes
    assert red_agent.red_targeting_prioritise_unconnected_nodes is False

    # red_prioritises_vulnerable_nodes
    assert red_agent.red_targeting_prioritise_vulnerable_nodes is False

    # red_prioritises_resilient_nodes
    assert red_agent.red_targeting_prioritise_resilient_nodes is False


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT TYPES
        ("chance_for_red_to_spread", True,
         "'chance_for_red_to_spread' needs to be of type: <class 'int'> or <class 'float'>"),
        ("chance_for_red_to_random_compromise", True,
         "'chance_for_red_to_random_compromise' needs to be of type: <class 'int'> or <class 'float'>"),
        ("red_skill", True,
         "'red_skill' needs to be of type: <class 'int'> or <class 'float'>"),
        ("spread_action_likelihood", True,
         "'spread_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>"),
        ("random_infect_action_likelihood", True,
         "'random_infect_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>"),
        ("basic_attack_action_likelihood", True,
         "'basic_attack_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>"),
        ("do_nothing_action_likelihood", True,
         "'do_nothing_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>"),
        ("move_action_likelihood", True,
         "'move_action_likelihood' needs to be of type: <class 'int'> or <class 'float'>"),
        ("chance_to_spread_to_connected_node", True,
         "'chance_to_spread_to_connected_node' needs to be of type: <class 'int'> or <class 'float'>"),
        ("chance_to_spread_to_unconnected_node", True,
         "'chance_to_spread_to_unconnected_node' needs to be of type: <class 'int'> or <class 'float'>"),

        # INT TYPES
        ("zero_day_start_amount", True,
         "'zero_day_start_amount' needs to be of type: <class 'int'>"),
        ("days_required_for_zero_day", True,
         "'days_required_for_zero_day' needs to be of type: <class 'int'>"),

        # BOOLEANS
        ("red_uses_skill", "fail",
         "'red_uses_skill' needs to be of type: <class 'bool'>"),
        ("red_ignores_defences", "fail",
         "'red_ignores_defences' needs to be of type: <class 'bool'>"),
        ("red_always_succeeds", "fail",
         "'red_always_succeeds' needs to be of type: <class 'bool'>"),
        ("red_can_only_attack_from_red_agent_node", "fail",
         "'red_can_only_attack_from_red_agent_node' needs to be of type: <class 'bool'>"),
        ("red_can_attack_from_any_red_node", "fail",
         "'red_can_attack_from_any_red_node' needs to be of type: <class 'bool'>"),
        ("red_uses_spread_action", "fail",
         "'red_uses_spread_action' needs to be of type: <class 'bool'>"),
        ("red_uses_random_infect_action", "fail",
         "'red_uses_random_infect_action' needs to be of type: <class 'bool'>"),
        ("red_uses_zero_day_action", "fail",
         "'red_uses_zero_day_action' needs to be of type: <class 'bool'>"),
        ("red_uses_basic_attack_action", "fail",
         "'red_uses_basic_attack_action' needs to be of type: <class 'bool'>"),
        ("red_uses_do_nothing_action", "fail",
         "'red_uses_do_nothing_action' needs to be of type: <class 'bool'>"),
        ("red_uses_move_action", "fail",
         "'red_uses_move_action' needs to be of type: <class 'bool'>"),
        ("red_chooses_target_at_random", "fail",
         "'red_chooses_target_at_random' needs to be of type: <class 'bool'>"),
        ("red_prioritises_connected_nodes", "fail",
         "'red_prioritises_connected_nodes' needs to be of type: <class 'bool'>"),
        ("red_prioritises_un_connected_nodes", "fail",
         "'red_prioritises_un_connected_nodes' needs to be of type: <class 'bool'>"),
        ("red_prioritises_vulnerable_nodes", "fail",
         "'red_prioritises_vulnerable_nodes' needs to be of type: <class 'bool'>"),
        ("red_prioritises_resilient_nodes", "fail",
         "'red_prioritises_resilient_nodes' needs to be of type: <class 'bool'>"),
        ("red_can_naturally_spread", "fail",
         "'red_can_naturally_spread' needs to be of type: <class 'bool'>")
    ]
)
def test_invalid_config_type(config_item_to_test: str, config_value: Any, expected_err: str):
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
        ("red_skill", 2,
         "'red_skill' Needs to have a value less than: 1 (inclusive)"),
        ("red_skill", -1,
         "'red_skill' Needs to have a value greater than: 0 (inclusive)"),
        ("chance_for_red_to_spread", 2,
         "'chance_for_red_to_spread' Needs to have a value less than: 1 (inclusive)"),
        ("chance_for_red_to_spread", -1,
         "'chance_for_red_to_spread' Needs to have a value greater than: 0 (inclusive)"),
        ("chance_for_red_to_random_compromise", 2,
         "'chance_for_red_to_random_compromise' Needs to have a value less than: 1 (inclusive)"),
        ("chance_for_red_to_random_compromise", -1,
         "'chance_for_red_to_random_compromise' Needs to have a value greater than: 0 (inclusive)"),
        ("chance_to_spread_to_connected_node", 2,
         "'chance_to_spread_to_connected_node' Needs to have a value less than: 1 (inclusive)"),
        ("chance_to_spread_to_connected_node", -1,
         "'chance_to_spread_to_connected_node' Needs to have a value greater than: 0 (inclusive)"),
        ("chance_to_spread_to_unconnected_node", 2,
         "'chance_to_spread_to_unconnected_node' Needs to have a value less than: 1 (inclusive)"),
        ("chance_to_spread_to_unconnected_node", -1,
         "'chance_to_spread_to_unconnected_node' Needs to have a value greater than: 0 (inclusive)"),

        # GREATER THAN 0
        ("spread_action_likelihood", -1,
         "'spread_action_likelihood' Needs to have a value greater than: 0 (not inclusive)"),
        ("random_infect_action_likelihood", -1,
         "'random_infect_action_likelihood' Needs to have a value greater than: 0 (not inclusive)"),
        ("basic_attack_action_likelihood", -1,
         "'basic_attack_action_likelihood' Needs to have a value greater than: 0 (not inclusive)"),
        ("do_nothing_action_likelihood", -1,
         "'do_nothing_action_likelihood' Needs to have a value greater than: 0 (not inclusive)"),
        ("move_action_likelihood", -1,
         "'move_action_likelihood' Needs to have a value greater than: 0 (not inclusive)"),

        # GREATER THAN OR EQUAL TO 0
        ("zero_day_start_amount", -1,
         "'zero_day_start_amount' Needs to have a value greater than: 0 (inclusive)"),
        ("days_required_for_zero_day", -1,
         "'days_required_for_zero_day' Needs to have a value greater than: 0 (inclusive)"),

    ]
)
def test_invalid_config_range(config_item_to_test: str, config_value: Any, expected_err: str):
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        RedAgentConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err
