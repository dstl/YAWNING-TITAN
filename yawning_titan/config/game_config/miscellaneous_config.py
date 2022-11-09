from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from yawning_titan.config.game_config.config_abc import ConfigABC


@dataclass()
class MiscellaneousConfig(ConfigABC):
    """
    Class that validates and stores the Miscellaneous Configuration
    """
    _output_timestep_data_to_json: bool

    @property
    def output_timestep_data_to_json(self) -> bool:
        """
        Toggle to output a json file for each step that contains the
        connections between nodes, the states of the nodes and the attacks
        that blue saw in that turn.
        """
        return self._output_timestep_data_to_json

    @output_timestep_data_to_json.setter
    def output_timestep_data_to_json(self, value):
        self._output_timestep_data_to_json = value

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> MiscellaneousConfig:
        """
        Creates an instance of `MiscellaneousConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        cls._validate(config_dict)

        misc_config = MiscellaneousConfig(
            _output_timestep_data_to_json=config_dict[
                "output_timestep_data_to_json"],
        )

        return misc_config

    @classmethod
    def _validate(cls, config_dict: Dict[str, Any]):
        pass
            