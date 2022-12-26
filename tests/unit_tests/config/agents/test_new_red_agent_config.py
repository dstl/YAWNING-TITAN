import pytest

from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.config.agents.new_red_agent_config import Red
from yawning_titan.config.toolbox.core import ConfigItem


@pytest.fixture
def default_red() -> Red:
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict()["red"])
    return red


@pytest.fixture(scope="module")
def red_erroneous_types():
    """Create a red agent where items have erroneous types."""
    print("GHGHGH")
    red_erroneous_types_config = {
        "agent_attack": {
            "ignores_defences": 1,
            "always_succeeds": 1,
            "skill": {"use": 1, "value": True},
            "attack_from": {"only_red_agent_node": 1, "any_red_node": 1},
        },
        "action_set": {
            "spread": {
                "use": 1,
                "likelihood": True,
                "chance": True,
            },
            "random_infect": {
                "use": 1,
                "likelihood": True,
                "chance": True,
            },
            "move": {
                "use": 1,
                "likelihood": True,
            },
            "basic_attack": {
                "use": 1,
                "likelihood": True,
            },
            "do_nothing": {
                "use": 1,
                "likelihood": True,
            },
            "zero_day": {
                "use": 1,
                "start_amount": True,
                "days_required": True,
            },
        },
        "natural_spreading": {
            "capable": 1,
            "chance": {
                "to_connected_node": True,
                "to_unconnected_node": True,
            },
        },
        "target_mechanism": {
            "random": 1,
            "prioritise_connected_nodes": 1,
            "prioritise_unconnected_nodes": 1,
            "prioritise_vulnerable_nodes": 1,
            "prioritise_resilient_nodes": 1,
            "target": {"use": 1, "target": None, "always_choose_shortest_distance": 1},
        },
    }
    red = Red()
    red.set_from_dict(red_erroneous_types_config)
    return red


@pytest.fixture(scope="module")
def red_erroneous_range_to_low() -> Red:
    """Create a red agent where items have erroneous values that are too low."""
    red_erroneous_types_config = {
        "agent_attack": {
            "ignores_defences": 1,
            "always_succeeds": 1,
            "skill": {"use": 1, "value": -1},
            "attack_from": {"only_red_agent_node": 1, "any_red_node": 1},
        },
        "action_set": {
            "spread": {
                "use": True,
                "likelihood": -1,
                "chance": -1,
            },
            "random_infect": {
                "use": True,
                "likelihood": -1,
                "chance": -1,
            },
            "move": {
                "use": True,
                "likelihood": -1,
            },
            "basic_attack": {
                "use": True,
                "likelihood": -1,
            },
            "do_nothing": {
                "use": True,
                "likelihood": -1,
            },
            "zero_day": {
                "use": True,
                "start_amount": -1,
                "days_required": -1,
            },
        },
        "natural_spreading": {
            "capable": 1,
            "chance": {
                "to_connected_node": -1,
                "to_unconnected_node": -1,
            },
        },
        "target_mechanism": {
            "random": 1,
            "prioritise_connected_nodes": 1,
            "prioritise_unconnected_nodes": 1,
            "prioritise_vulnerable_nodes": 1,
            "prioritise_resilient_nodes": 1,
            "target": {"use": 1, "target": None, "always_choose_shortest_distance": 1},
        },
    }
    red = Red()
    red.set_from_dict(red_erroneous_types_config)
    return red


