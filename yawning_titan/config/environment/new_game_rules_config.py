from __future__ import annotations

from typing import Optional

from yawning_titan.config.toolbox.core import ConfigGroup
from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup, UseValueGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties

# --- Tier 0 groups


class NetworkCompatibilityGroup(ConfigGroup):
    """A set of optional restrictions that collectively constrain the types of network a game mode can be used upon."""

    def __init__(
        self,
        doc: Optional[str] = None,
        node_count: Optional[RestrictRangeGroup] = None,
        entry_node_count: Optional[RestrictRangeGroup] = None,
        high_value_node_count: Optional[RestrictRangeGroup] = None
    ):
        self.node_count = node_count if node_count else RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of node counts"
        )
        self.entry_node_count = entry_node_count if entry_node_count else RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of entry_node_count counts"
        )
        self.high_value_node_count = high_value_node_count if high_value_node_count else RestrictRangeGroup(
            doc="Restrict the game mode to only work with network works within a range of high_value_node_count counts"
        )

        self.node_count.min.alias = "min_number_of_network_nodes"
        super().__init__(doc)


class BlueLossConditionGroup(ConfigGroup):
    """The state of the network that must be reached for the red agent to win the game."""

    def __init__(
        self,
        doc: Optional[str] = None,
        all_nodes_lost: Optional[bool] = False,
        high_value_node_lost: Optional[bool] = False,
        target_node_lost: Optional[bool] = False,
        n_percent_nodes_lost: Optional[UseValueGroup] = None
    ):
        self.all_nodes_lost = BoolItem(
            value=all_nodes_lost,
            doc="The blue agent loses if all the nodes become compromised",
            properties=BoolProperties(allow_null=True, default=False),
            alias="lose_when_all_nodes_lost"
        )
        self.high_value_node_lost = BoolItem(
            value=high_value_node_lost,
            doc="Blue loses if a special node designated as 'high value' is lost",
            properties=BoolProperties(allow_null=True, default=False),
            alias="lose_when_high_value_node_lost"
        )
        self.target_node_lost = BoolItem(
            value=target_node_lost,
            doc="Blue loses if a target node it lost",
            properties=BoolProperties(allow_null=True, default=False),
            alias="lose_when_target_node_lost"
        )
        self.n_percent_nodes_lost = n_percent_nodes_lost if n_percent_nodes_lost else UseValueGroup(
            doc="The percentage of nodes that need to be lost for blue to lose",
        )

        self.n_percent_nodes_lost.value.alias = "percentage_of_nodes_compromised_equals_loss"
        self.n_percent_nodes_lost.use.alias = "lose_when_n_percent_of_nodes_lost"
        super().__init__(doc)


# --- Tier 1 groups ---


class GameRules(ConfigGroup):
    """The overall rules of the game mode."""

    def __init__(
        self,
        doc: Optional[str] = None,
        grace_period_length: Optional[int] = 0,
        max_steps: Optional[int] = 0,
        blue_loss_condition: Optional[BlueLossConditionGroup] = None,
        network_compatibility: Optional[NetworkCompatibilityGroup] = None        
    ):
        self.grace_period_length = IntItem(
            value=grace_period_length,
            doc=(
                "The length of a grace period at the start of the game. During this time the red agent cannot act. "
                "This gives the blue agent a chance to 'prepare' (A length of 0 means that there is no grace period)"
            ),
            properties=IntProperties(allow_null=False, default=0, min_val=0, max_val=100, inclusive_min=True, inclusive_max=True),
            alias="grace_period_length"
        )
        self.max_steps = IntItem(
            value=max_steps,
            doc="The max steps that a game can go on for. If the blue agent reaches this they win",
            properties=IntProperties(allow_null=False, default=1, min_val=1, max_val=10_000_000, inclusive_min=True, inclusive_max=True),
            alias="max_steps"
        )
        self.blue_loss_condition: BlueLossConditionGroup = blue_loss_condition if blue_loss_condition else BlueLossConditionGroup(
            doc="The state of the network that must be reached for the red agent to win the game.",
        )
        self.network_compatibility: NetworkCompatibilityGroup = network_compatibility if network_compatibility else NetworkCompatibilityGroup(
            doc="The range of networks the game mode can be played upon"
        )
        super().__init__(doc)
