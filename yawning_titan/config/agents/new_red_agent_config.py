from __future__ import annotations
from typing import Optional
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties

from yawning_titan.config.item_types.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.config.item_types.grouped.action_likelihood_chance_group import ActionLikelihoodChanceGroup, ActionLikelihoodGroup
from yawning_titan.config.item_types.int_item import IntItem, IntProperties
from yawning_titan.exceptions import ConfigGroupValidationError


# # region Getters
# @property
# def red_skill(self) -> float:
#     """
#     Red Skill.

#     The red agents skill level. Higher means that red is more likely to
#     succeed in attacks.
#     """
#     return self._red_skill

# @property
# def red_uses_skill(self) -> bool:
#     """Red uses its skill modifier when attacking nodes."""
#     return self._red_uses_skill

# @property
# def red_ignores_defences(self) -> bool:
#     """The red agent ignores the defences of nodes."""
#     return self._red_ignores_defences

# @property
# def red_always_succeeds(self) -> bool:
#     """Reds attacks always succeed."""
#     return self._red_always_succeeds

# @property
# def red_can_only_attack_from_red_agent_node(self) -> bool:
#     """
#     Red can only attack from red agent node.

#     The red agent will only ever be in one node however it can control any
#     amount of nodes. Can the red agent only attack from its one main
#     node or can it attack from any node that it controls.
#     """
#     return self._red_can_only_attack_from_red_agent_node

# @property
# def red_can_attack_from_any_red_node(self) -> bool:
#     """
#     Red can attack from any node.

#     The red agent will only ever be in one node however it can control any
#     amount of nodes. Can the red agent only attack from its one main
#     node or can it attack from any node that it controls.
#     """
#     return self._red_can_attack_from_any_red_node

# @property
# def red_can_naturally_spread(self) -> bool:
#     """The red agent naturally spreads its influence every time-step."""
#     return self._red_can_naturally_spread

# @property
# def chance_to_spread_to_connected_node(self) -> float:
#     """
#     Chance to spread to connected node.

#     If a node is connected to a compromised node what chance does it have
#     to become compromised every turn through natural spreading.
#     """
#     return self._chance_to_spread_to_connected_node

# @property
# def chance_to_spread_to_unconnected_node(self) -> float:
#     """
#     Chance to spread to unconnected node.

#     If a node is not connected to a compromised node what chance does it
#     have to become randomly infected through natural spreading.
#     """
#     return self._chance_to_spread_to_unconnected_node

# @property
# def red_uses_spread_action(self) -> bool:
#     """Tries to spread to every node connected to an infected node."""
#     return self._red_uses_spread_action

# @property
# def spread_action_likelihood(self) -> float:
#     """Weighting for red_uses_spread_action."""
#     return self._spread_action_likelihood

# @property
# def chance_for_red_to_spread(self) -> float:
#     """Chance for each 'spread' to succeed."""
#     return self._chance_for_red_to_spread

# @property
# def red_uses_random_infect_action(self) -> bool:
#     """Tries to infect every safe node in the environment."""
#     return self._red_uses_random_infect_action

# @property
# def random_infect_action_likelihood(self) -> float:
#     """Weighting for red_uses_random_infect_action."""
#     return self._random_infect_action_likelihood

# @property
# def chance_for_red_to_random_compromise(self) -> float:
#     """Chance for each 'infect' to succeed."""
#     return self._chance_for_red_to_random_compromise

# @property
# def red_uses_basic_attack_action(self) -> bool:
#     """
#     Red uses basic attack action.

#     The red agent picks a single node connected to an infected node and
#     tries to attack and take over that node.
#     """
#     return self._red_uses_basic_attack_action

# @property
# def basic_attack_action_likelihood(self) -> float:
#     """Weighting for red_uses_basic_attack_action."""
#     return self._basic_attack_action_likelihood

# @property
# def red_uses_do_nothing_action(self) -> bool:
#     """The red agent does nothing."""
#     return self._red_uses_do_nothing_action

# @property
# def do_nothing_action_likelihood(self) -> float:
#     """Chance for red_uses_do_nothing_action."""
#     return self._do_nothing_action_likelihood

# @property
# def red_uses_move_action(self) -> bool:
#     """The red agent moves to a different node."""
#     return self._red_uses_move_action

# @property
# def move_action_likelihood(self) -> float:
#     """Chance of red_uses_move_action."""
#     return self._move_action_likelihood

# @property
# def red_uses_zero_day_action(self) -> bool:
#     """
#     Red uses zero day action.

#     The red agent will pick a safe node connected to an infected node and
#     take it over with a 100% chance to succeed (can only happen every n
#     timesteps).
#     """
#     return self._red_uses_zero_day_action

# @property
# def zero_day_start_amount(self) -> float:
#     """The number of zero-day attacks that the red agent starts with."""
#     return self._zero_day_start_amount

