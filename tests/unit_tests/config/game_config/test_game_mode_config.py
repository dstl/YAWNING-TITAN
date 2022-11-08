import os
from pathlib import Path
from typing import Dict

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan.config.game_modes import default_game_mode_path


def get_config_dict() -> Dict:
    return read_yaml_file(TEST_BASE_CONFIG_PATH)


def get_default_config_dict() -> Dict:
    return read_yaml_file(default_game_mode_path())


def test_read_valid_path_and_valid_config():
    config_dict = get_config_dict()
    game_mode = GameModeConfig.create_from_yaml(TEST_BASE_CONFIG_PATH)    
    assert game_mode.red == RedAgentConfig.create(config_dict["RED"])
    assert game_mode.blue == BlueAgentConfig.create(config_dict["BLUE"])
    assert game_mode.observation_space == ObservationSpaceConfig.create(config_dict["OBSERVATION_SPACE"])
    assert game_mode.game_rules == GameRulesConfig.create(config_dict["GAME_RULES"])
    assert game_mode.reset== ResetConfig.create(config_dict["RESET"])
    assert game_mode.rewards == RewardsConfig.create(config_dict["REWARDS"])
    assert game_mode.miscellaneous == MiscellaneousConfig.create(config_dict["MISCELLANEOUS"])


def test_read_default_config():
    game_mode:GameModeConfig = GameModeConfig.create()
    config_dict = get_default_config_dict()
    assert game_mode.red == RedAgentConfig.create(config_dict["RED"])
    assert game_mode.blue == BlueAgentConfig.create(config_dict["BLUE"])
    assert game_mode.observation_space == ObservationSpaceConfig.create(config_dict["OBSERVATION_SPACE"])
    assert game_mode.game_rules == GameRulesConfig.create(config_dict["GAME_RULES"])
    assert game_mode.reset == ResetConfig.create(config_dict["RESET"])
    assert game_mode.rewards == RewardsConfig.create(config_dict["REWARDS"])
    assert game_mode.miscellaneous == MiscellaneousConfig.create(config_dict["MISCELLANEOUS "])

def test_read_created_yaml(tmpdir_factory):
    game_mode:GameModeConfig = GameModeConfig.create()
    config_dict = get_default_config_dict()
    config_dir = tmpdir_factory.mktemp("temp")
    game_mode.write_to_file(config_dir)
    new_game_mode = GameModeConfig.create_from_yaml(config_dir)
    assert new_game_mode.as_formatted_dict() == config_dict


def test_invalid_path():
    with pytest.raises(FileNotFoundError) as err_info:
        GameModeConfig.create(Path("fake_test_path"))

    # assert that the error message is as expected
    assert err_info.value.args[1] == "No such file or directory"
