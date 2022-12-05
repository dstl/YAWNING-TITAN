import os
from pathlib import Path
from typing import Dict
from uuid import uuid4

import pytest

from tests import TEST_BASE_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import (
    ObservationSpaceConfig,
)
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan.config.game_modes import default_game_mode_path


def get_config_dict() -> Dict:
    """Return the config dict from the `TEST_BASE_CONFIG_PATH`."""
    return read_yaml_file(TEST_BASE_CONFIG_PATH)


def get_default_config_dict() -> Dict:
    """Return the defauly game mode config."""
    return read_yaml_file(default_game_mode_path())


def test_read_valid_path_and_valid_config():
    """Tests reading config from a valid path that is a valid config."""
    config_dict = get_config_dict()
    game_mode = GameModeConfig.create_from_yaml(TEST_BASE_CONFIG_PATH)
    assert game_mode.red == RedAgentConfig.create(config_dict["RED"])
    assert game_mode.blue == BlueAgentConfig.create(config_dict["BLUE"])
    assert game_mode.observation_space == ObservationSpaceConfig.create(
        config_dict["OBSERVATION_SPACE"]
    )
    assert game_mode.game_rules == GameRulesConfig.create(config_dict["GAME_RULES"])
    assert game_mode.reset == ResetConfig.create(config_dict["RESET"])
    assert game_mode.rewards == RewardsConfig.create(config_dict["REWARDS"])
    assert game_mode.miscellaneous == MiscellaneousConfig.create(
        config_dict["MISCELLANEOUS"]
    )


def test_read_default_config():
    """Tests reading the default game mode config."""
    game_mode: GameModeConfig = GameModeConfig.create_from_yaml()
    config_dict = get_default_config_dict()
    assert game_mode.red == RedAgentConfig.create(config_dict["RED"])
    assert game_mode.blue == BlueAgentConfig.create(config_dict["BLUE"])
    assert game_mode.observation_space == ObservationSpaceConfig.create(
        config_dict["OBSERVATION_SPACE"]
    )
    assert game_mode.game_rules == GameRulesConfig.create(config_dict["GAME_RULES"])
    assert game_mode.reset == ResetConfig.create(config_dict["RESET"])
    assert game_mode.rewards == RewardsConfig.create(config_dict["REWARDS"])
    assert game_mode.miscellaneous == MiscellaneousConfig.create(
        config_dict["MISCELLANEOUS"]
    )


def test_read_created_yaml(tmp_path_factory):
    """Tests reading a newly created game mode yaml file."""
    game_mode: GameModeConfig = GameModeConfig.create_from_yaml()
    config_dict = get_default_config_dict()
    config_file = Path(
        os.path.join(tmp_path_factory.mktemp("yawning-titan"), f"{uuid4()}.yaml")
    )
    game_mode.to_yaml(config_file)
    new_game_mode = GameModeConfig.create_from_yaml(config_file)
    assert new_game_mode.to_dict(key_upper=True) == config_dict


def test_invalid_path():
    """Test attempting to create a `GameModeConfig` from an invalid filepath."""
    with pytest.raises(FileNotFoundError) as err_info:
        GameModeConfig.create_from_yaml("fake_test_path")

    # assert that the error message is as expected
    assert err_info.value.args[1] == "No such file or directory"
