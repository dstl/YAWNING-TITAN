from __future__ import annotations

from typing import Optional

from yawning_titan.config.toolbox.groups.validation import AnyTrueGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties

# --- Tier 0 groups


class Reset(AnyTrueGroup):
    """The modifications to network performed on reset."""

    def __init__(
        self,
        doc: Optional[str] = None,
        randomise_vulnerabilities: Optional[bool] = False,
        choose_new_high_value_nodes: Optional[bool] = False,
        choose_new_entry_nodes: Optional[bool] = False,
    ):
        self.randomise_vulnerabilities = BoolItem(
            value=randomise_vulnerabilities,
            doc="Randomise the node vulnerabilities when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.choose_new_high_value_nodes = BoolItem(
            value=choose_new_high_value_nodes,
            doc="Choose new high value nodes when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.choose_new_entry_nodes = BoolItem(
            value=choose_new_entry_nodes,
            doc="Choose new entry nodes when the network is reset",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc)
