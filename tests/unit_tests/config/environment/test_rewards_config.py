from typing import Dict, Any

import pytest

from tests.unit_tests.config.config_test_utils import read_yaml_file
from tests.unit_tests.config.environment import TEST_REWARDS_CONFIG_PATH
from yawning_titan.config.environment.rewards_config import RewardsConfig


def get_config_dict() -> Dict:
    return read_yaml_file(TEST_REWARDS_CONFIG_PATH)


def test_read_valid_config():
    rewards_config = RewardsConfig.create(get_config_dict())

    assert rewards_config.reward_loss == -100

    assert rewards_config.reward_success == 100

    assert rewards_config.reward_end_multiplier is True

    assert rewards_config.reward_reduce_negative_rewards is True

    assert rewards_config.reward_function == "standard_rewards"


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT
        ("rewards_for_loss", "fail",
         "'rewards_for_loss' needs to be of type: <class 'int'> or <class 'float'>"),
        ("rewards_for_reaching_max_steps", "fail",
         "'rewards_for_reaching_max_steps' needs to be of type: <class 'int'> or <class 'float'>"),

        # BOOLEAN
        ("end_rewards_are_multiplied_by_end_state", "fail",
         "'end_rewards_are_multiplied_by_end_state' needs to be of type: <class 'bool'>"),
        ("reduce_negative_rewards_for_closer_fails", "fail",
         "'reduce_negative_rewards_for_closer_fails' needs to be of type: <class 'bool'>"),
    ]
)
def test_invalid_config_type(config_item_to_test: str, config_value: Any, expected_err: str):
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        RewardsConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


def test_invalid_reward_function_type():
    conf: Dict = get_config_dict()

    # set value
    conf["reward_function"] = True

    with pytest.raises(TypeError) as err_info:
        RewardsConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == "hasattr(): attribute name must be string"
