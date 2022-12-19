from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from yaml import SafeLoader

from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import (
    ObservationSpaceConfig,
)
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan.config.game_modes import default_game_mode_path

_LOGGER = getLogger(__name__)


@dataclass()
class GameModeConfig:
    """Class that holds the configuration for YAWNING-TITAN."""

    _red: RedAgentConfig
    _observation_space: ObservationSpaceConfig
    _blue: BlueAgentConfig
    _game_rules: GameRulesConfig
    _reset: ResetConfig
    _rewards: RewardsConfig
    _miscellaneous: MiscellaneousConfig

    # region Getters
    @property
    def red(self) -> RedAgentConfig:
        """The RegAgentConfig."""
        return self._red

    @property
    def observation_space(self) -> ObservationSpaceConfig:
        """The ObservationSpaceConfig."""
        return self._observation_space

    @property
    def blue(self) -> BlueAgentConfig:
        """The BlueAgentConfig."""
        return self._blue

    @property
    def game_rules(self) -> GameRulesConfig:
        """The GameRulesConfig."""
        return self._game_rules

    @property
    def reset(self) -> ResetConfig:
        """The ResetConfig."""
        return self._reset

    @property
    def rewards(self) -> RewardsConfig:
        """The RewardsConfig."""
        return self._rewards

    @property
    def miscellaneous(self) -> MiscellaneousConfig:
        """The MiscellaneousConfig."""
        return self._miscellaneous

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Dict[str, Any]]) -> GameModeConfig:
        """
        Creates an instance of `GameModeConfig` after calling.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        return GameModeConfig(
            _red=RedAgentConfig.create(config_dict["RED"]),
            _observation_space=ObservationSpaceConfig.create(
                config_dict["OBSERVATION_SPACE"]
            ),
            _blue=BlueAgentConfig.create(config_dict["BLUE"]),
            _game_rules=GameRulesConfig.create(config_dict["GAME_RULES"]),
            _reset=ResetConfig.create(config_dict["RESET"]),
            _rewards=RewardsConfig.create(config_dict["REWARDS"]),
            _miscellaneous=MiscellaneousConfig.create(config_dict["MISCELLANEOUS"]),
        )

    @classmethod
    def create_from_yaml(
        cls, config_path: Union[str, Path] = default_game_mode_path()
    ) -> GameModeConfig:
        """
        Create and return an instance of `GameModeConfig` from a given config `.yaml` file path.

        Args:
            config_path:
                A config `.yaml` filepath.
        Returns:
            An instance of `GameModeConfig`.
        """
        try:
            with open(config_path) as f:
                config_dict = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {config_path}"
            _LOGGER.critical(msg, exc_info=True)
            raise e
        return cls.create(config_dict)

    def to_dict(self, key_upper: bool = False) -> Dict[str, Any]:
        """Returns the instance of `GameModeConfig` as a dict."""
        d = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                k = k[1:]
                if isinstance(v, ConfigABC):
                    v = v.to_dict()
            d[k.upper() if key_upper else k] = v
        return d

    def to_yaml(self, settings_path: Path):
        """
        Save the instance of `GameModeConfig` to a `.yaml` file.

        Args:
            settings_path:
                The destination filepath.
        """
        with open(settings_path, "w") as file:
            yaml.safe_dump(self.to_dict(key_upper=True), file)
