from __future__ import annotations

from typing import Optional

from yawning_titan.config.core import ConfigGroup
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties

# --- Tier 0 groups


class Reset(ConfigGroup):
    """The modifications to network performed on reset."""

    def __init__(
        self,
        randomise_vulnerabilities: Optional[bool] = False,
        choose_new_high_value_nodes: Optional[bool] = False,
        choose_new_entry_nodes: Optional[bool] = False,
    ):
        doc = "The changes to the network made upon reset"
        self.randomise_vulnerabilities = BoolItem(
            value=randomise_vulnerabilities,
            doc="Randomise the node vulnerabilities when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
            alias="randomise_vulnerabilities_on_reset",
        )
        self.choose_new_high_value_nodes = BoolItem(
            value=choose_new_high_value_nodes,
            doc="Choose new high value nodes when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
            alias="choose_new_high_value_nodes_on_reset",
        )
        self.choose_new_entry_nodes = BoolItem(
            value=choose_new_entry_nodes,
            doc="Choose new entry nodes when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
            alias="choose_new_entry_nodes_on_reset",
        )
        super().__init__(doc)