# @property
# def days_required_for_zero_day(self) -> int:
#     """The amount of 'progress' that need to have passed before the red agent gains a zero day attack."""
#     return self._days_required_for_zero_day

# @property
# def red_chooses_target_at_random(self) -> bool:
#     """Red picks nodes to attack at random."""
#     return self._red_chooses_target_at_random

# @property
# def red_target_node(self) -> str:
#     """Red targets a specific node."""
#     return self._red_target_node

# @property
# def red_prioritises_connected_nodes(self) -> bool:
#     """Red sorts the nodes it can attack and chooses the one that has the most connections."""
#     return self._red_prioritises_connected_nodes

# @property
# def red_prioritises_un_connected_nodes(self) -> bool:
#     """Red sorts the nodes it can attack and chooses the one that has the least connections."""
#     return self._red_prioritises_un_connected_nodes

# @property
# def red_prioritises_vulnerable_nodes(self) -> bool:
#     """Red sorts the nodes is can attack and chooses the one that is the most vulnerable."""
#     return self._red_prioritises_vulnerable_nodes

# @property
# def red_prioritises_resilient_nodes(self) -> bool:
#     """Red sorts the nodes is can attack and chooses the one that is the least vulnerable."""
#     return self._red_prioritises_resilient_nodes

# @property
# def red_always_chooses_shortest_distance_to_target(self) -> bool:
#     """Red always chooses the absolute shortest distance to target with no randomisation."""
#     return self._red_always_chooses_shortest_distance_to_target

class ZeroDayGroup(ConfigGroup):
    """
    Group of values that collectively describe the red zero day action.
    """
    def __init__(
        self, 
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        start_amount: Optional[int] = 0,
        days_required: Optional[int] = 0
    ):
        self.use:BoolItem = BoolItem(
            value=use,
            doc="The red agent will pick a safe node connected to an infected node and take it over with a 100% chance to succeed (can only happen every n timesteps).",
            properties=BoolProperties(allow_null=False)
        )
        self.start_amount:IntItem = IntItem(
            value=start_amount,
            doc="The number of zero-day attacks that the red agent starts with.",
            properties=IntProperties(allow_null=True,default=0,min_val=0,inclusive_min=True)
        )
        self.days_required:IntItem = IntItem(
            value=days_required,
            doc="The amount of 'progress' that need to have passed before the red agent gains a zero day attack.",
            properties=IntProperties(allow_null=True,default=0,min_val=0,inclusive_min=True)
        )
        super().__init__(doc)

class RedActionSetGroup(ConfigGroup):
    """The ConfigGroup to represent an action, likelihood, and chance common config group."""

    def __init__(
        self,
        spread: ActionLikelihoodChanceGroup = ActionLikelihoodChanceGroup(
            doc="Whether red tries to spread to every node connected to an infected node and the associated likelihood of this occurring."
        ),
        random_infect: ActionLikelihoodChanceGroup = ActionLikelihoodChanceGroup(
            doc="Whether red tries to infect every safe node in the environment and the associated likelihood of this occurring."
        ),
        move: ActionLikelihoodGroup = ActionLikelihoodGroup(
            doc="Whether the red agent moves to a different node and the associated likelihood of this occurring."
        ),
        basic_attack: ActionLikelihoodGroup = ActionLikelihoodGroup(
            doc="Whether the red agent picks a single node connected to an infected node and tries to attack and take over that node and the associated likelihood of this occurring."
        ),
        do_nothing: ActionLikelihoodGroup = ActionLikelihoodGroup(
            doc="Whether the red agent is able to perform no attack for a given turn and the likelihood of this occurring."
        ),
        zero_day: ZeroDayGroup = ZeroDayGroup(
            doc="Group of values that collectively describe the red zero day action."
        ),
        doc: Optional[str] = None,
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param spread: The likelihood of the action.
        :param random_infect: The chance of the action.
        :param doc: An optional descriptor.
        """
        self.spread = spread
        self.random_infect = random_infect
        self.move = move
        self.basic_attack = basic_attack
        self.do_nothing = do_nothing
        self.zero_day = zero_day
        
        super().__init__(doc)
    
    def validate(self) -> ConfigGroupValidation:
        try:
            if not any(e.use.value for e in self.get_config_elements().values()):
                msg = f"At least one of {', '.join(self.get_config_elements().keys())} should be used."
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation = ConfigGroupValidation(False, msg, e)
        
        super().validate()
        return self.validation
    
red_action_set = RedActionSetGroup()
red_action_set.set_from_dict({
    "spread":{
        "use":True,
        # "likelihood":2,
        # "chance": 3
    },
    "random_infect":{
        "use":False,
        "likelihood":4,
        "chance": 5
    },
    "move":{
        "use":False,
        "likelihood":6,
    },
    "basic_attack":{
        "use":False,
        "likelihood":"F",
    },
    "do_nothing":{
        "use":False,
        "likelihood":7,
    }
})
red_action_set.validation.log()