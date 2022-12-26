import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.agents.new_blue_agent_config import Blue
from yawning_titan.config.toolbox.core import ConfigItem


@pytest.fixture
def default_blue() -> Blue:
    """Create a blue agent using the default config."""
    blue = Blue()
    blue.set_from_dict(get_default_config_dict()["blue"])
    return blue


@pytest.fixture(scope="module")
def blue_erroneous_types():
    """Create a blue agent where items have erroneous types."""
    blue_erroneous_types_config = {
        "action_set": {
            "restore_node": 1,
            "scan": 1,
            "isolate_node": 1,
            "reconnect_node": 1,
            "reduce_vulnerability": 1,
            "do_nothing": 1,
            "make_node_safe": {
                "use": 1,
                "increases_vulnerability": 1,
                "gives_random_vulnerability": 1,
                "vulnerability_change_during_node_patch": True,
            },
            "deceptive_nodes": {
                "use": 1,
                "max_number": True,
                "new_node_on_relocate": 1,
            },
        },
        "intrusion_discovery_chance": {
            "immediate": True,
            "immediate_deceptive_node": True,
            "on_scan": True,
            "on_scan_deceptive_node": True,
        },
        "attack_discovery": {
            "failed_attacks": {
                "use": 1,
                "chance": {"standard_node": True, "deceptive_node": True},
            },
            "succeeded_attacks": {
                "use": 1,
                "chance": {"standard_node": True, "deceptive_node": True},
            },
            "succeeded_attacks_unknown_comprimise": {
                "use": 1,
                "chance": {"standard_node": True, "deceptive_node": True},
            },
        },
    }
    blue = Blue()
    blue.set_from_dict(blue_erroneous_types_config)
    return blue


@pytest.fixture(scope="module")
def blue_erroneous_range_to_high() -> Blue:
    """Create a blue agent where items have erroneous values that are too high."""
    blue_erroneous_types_config = {
        "action_set": {
            "restore_node": 1,
            "scan": 1,
            "isolate_node": 1,
            "reconnect_node": 1,
            "reduce_vulnerability": 1,
            "do_nothing": 1,
            "make_node_safe": {
                "use": 1,
                "increases_vulnerability": 1,
                "gives_random_vulnerability": 1,
                "vulnerability_change_during_node_patch": 2,
            },
            "deceptive_nodes": {
                "use": 1,
                "max_number": True,
                "new_node_on_relocate": 1,
            },
        },
        "intrusion_discovery_chance": {
            "immediate": 2,
            "immediate_deceptive_node": 2,
            "on_scan": 2,
            "on_scan_deceptive_node": 2,
        },
        "attack_discovery": {
            "failed_attacks": {
                "use": 1,
                "chance": {"standard_node": 2, "deceptive_node": 2},
            },
            "succeeded_attacks": {
                "use": 1,
                "chance": {"standard_node": 2, "deceptive_node": 2},
            },
            "succeeded_attacks_unknown_comprimise": {
                "use": 1,
                "chance": {"standard_node": 2, "deceptive_node": 2},
            },
        },
    }
    blue = Blue()
    blue.set_from_dict(blue_erroneous_types_config)
    return blue


