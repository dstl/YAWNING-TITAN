import os
from pathlib import Path
from typing import Dict

import pytest

from tests import TEST_CONFIG_PATH
from tests.unit_tests.config.config_test_utils import read_yaml_file
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import default_game_mode_path


def get_config_dict() -> Dict:
    return read_yaml_file(Path(os.path.join(TEST_CONFIG_PATH, "base_config.yaml")))


def get_default_config_dict() -> Dict:
    return read_yaml_file(default_game_mode_path())


def test_read_valid_path_and_valid_config():
    game_mode = GameModeConfig.create(os.path.join(TEST_CONFIG_PATH, "base_config.yaml"))

    assert game_mode.red_agent_config == RedAgentConfig.create(get_config_dict()["RED"])
    assert game_mode.blue_agent_config == BlueAgentConfig.create(get_config_dict()["BLUE"])
    assert game_mode.observation_space_config == ObservationSpaceConfig.create(get_config_dict()["OBSERVATION_SPACE"])
    assert game_mode.game_rules_config == GameRulesConfig.create(get_config_dict()["GAME_RULES"])
    assert game_mode.reset_config == ResetConfig.create(get_config_dict()["RESET"])
    assert game_mode.rewards_config == RewardsConfig.create(get_config_dict()["REWARDS"])
    assert game_mode.output_timestep_data_to_json == get_config_dict()["MISCELLANEOUS"]["output_timestep_data_to_json"]


def test_read_default_config():
    game_mode = GameModeConfig.create()

    assert game_mode.red_agent_config == RedAgentConfig.create(get_default_config_dict()["RED"])
    assert game_mode.blue_agent_config == BlueAgentConfig.create(get_default_config_dict()["BLUE"])
    assert game_mode.observation_space_config == ObservationSpaceConfig.create(
        get_default_config_dict()["OBSERVATION_SPACE"])
    assert game_mode.game_rules_config == GameRulesConfig.create(get_default_config_dict()["GAME_RULES"])
    assert game_mode.reset_config == ResetConfig.create(get_default_config_dict()["RESET"])
    assert game_mode.rewards_config == RewardsConfig.create(get_default_config_dict()["REWARDS"])
    assert game_mode.output_timestep_data_to_json == get_default_config_dict()["MISCELLANEOUS"][
        "output_timestep_data_to_json"]


def test_invalid_path():
    with pytest.raises(FileNotFoundError) as err_info:
        GameModeConfig.create(Path("fake_test_path"))

    # assert that the error message is as expected
    assert err_info.value.args[1] == "No such file or directory"
