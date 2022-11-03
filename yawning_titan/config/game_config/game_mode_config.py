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