@pytest.fixture(scope="module")
def blue_erroneous_range_to_low() -> Blue:
    """Create a blue agent where items have erroneous values that are too low."""
    blue_erroneous_types_config = {
        "action_set": {
            "restore_node": 1,
            "scan": 1,
            "isolate_node": 1,
            "reconnect_node": 1,
            "reduce_vulnerability": 1,
            "do_nothing": 1,
            "make_node_safe": {
                "use": 1,
                "increases_vulnerability": 1,
                "gives_random_vulnerability": 1,
                "vulnerability_change_during_node_patch": -2,
            },
            "deceptive_nodes": {
                "use": 1,
                "max_number": True,
                "new_node_on_relocate": 1,
            },
        },
        "intrusion_discovery_chance": {
            "immediate": -1,
            "immediate_deceptive_node": -1,
            "on_scan": -1,
            "on_scan_deceptive_node": -1,
        },
        "attack_discovery": {
            "failed_attacks": {
                "use": 1,
                "chance": {"standard_node": -1, "deceptive_node": -1},
            },
            "succeeded_attacks": {
                "use": 1,
                "chance": {"standard_node": -1, "deceptive_node": -1},
            },
            "succeeded_attacks_unknown_comprimise": {
                "use": 1,
                "chance": {"standard_node": -1, "deceptive_node": -1},
            },
        },
    }
    blue = Blue()
    blue.set_from_dict(blue_erroneous_types_config)
    return blue


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        # INT/FLOAT TYPES
        (
            "intrusion_discovery_chance.immediate",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "intrusion_discovery_chance.on_scan",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.make_node_safe.vulnerability_change_during_node_patch",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "attack_discovery.failed_attacks.chance.standard_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.standard_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "attack_discovery.succeeded_attacks_unknown_comprimise.chance.standard_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "intrusion_discovery_chance.immediate_deceptive_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "intrusion_discovery_chance.on_scan_deceptive_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "attack_discovery.failed_attacks.chance.deceptive_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.deceptive_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        # INT TYPE
        (
            "action_set.deceptive_nodes.max_number",
            "Value True is of type <class 'bool'>, should be <class 'int'>.",
        ),
        # BOOLEANS
        (
            "action_set.make_node_safe.increases_vulnerability",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.make_node_safe.gives_random_vulnerability",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.reduce_vulnerability",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.restore_node",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.make_node_safe.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.scan",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.isolate_node",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.reconnect_node",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.do_nothing",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.deceptive_nodes.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "attack_discovery.failed_attacks.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "attack_discovery.succeeded_attacks.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "attack_discovery.succeeded_attacks_unknown_comprimise.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.deceptive_nodes.new_node_on_relocate",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, expected_err: str, blue_erroneous_types
):
    """Tests creation of `Blue` with invalid data type."""
    item: ConfigItem = eval(f"blue_erroneous_types.{config_item_to_test}")
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        # BETWEEN 0 and 1
        (
            "intrusion_discovery_chance.immediate",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "intrusion_discovery_chance.immediate_deceptive_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "intrusion_discovery_chance.on_scan_deceptive_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "intrusion_discovery_chance.on_scan",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "attack_discovery.failed_attacks.chance.standard_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.standard_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "attack_discovery.succeeded_attacks_unknown_comprimise.chance.standard_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "attack_discovery.failed_attacks.chance.deceptive_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.deceptive_node",
            "Value 2 is greater than the max property 1.",
        ),
        # BETWEEN -1 and 1
        (
            "action_set.make_node_safe.vulnerability_change_during_node_patch",
            "Value 2 is greater than the max property 1.",
        ),
    ],
)
def test_invalid_config_range_too_high(
    config_item_to_test: str, expected_err: str, blue_erroneous_range_to_high
):
    """Tests creation of `BlueAgent` with invalid config range."""
    item: ConfigItem = eval(f"blue_erroneous_range_to_high.{config_item_to_test}")
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        # BETWEEN 0 and 1
        (
            "intrusion_discovery_chance.immediate",
            "Value -1 is less than the min property 0.",
        ),
        (
            "intrusion_discovery_chance.immediate_deceptive_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "intrusion_discovery_chance.on_scan_deceptive_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "intrusion_discovery_chance.on_scan",
            "Value -1 is less than the min property 0.",
        ),
        (
            "attack_discovery.failed_attacks.chance.standard_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.standard_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "attack_discovery.succeeded_attacks_unknown_comprimise.chance.standard_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "attack_discovery.failed_attacks.chance.deceptive_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "attack_discovery.succeeded_attacks.chance.deceptive_node",
            "Value -1 is less than the min property 0.",
        ),
        # BETWEEN -1 and 1
        (
            "action_set.make_node_safe.vulnerability_change_during_node_patch",
            "Value -2 is less than the min property -1.",
        ),
    ],
)
def test_invalid_config_range_too_low(
    config_item_to_test: str, expected_err: str, blue_erroneous_range_to_low
):
    """Tests creation of `BlueAgent` with invalid config range."""
    item: ConfigItem = eval(f"blue_erroneous_range_to_low.{config_item_to_test}")
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


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


def test_default_red_from_legacy(default_blue: Blue) -> Blue:
    """Create a red agent using the default config file."""
    blue = Blue()
    import yaml

    print(yaml.dump(blue.to_dict(values_only=True)))
    blue.set_from_dict(get_default_config_dict_legacy()["BLUE"], legacy=True)
    print(yaml.dump(blue.to_dict(values_only=True)))
    assert blue == default_blue
    assert blue.to_dict() == default_blue.to_dict()
