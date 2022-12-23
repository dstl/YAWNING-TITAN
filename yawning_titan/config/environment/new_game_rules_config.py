from __future__ import annotations

from typing import Optional

from yawning_titan.config.toolbox.core import ConfigGroup
from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup, UseValueGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties

# --- Tier 0 groups


class NetworkCompatibility(ConfigGroup):
    """A set of optional restrictions that collectively constrain the types of network a game mode can be used upon."""

    def __init__(
        self,
        doc: Optional[str] = None,
        node_count: RestrictRangeGroup = RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of node counts"
        ),
        entry_node_count: RestrictRangeGroup = RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of entry_node_count counts"
        ),
        high_value_node_count: RestrictRangeGroup = RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of high_value_node_count counts"
        ),
    ):
        self.node_count = node_count
        self.entry_node_count = entry_node_count
        self.high_value_node_count = high_value_node_count
        super().__init__(doc)


class BlueLossConditionGroup(ConfigGroup):
    """The state of the network that must be reached for the red agent to win the game."""

    def __init__(
        self,
        doc: Optional[str] = None,
        all_nodes_lost: Optional[bool] = False,
        high_value_node_lost: Optional[bool] = False,
        target_node_lost: Optional[bool] = False,
        n_percent_nodes_lost: UseValueGroup = UseValueGroup(
            doc="The percentage of nodes that need to be lost for blue to lose"
        ),
    ):
        self.all_nodes_lost = BoolItem(
            value=all_nodes_lost,
            doc="The blue agent loses if all the nodes become compromised",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.high_value_node_lost = BoolItem(
            value=high_value_node_lost,
            doc="Blue loses if a special node designated as 'high value' is lost",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.target_node_lost = BoolItem(
            value=target_node_lost,
            doc="Blue loses if a target node it lost",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.n_percent_nodes_lost = n_percent_nodes_lost
        super().__init__(doc)


# --- Tier 1 groups ---


class GameRules(ConfigGroup):
    """The overall rules of the game mode."""

    def __init__(
        self,
        doc: Optional[str] = None,
        grace_period_length: Optional[int] = 0,
        max_steps: Optional[int] = 0,
        network_compatibility: NetworkCompatibility = NetworkCompatibility(
            doc="The range of networks the game mode can be played upn"
        ),
        blue_loss_condition: BlueLossConditionGroup = BlueLossConditionGroup(
            doc="The state of the network that must be reached for the red agent to win the game."
        ),
    ):
        self.grace_period_length = IntItem(
            value=grace_period_length,
            doc=(
                "The length of a grace period at the start of the game. During this time the red agent cannot act. "
                "This gives the blue agent a chance to 'prepare' (A length of 0 means that there is no grace period)"
            ),
            properties=IntProperties(allow_null=False, default=0),
        )
        self.max_steps = IntItem(
            value=max_steps,
            doc="The max steps that a game can go on for. If the blue agent reaches this they win",
            properties=IntProperties(allow_null=False, default=0),
        )
        self.network_compatibility = network_compatibility
        self.blue_loss_condition = blue_loss_condition
        super().__init__(doc)