@pytest.fixture(scope="module")
def red_erroneous_range_to_high() -> Red:
    """Create a blue agent where items have erroneous values that are too high."""
    red_erroneous_types_config = {
        "agent_attack": {
            "ignores_defences": 1,
            "always_succeeds": 1,
            "skill": {"use": 1, "value": 2},
            "attack_from": {"only_red_agent_node": 1, "any_red_node": 1},
        },
        "action_set": {
            "spread": {
                "use": 1,
                "likelihood": True,
                "chance": 2,
            },
            "random_infect": {
                "use": 1,
                "likelihood": True,
                "chance": 2,
            },
            "move": {
                "use": 1,
                "likelihood": True,
            },
            "basic_attack": {
                "use": 1,
                "likelihood": True,
            },
            "do_nothing": {
                "use": 1,
                "likelihood": True,
            },
            "zero_day": {
                "use": 1,
                "start_amount": True,
                "days_required": True,
            },
        },
        "natural_spreading": {
            "capable": 1,
            "chance": {
                "to_connected_node": 2,
                "to_unconnected_node": 2,
            },
        },
        "target_mechanism": {
            "random": 1,
            "prioritise_connected_nodes": 1,
            "prioritise_unconnected_nodes": 1,
            "prioritise_vulnerable_nodes": 1,
            "prioritise_resilient_nodes": 1,
            "target": {"use": 1, "target": None, "always_choose_shortest_distance": 1},
        },
    }
    red = Red()
    red.set_from_dict(red_erroneous_types_config)
    return red


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        # INT/FLOAT TYPES
        (
            "action_set.spread.chance",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.random_infect.chance",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "agent_attack.skill.value",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.spread.likelihood",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.random_infect.likelihood",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.basic_attack.likelihood",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.do_nothing.likelihood",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "action_set.move.likelihood",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "natural_spreading.chance.to_connected_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        (
            "natural_spreading.chance.to_unconnected_node",
            "Value True is of type <class 'bool'>, should be <class 'float'> or <class 'int'>.",
        ),
        # INT TYPES
        (
            "action_set.zero_day.start_amount",
            "Value True is of type <class 'bool'>, should be <class 'int'>.",
        ),
        (
            "action_set.zero_day.days_required",
            "Value True is of type <class 'bool'>, should be <class 'int'>.",
        ),
        # BOOLEANS
        (
            "agent_attack.skill.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "agent_attack.ignores_defences",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "agent_attack.always_succeeds",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "agent_attack.attack_from.only_red_agent_node",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "agent_attack.attack_from.any_red_node",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.spread.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.random_infect.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.zero_day.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.basic_attack.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.do_nothing.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "action_set.move.use",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "target_mechanism.random",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "target_mechanism.prioritise_connected_nodes",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "target_mechanism.prioritise_unconnected_nodes",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "target_mechanism.prioritise_vulnerable_nodes",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "target_mechanism.prioritise_resilient_nodes",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
        (
            "natural_spreading.capable",
            "Value 1 is of type <class 'int'>, should be <class 'bool'>.",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, expected_err: str, red_erroneous_types
):
    """Tests creation of `Red` with invalid data type."""
    item: ConfigItem = eval(f"red_erroneous_types.{config_item_to_test}")
    print("ITEM: ", config_item_to_test, "VAL", item.value)
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        ("agent_attack.skill.value", "Value 2 is greater than the max property 1."),
        (
            "action_set.spread.chance",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "action_set.random_infect.chance",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "natural_spreading.chance.to_connected_node",
            "Value 2 is greater than the max property 1.",
        ),
        (
            "natural_spreading.chance.to_unconnected_node",
            "Value 2 is greater than the max property 1.",
        ),
    ],
)
def test_invalid_config_range_too_high(
    config_item_to_test: str, expected_err: str, red_erroneous_range_to_high
):
    """Tests creation of `Red` with invalid config range."""
    item: ConfigItem = eval(f"red_erroneous_range_to_high.{config_item_to_test}")
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


@pytest.mark.parametrize(
    ("config_item_to_test", "expected_err"),
    [
        # BETWEEN 0 and 1
        ("agent_attack.skill.value", "Value -1 is less than the min property 0."),
        (
            "action_set.spread.chance",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.random_infect.chance",
            "Value -1 is less than the min property 0.",
        ),
        (
            "natural_spreading.chance.to_connected_node",
            "Value -1 is less than the min property 0.",
        ),
        (
            "natural_spreading.chance.to_unconnected_node",
            "Value -1 is less than the min property 0.",
        ),
        # GREATER THAN 0
        (
            "action_set.spread.likelihood",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.random_infect.likelihood",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.basic_attack.likelihood",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.do_nothing.likelihood",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.move.likelihood",
            "Value -1 is less than the min property 0.",
        ),
        # GREATER THAN OR EQUAL TO 0
        (
            "action_set.zero_day.start_amount",
            "Value -1 is less than the min property 0.",
        ),
        (
            "action_set.zero_day.days_required",
            "Value -1 is less than the min property 0.",
        ),
    ],
)
def test_invalid_config_range_too_low(
    config_item_to_test: str, expected_err: str, red_erroneous_range_to_low
):
    """Tests creation of `Red` with invalid config range."""
    item: ConfigItem = eval(f"red_erroneous_range_to_low.{config_item_to_test}")
    # assert that the error message is as expected
    assert expected_err in item.validation.fail_reasons


def test_default_red_from_legacy(default_red: Red) -> Red:
    """Create a red agent using the default config file."""
    red = Red()
    red.set_from_dict(get_default_config_dict_legacy()["RED"], legacy=True)
    assert red == default_red
    assert red.to_dict() == default_red.to_dict()
