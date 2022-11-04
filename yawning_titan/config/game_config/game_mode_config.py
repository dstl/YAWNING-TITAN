from __future__ import annotations
from dataclasses import dataclass
from logging import getLogger

import yaml
from yaml import SafeLoader

from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_modes import default_game_mode_path

_LOGGER = getLogger(__name__)


@dataclass()
class GameModeConfig:
    """
    Class that holds the configuration for YAWNING-TITAN
    """

    red_agent_config: RedAgentConfig
    """
    Red agent configuration object
    """

    blue_agent_config: BlueAgentConfig
    """
    Blue agent configuration object
    """

    observation_space_config: ObservationSpaceConfig
    """
    Observation space configuration object
    """

    game_rules_config: GameRulesConfig
    """
    Game rules configuration object
    """

    reset_config: ResetConfig
    """
    Reset configuration object
    """

    rewards_config: RewardsConfig
    """
    Rewards configuration object
    """

    output_timestep_data_to_json: bool
    """
    Is true if the timestep data is output to JSON
    """

    @classmethod
    def create(
            cls,
            config_path=None
    ) -> GameModeConfig:
        """
        Creates an instance of the GameModeConfig class
        """
        # opens the fle the user has specified to be the location of the settings
        if not config_path:
            settings_path = default_game_mode_path()
        try:
            with open(settings_path) as f:
                settings = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        return GameModeConfig(
            red_agent_config=RedAgentConfig.create(settings["RED"]),
            blue_agent_config=BlueAgentConfig.create(settings["BLUE"]),
            observation_space_config=ObservationSpaceConfig.create(settings["OBSERVATION_SPACE"]),
            game_rules_config=GameRulesConfig.create(settings=settings["GAME_RULES"]),
            reset_config=ResetConfig.create(settings["RESET"]),
            rewards_config=RewardsConfig.create(settings["REWARDS"]),
            output_timestep_data_to_json=True
        )
