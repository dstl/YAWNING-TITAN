import os
from pathlib import Path
from typing import Dict
from uuid import uuid4

import pytest

from tests import TEST_BASE_NEW_CONFIG_PATH
from tests.config_test_utils import read_yaml_file
from yawning_titan.config.agents.new_blue_agent_config import Blue
from yawning_titan.config.agents.new_red_agent_config import Red
from yawning_titan.config.environment.new_game_rules_config import GameRules
from yawning_titan.config.environment.new_observation_space_config import (
    ObservationSpace,
)
from yawning_titan.config.environment.new_reset_config import Reset
from yawning_titan.config.environment.new_rewards_config import Rewards
from yawning_titan.config.game_config.game_mode import GameMode
from yawning_titan.config.game_config.new_miscellaneous_config import Miscellaneous
from yawning_titan.config.game_modes import default_new_game_mode_path


def get_config_dict() -> Dict:
    """Return the config dict from the `TEST_BASE_CONFIG_PATH`."""
    return read_yaml_file(TEST_BASE_NEW_CONFIG_PATH)


def get_default_config_dict() -> Dict:
    """Return the default game mode config."""
    return read_yaml_file(default_new_game_mode_path())


def test_read_valid_path_and_valid_config_classes_match():
    """Tests reading config from a valid path that is a valid config.

    Compare complete classes by calling the eq dunder.
    """
    config_dict = get_config_dict()
    game_mode: GameMode = GameMode()
    game_mode.set_from_yaml(TEST_BASE_NEW_CONFIG_PATH)

    red = Red("The configuration of the red agent")
    blue = Blue("The configuration of the blue agent")
    game_rules = GameRules("The rules of the overall game mode")
    blue_can_observe = ObservationSpace(
        "The characteristics of the network and the red agent that the blue agent can observe"
    )
    game_rules = GameRules("The rules of the overall game mode")
    on_reset = Reset("The changes to the network made upon reset")
    rewards = Rewards("The rewards the blue agent gets for different game states")
    miscellaneous = Miscellaneous("Additional options")

    red.set_from_dict(config_dict["red"])
    blue.set_from_dict(config_dict["blue"])
    game_rules.set_from_dict(config_dict["game_rules"])
    blue_can_observe.set_from_dict(config_dict["blue_can_observe"])
    on_reset.set_from_dict(config_dict["on_reset"])
    rewards.set_from_dict(config_dict["rewards"])
    miscellaneous.set_from_dict(config_dict["miscellaneous"])

    game_mode.set_from_yaml(TEST_BASE_NEW_CONFIG_PATH)
    assert game_mode.red == red
    assert game_mode.blue == blue
    assert game_mode.blue_can_observe == blue_can_observe
    assert game_mode.game_rules == game_rules
    assert game_mode.on_reset == on_reset
    assert game_mode.rewards == rewards
    assert game_mode.miscellaneous == miscellaneous


def test_read_valid_path_and_valid_config_values_match():
    """Tests reading config from a valid path that is a valid config.

    Compare dictionary representations of elements.
    """
    config_dict = get_config_dict()
    game_mode: GameMode = GameMode()
    red = Red("The configuration of the red agent")
    blue = Blue("The configuration of the blue agent")
    game_rules = GameRules("The rules of the overall game mode")
    blue_can_observe = ObservationSpace(
        "The characteristics of the network and the red agent that the blue agent can observe"
    )
    game_rules = GameRules("The rules of the overall game mode")
    on_reset = Reset("The changes to the network made upon reset")
    rewards = Rewards("The rewards the blue agent gets for different game states")
    miscellaneous = Miscellaneous("Additional options")

    red.set_from_dict(config_dict["red"])
    blue.set_from_dict(config_dict["blue"])
    game_rules.set_from_dict(config_dict["game_rules"])
    blue_can_observe.set_from_dict(config_dict["blue_can_observe"])
    on_reset.set_from_dict(config_dict["on_reset"])
    rewards.set_from_dict(config_dict["rewards"])
    miscellaneous.set_from_dict(config_dict["miscellaneous"])

    game_mode.set_from_yaml(TEST_BASE_NEW_CONFIG_PATH)
    assert game_mode.red.to_dict(values_only=True) == red.to_dict(values_only=True)
    assert game_mode.blue.to_dict(values_only=True) == blue.to_dict(values_only=True)
    assert game_mode.blue_can_observe.to_dict(
        values_only=True
    ) == blue_can_observe.to_dict(values_only=True)
    assert game_mode.game_rules.to_dict(values_only=True) == game_rules.to_dict(
        values_only=True
    )
    assert game_mode.on_reset.to_dict(values_only=True) == on_reset.to_dict(
        values_only=True
    )
    assert game_mode.rewards.to_dict(values_only=True) == rewards.to_dict(
        values_only=True
    )
    assert game_mode.miscellaneous.to_dict(values_only=True) == miscellaneous.to_dict(
        values_only=True
    )


def test_read_default_config():
    """Tests reading the default game mode config."""
    config_dict = get_default_config_dict()
    game_mode: GameMode = GameMode()
    red = Red("The configuration of the red agent")
    blue = Blue("The configuration of the blue agent")
    game_rules = GameRules("The rules of the overall game mode")
    blue_can_observe = ObservationSpace(
        "The characteristics of the network and the red agent that the blue agent can observe"
    )
    game_rules = GameRules("The rules of the overall game mode")
    on_reset = Reset("The changes to the network made upon reset")
    rewards = Rewards("The rewards the blue agent gets for different game states")
    miscellaneous = Miscellaneous("Additional options")

    game_mode.set_from_yaml(default_new_game_mode_path())

    red.set_from_dict(config_dict["red"])
    blue.set_from_dict(config_dict["blue"])
    game_rules.set_from_dict(config_dict["game_rules"])
    blue_can_observe.set_from_dict(config_dict["blue_can_observe"])
    on_reset.set_from_dict(config_dict["on_reset"])
    rewards.set_from_dict(config_dict["rewards"])
    miscellaneous.set_from_dict(config_dict["miscellaneous"])

    assert game_mode.red == red
    assert game_mode.blue == blue
    assert game_mode.blue_can_observe == blue_can_observe
    assert game_mode.game_rules == game_rules
    assert game_mode.on_reset == on_reset
    assert game_mode.rewards == rewards
    assert game_mode.miscellaneous == miscellaneous


def test_read_created_yaml(tmp_path_factory):
    """Tests reading a newly created game mode yaml file."""
    config_dict = get_default_config_dict()
    config_path = Path(
        os.path.join(tmp_path_factory.mktemp("yawning-titan"), f"{uuid4()}.yaml")
    ).as_posix()

    game_mode: GameMode = GameMode()
    game_mode.set_from_dict(config_dict)
    game_mode.to_yaml(config_path)

    new_game_mode: GameMode = GameMode()

    new_game_mode.set_from_yaml(config_path)
    assert new_game_mode.to_dict(values_only=True) == config_dict


def test_invalid_path():
    """Test attempting to create a `GameModeConfig` from an invalid filepath."""
    with pytest.raises(FileNotFoundError) as err_info:
        GameMode().set_from_yaml("fake_test_path")

    # assert that the error message is as expected
    assert err_info.value.args[1] == "No such file or directory"
