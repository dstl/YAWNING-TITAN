import os
from pathlib import Path
from uuid import uuid4

import pytest
import yaml

from tests import TEST_CONFIG_PATH_NEW, TEST_CONFIG_PATH_OLD
from tests.unit_tests.config import (
    get_default_config_dict,
    get_default_config_dict_legacy,
)
from yawning_titan.game_modes.components.blue_agent import Blue
from yawning_titan.game_modes.components.game_rules import GameRules
from yawning_titan.game_modes.components.miscellaneous import Miscellaneous
from yawning_titan.game_modes.components.observation_space import ObservationSpace
from yawning_titan.game_modes.components.red_agent import Red
from yawning_titan.game_modes.components.reset import Reset
from yawning_titan.game_modes.components.rewards import Rewards
from yawning_titan.game_modes.game_mode import GameMode


@pytest.fixture
def default_game_mode() -> GameMode:
    """Create a game mode instance using the default config."""
    game_mode = GameMode()
    game_mode.set_from_dict(get_default_config_dict())
    return game_mode


def test_read_valid_path_and_valid_config_classes_match(default_game_mode: GameMode):
    """Tests reading config from a valid path that is a valid config.

    Compare complete classes by calling the eq dunder.
    """
    config_dict = get_default_config_dict()

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

    assert default_game_mode.red == red
    assert default_game_mode.blue == blue
    assert default_game_mode.blue_can_observe == blue_can_observe
    assert default_game_mode.game_rules == game_rules
    assert default_game_mode.on_reset == on_reset
    assert default_game_mode.rewards == rewards
    assert default_game_mode.miscellaneous == miscellaneous


def test_read_valid_path_and_valid_config_values_match(default_game_mode: GameMode):
    """Tests reading config from a valid path that is a valid config.

    Compare dictionary representations of elements.
    """
    config_dict = get_default_config_dict()

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

    assert default_game_mode.red.to_dict(values_only=True) == red.to_dict(
        values_only=True
    )
    assert default_game_mode.blue.to_dict(values_only=True) == blue.to_dict(
        values_only=True
    )
    assert default_game_mode.blue_can_observe.to_dict(
        values_only=True
    ) == blue_can_observe.to_dict(values_only=True)
    assert default_game_mode.game_rules.to_dict(values_only=True) == game_rules.to_dict(
        values_only=True
    )
    assert default_game_mode.on_reset.to_dict(values_only=True) == on_reset.to_dict(
        values_only=True
    )
    assert default_game_mode.rewards.to_dict(values_only=True) == rewards.to_dict(
        values_only=True
    )
    assert default_game_mode.miscellaneous.to_dict(
        values_only=True
    ) == miscellaneous.to_dict(values_only=True)


def test_read_default_config(default_game_mode: GameMode):
    """Tests reading the default game mode config."""
    config_dict = get_default_config_dict()

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

    assert default_game_mode.red == red
    assert default_game_mode.blue == blue
    assert default_game_mode.blue_can_observe == blue_can_observe
    assert default_game_mode.game_rules == game_rules
    assert default_game_mode.on_reset == on_reset
    assert default_game_mode.rewards == rewards
    assert default_game_mode.miscellaneous == miscellaneous


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


def test_default_game_mode_from_legacy(default_game_mode: GameMode):
    """Create a game mode instance using the default config file."""
    game_mode = GameMode()

    game_mode.set_from_dict(get_default_config_dict_legacy(), legacy=True)

    assert game_mode == default_game_mode
    assert game_mode.to_dict() == default_game_mode.to_dict()


def test_everything_changed_game_mode_from_legacy():
    """Create a game mode instance using the everything changed config file to ensure all items can be updated."""
    with open(TEST_CONFIG_PATH_NEW / "everything_changed.yaml") as f:
        config_dict = yaml.safe_load(f)

    game_mode = GameMode()
    game_mode.set_from_yaml(
        (TEST_CONFIG_PATH_OLD / "everything_changed.yaml").as_posix(), legacy=True
    )

    d = game_mode.to_dict(values_only=True)

    d["red"]["target_mechanism"]["target_specific_node"].pop("use")

    assert d == config_dict
