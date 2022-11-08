from __future__ import annotations
from ast import Dict
from dataclasses import asdict, dataclass
from logging import getLogger
from typing import Any

import yaml
from yaml import SafeLoader

from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import (
    ObservationSpaceConfig,
)
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.config_group_class import (
    ConfigGroupABC,
    MiscellaneousConfig,
)
from yawning_titan.config.game_modes import default_game_mode_path

import ruamel.yaml as ry

_LOGGER = getLogger(__name__)


@dataclass()
class GameModeConfig:
    """
    Class that holds the configuration for YAWNING-TITAN
    """

    red: RedAgentConfig
    """
    Red agent configuration object
    """

    blue: BlueAgentConfig
    """
    Blue agent configuration object
    """

    observation_space: ObservationSpaceConfig
    """
    Observation space configuration object
    """

    game_rules: GameRulesConfig
    """
    Game rules configuration object
    """

    reset: ResetConfig
    """
    Reset configuration object
    """

    rewards: RewardsConfig
    """
    Rewards configuration object
    """

    miscellaneous: MiscellaneousConfig
    """
    Is true if the timestep data is output to JSON
    """

    @classmethod
    def create(cls, settings:Dict[str, Dict[str, Any]]) -> GameModeConfig:
        """
        Creates an instance of the GameModeConfig class
        """
        return GameModeConfig(
            red=RedAgentConfig.create(settings["RED"]),
            blue=BlueAgentConfig.create(settings["BLUE"]),
            observation_space=ObservationSpaceConfig.create(
                settings["OBSERVATION_SPACE"]
            ),
            game_rules=GameRulesConfig.create(settings=settings["GAME_RULES"]),
            reset=ResetConfig.create(settings["RESET"]),
            rewards=RewardsConfig.create(settings["REWARDS"]),
            miscellaneous=MiscellaneousConfig.create(settings["MISCELLANEOUS"]),
        )

    @classmethod
    def create_from_yaml(cls, settings_path=default_game_mode_path()) -> GameModeConfig:
        try:
            with open(settings_path) as f:
                settings = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            _LOGGER.critical(msg, exc_info=True)
            raise e
        return cls.create(settings=settings)

    def as_formatted_dict(self):
        settings_dict = {
            key: val
            for key, val in self.__dict__.items()
            if isinstance(val, ConfigGroupABC)
        }
        _settings_dict = {}
        for section_name, section_class in settings_dict.items():
            section_dict = section_class.to_dict()
            _settings_dict[section_name.upper()] = section_dict
        return _settings_dict

    def write_to_file(self, settings_path):
        self.file_path = settings_path
        with open(settings_path, "w") as file:
            yaml.safe_dump(self.as_formatted_dict(), file)

    def write_to_file_with_comments(self, file_path):
        settings_dict = self.as_formatted_dict()
        data = ry.round_trip_load(ry.round_trip_dump(settings_dict))

        _yaml = ry.YAML()
        _yaml.indent(mapping=2)

        with open(file_path, "w") as f:
            section_name: str
            section_class: ConfigGroupABC
            for section_name, section_class in self.__dict__.items():
                if isinstance(section_class, ConfigGroupABC):
                    section_name = section_name.upper()
                    # data[section_name].yaml_set_start_comment(, indent=2) TODO: add description for individual config object
                    data[section_name] = section_class.as_commented_yaml()
            _yaml.dump(data, f)
