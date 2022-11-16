from typing import Any, Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.environment.reset_config import ResetConfig


def get_config_dict() -> Dict:
    """Return the RESET config dict."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)["RESET"]


def test_read_valid_config():
    """Tests creating a valid `ResetConfig`."""
    config_dict = get_config_dict()
    reset = ResetConfig.create(config_dict)
    assert reset.to_dict() == config_dict


@pytest.mark.parametrize(
    ("config_item_to_test", "config_value", "expected_err"),
    [
        (
            "randomise_vulnerabilities_on_reset",
            "fail",
            "'randomise_vulnerabilities_on_reset' needs to be of type: <class 'bool'>",
        ),
        (
            "choose_new_high_value_nodes_on_reset",
            "fail",
            "'choose_new_high_value_nodes_on_reset' needs to be of type: <class 'bool'>",
        ),
        (
            "choose_new_entry_nodes_on_reset",
            "fail",
            "'choose_new_entry_nodes_on_reset' needs to be of type: <class 'bool'>",
        ),
    ],
)
def test_invalid_config_type(
    config_item_to_test: str, config_value: Any, expected_err: str
):
    """Tests invalid config type."""
    conf: Dict = get_config_dict()

    # set value
    conf[config_item_to_test] = config_value

    with pytest.raises(ValueError) as err_info:
        ResetConfig.create(conf)

    # assert that the error message is as expected
    assert err_info.value.args[0] == expected_err
