from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig


def get_config_dict() -> Dict:
    """Return the BLUE config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["BLUE"]


def test_read_valid_config():
    """Tests creation of `BlueAgentConfig` with valid config."""
    config_dict = get_config_dict()
    blue_agent = BlueAgentConfig.create(config_dict)
    assert blue_agent.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT TYPES
        (
            "chance_to_immediately_discover_intrusion",
            True,
            "'chance_to_immediately_discover_intrusion' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_intrusion_on_scan",
            True,
            "'chance_to_discover_intrusion_on_scan' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "vulnerability_change_during_node_patch",
            True,
            "'vulnerability_change_during_node_patch' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_failed_attack",
            True,
            "'chance_to_discover_failed_attack' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_known",
            True,
            "'chance_to_discover_succeeded_attack_compromise_known' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_not_known",
            True,
            "'chance_to_discover_succeeded_attack_compromise_not_known' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_immediately_discover_intrusion_deceptive_node",
            True,
            "'chance_to_immediately_discover_intrusion_deceptive_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_intrusion_on_scan_deceptive_node",
            True,
            "'chance_to_discover_intrusion_on_scan_deceptive_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_failed_attack_deceptive_node",
            True,
            "'chance_to_discover_failed_attack_deceptive_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "chance_to_discover_succeeded_attack_deceptive_node",
            True,
            "'chance_to_discover_succeeded_attack_deceptive_node' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "vulnerability_change_during_node_patch",
            True,
            "'vulnerability_change_during_node_patch' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        # INT TYPE
        (
            "max_number_deceptive_nodes",
            True,
            "'max_number_deceptive_nodes' needs to be of type: <class 'int'>",
        ),
        # BOOLEANS
        (
            "making_node_safe_modifies_vulnerability",
            "fail",
            "'making_node_safe_modifies_vulnerability' needs to be of type: <class 'bool'>",
        ),
        (
            "making_node_safe_gives_random_vulnerability",
            "fail",
            "'making_node_safe_gives_random_vulnerability' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_reduce_vulnerability",
            "fail",
            "'blue_uses_reduce_vulnerability' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_restore_node",
            "fail",
            "'blue_uses_restore_node' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_make_node_safe",
            "fail",
            "'blue_uses_make_node_safe' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_scan",
            "fail",
            "'blue_uses_scan' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_isolate_node",
            "fail",
            "'blue_uses_isolate_node' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_reconnect_node",
            "fail",
            "'blue_uses_reconnect_node' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_do_nothing",
            "fail",
            "'blue_uses_do_nothing' needs to be of type: <class 'bool'>",
        ),
        (
            "blue_uses_deceptive_nodes",
            "fail",
            "'blue_uses_deceptive_nodes' needs to be of type: <class 'bool'>",
        ),
        (
            "can_discover_failed_attacks",
            "fail",
            "'can_discover_failed_attacks' needs to be of type: <class 'bool'>",
        ),
        (
            "can_discover_succeeded_attacks_if_compromise_is_discovered",
            "fail",
            "'can_discover_succeeded_attacks_if_compromise_is_discovered' needs to be of type: <class 'bool'>",
        ),
        (
            "can_discover_succeeded_attacks_if_compromise_is_not_discovered",
            "fail",
            "'can_discover_succeeded_attacks_if_compromise_is_not_discovered' needs to be of type: <class 'bool'>",
        ),
        (
            "relocating_deceptive_nodes_generates_a_new_node",
            "fail",
            "'relocating_deceptive_nodes_generates_a_new_node' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation of `BlueAgentConfig` with invalid data type."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # BETWEEN 0 and 1
        (
            "chance_to_immediately_discover_intrusion",
            2,
            "'chance_to_immediately_discover_intrusion' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_immediately_discover_intrusion",
            -1,
            "'chance_to_immediately_discover_intrusion' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_immediately_discover_intrusion_deceptive_node",
            2,
            "'chance_to_immediately_discover_intrusion_deceptive_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_immediately_discover_intrusion_deceptive_node",
            -1,
            "'chance_to_immediately_discover_intrusion_deceptive_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_intrusion_on_scan_deceptive_node",
            2,
            "'chance_to_discover_intrusion_on_scan_deceptive_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_intrusion_on_scan_deceptive_node",
            -1,
            "'chance_to_discover_intrusion_on_scan_deceptive_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_intrusion_on_scan",
            2,
            "'chance_to_discover_intrusion_on_scan' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_intrusion_on_scan",
            -1,
            "'chance_to_discover_intrusion_on_scan' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_failed_attack",
            2,
            "'chance_to_discover_failed_attack' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_failed_attack",
            -1,
            "'chance_to_discover_failed_attack' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_known",
            2,
            "'chance_to_discover_succeeded_attack_compromise_known' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_known",
            -1,
            "'chance_to_discover_succeeded_attack_compromise_known' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_not_known",
            2,
            "'chance_to_discover_succeeded_attack_compromise_not_known' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_compromise_not_known",
            -1,
            "'chance_to_discover_succeeded_attack_compromise_not_known' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_failed_attack_deceptive_node",
            2,
            "'chance_to_discover_failed_attack_deceptive_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_failed_attack_deceptive_node",
            -1,
            "'chance_to_discover_failed_attack_deceptive_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_deceptive_node",
            2,
            "'chance_to_discover_succeeded_attack_deceptive_node' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "chance_to_discover_succeeded_attack_deceptive_node",
            -1,
            "'chance_to_discover_succeeded_attack_deceptive_node' Needs to have a value greater than: 0 (inclusive)",
        ),
        # BETWEEN -1 and 1
        (
            "vulnerability_change_during_node_patch",
            2,
            "'vulnerability_change_during_node_patch' Needs to have a value less than: 1 (inclusive)",
        ),
        (
            "vulnerability_change_during_node_patch",
            -2,
            "'vulnerability_change_during_node_patch' Needs to have a value greater than: -1 (inclusive)",
        ),
    ],
)
def test_invalid_config_range(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation of `BlueAgent` with invalid config range."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


def test_blue_has_no_action_error():
    """Tests blue not having any actions."""
    conf: Dict = get_config_dict()

    conf["blue_uses_reduce_vulnerability"] = False
    conf["blue_uses_restore_node"] = False
    conf["blue_uses_make_node_safe"] = False
    conf["blue_uses_scan"] = False
    conf["blue_uses_isolate_node"] = False
    conf["blue_uses_reconnect_node"] = False
    conf["blue_uses_do_nothing"] = False
    conf["blue_uses_deceptive_nodes"] = False

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert (
        err_info.value.args[0]
        == "'blue_uses_****' -> Blue must have at least one action selected. If you want blue to do nothing set "
        "'blue_uses_do_nothing' to True."
    )


def test_reconnect_isolate_config():
    """Tests use isolate node while reconnect node is False."""
    conf: Dict = get_config_dict()

    conf["blue_uses_isolate_node"] = True
    conf["blue_uses_reconnect_node"] = False

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert (
        err_info.value.args[0]
        == "'blue_uses_isolate_node', 'blue_uses_reconnect_node' -> Blue should be able to reconnect or isolate nodes "
        "if the other is true."
    )

    conf["blue_uses_isolate_node"] = False
    conf["blue_uses_reconnect_node"] = True

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert (
        err_info.value.args[0]
        == "'blue_uses_isolate_node', 'blue_uses_reconnect_node' -> Blue should be able to reconnect or isolate nodes "
        "if the other is true."
    )


def test_no_max_number_deceptive_nodes():
    """Tests using deceptive nodes but there being 0 as the max number."""
    conf: Dict = get_config_dict()

    conf["blue_uses_deceptive_nodes"] = True
    conf["max_number_deceptive_nodes"] = 0

    with pytest.raises(ValueError) as err_info:
        BlueAgentConfig.create(conf)

    # assert that the error message is as expected
    assert (
        err_info.value.args[0]
        == "'blue_uses_deceptive_nodes', 'max_number_deceptive_nodes' -> If blue can use deceptive nodes then max_number_deceptive_nodes."
    )
