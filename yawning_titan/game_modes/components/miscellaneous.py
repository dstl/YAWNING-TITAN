from __future__ import annotations

from typing import Optional

from yawning_titan.config.toolbox.core import ConfigGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.db.schemas import GameModeConfigurationSchema

# --- Tier 0 groups


class Miscellaneous(ConfigGroup):
    """Miscellaneous settings."""

    def __init__(
        self,
        doc: Optional[str] = None,
        random_seed: Optional[int] = None,
        output_timestep_data_to_json: Optional[bool] = False,
    ):
        self.random_seed = IntItem(
            value=random_seed,
            doc="Seed to inform the random number generation of python and numpy thereby creating deterministic game outputs",
            query=GameModeConfigurationSchema.MISCELLANEOUS.RANDOM_SEED,
            properties=IntProperties(allow_null=True),
            alias="random_seed",
        )
        self.output_timestep_data_to_json = BoolItem(
            value=output_timestep_data_to_json,
            doc="Toggle to output a json file for each step that contains the connections between nodes, the states of the nodes and the attacks that blue saw in that turn",
            query=GameModeConfigurationSchema.MISCELLANEOUS.OUTPUT_TIMESTEP_DATA_TO_JSON,
            properties=BoolProperties(allow_null=True, default=False),
            alias="output_timestep_data_to_json",
        )

        super().__init__(doc)
