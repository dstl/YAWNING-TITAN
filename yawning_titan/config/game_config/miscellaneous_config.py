from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


@dataclass()
class MiscellaneousConfig(ConfigABC):
    """
    Class that validates and stores the Miscellaneous Configuration
    """
    _output_timestep_data_to_json: bool
    _random_seed: Optional[int]

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

    @property
    def random_seed(self) -> Optional[int]:
        """
        A random_seed used for the random number generators in
        both python and numpy to create a deterministic
        output for the game.
        """
        return self._random_seed

    @random_seed.setter
    def random_seed(self, value):
        self._random_seed = value


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
            _random_seed=config_dict["random_seed"]
        )

        return misc_config

    @classmethod
    def _validate(cls, config_dict: Dict[str, Any]):
        check_type(config_dict,"random_seed",[int,None])
