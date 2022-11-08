from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC


@dataclass()
class MiscellaneousConfig(ConfigGroupABC):
    """
    Class that validates and stores the Miscellaneous Configuration
    """

    output_timestep_data_to_json: bool = field(
        metadata="""
        Toggle to output a json file for each step that contains the connections between nodes, the states of the nodes and
        the attacks that blue saw in that turn
    """
    )
    """
    Toggle to output a json file for each step that contains the connections between nodes, the states of the nodes and
    the attacks that blue saw in that turn
    """

    @classmethod
    def create(cls, settings: Dict[str, Any]) -> MiscellaneousConfig:
        cls._validate(settings)

        misc_config = MiscellaneousConfig(
            output_timestep_data_to_json=settings["output_timestep_data_to_json"],
        )

        return misc_config

    @classmethod
    def _validate(cls, data: dict):
        pass
