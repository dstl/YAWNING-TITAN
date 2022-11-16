from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.environment.rewards_config import RewardsConfig


def get_config_dict() -> Dict:
    """Return the REWARDS config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["REWARDS"]


def test_read_valid_config():
    """Tests creation of `RewardsConfig` with a valid config."""
    config_dict = get_config_dict()
    rewards = RewardsConfig.create(config_dict)
    assert rewards.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        # INT/FLOAT
        (
            "rewards_for_loss",
            "fail",
            "'rewards_for_loss' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        (
            "rewards_for_reaching_max_steps",
            "fail",
            "'rewards_for_reaching_max_steps' needs to be of type: <class 'int'> or <class 'float'>",
        ),
        # BOOLEAN
        (
            "end_rewards_are_multiplied_by_end_state",
            "fail",
            "'end_rewards_are_multiplied_by_end_state' needs to be of type: <class 'bool'>",
        ),
        (
            "reduce_negative_rewards_for_closer_fails",
            "fail",
            "'reduce_negative_rewards_for_closer_fails' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests creation of `RewardsConfig` with an invalid type."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        RewardsConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err


def test_invalid_reward_function_type():
    """Tests creation of `RewardsConfig` with an invalid reward_function type."""
    conf: Dict = get_config_dict()

    # set value
    conf["reward_function"] = True

    with pytest.raises(TypeError) as err_info:
        RewardsConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == "hasattr(): attribute name must be string"
