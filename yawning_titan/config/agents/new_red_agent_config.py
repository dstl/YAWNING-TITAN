from __future__ import annotations

from typing import Optional, Union

from yawning_titan.config.toolbox.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.toolbox.groups.core import (
    ActionLikelihoodChanceGroup,
    ActionLikelihoodGroup,
    UseValueGroup,
)
from yawning_titan.config.toolbox.groups.validation import AnyNonZeroGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.float_item import (
    FloatItem,
    FloatProperties,
)
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.config.toolbox.item_types.str_item import StrItem, StrProperties
from yawning_titan.exceptions import ConfigGroupValidationError


# -- Tier 0 groups ---
class ZeroDayGroup(ConfigGroup):
    """Group of values that collectively describe the red zero day action."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        start_amount: Optional[int] = 0,
        days_required: Optional[int] = 0,
    ):
        self.use: BoolItem = BoolItem(
            value=use,
            doc="The red agent will pick a safe node connected to an infected node and take it over with a 100% chance to succeed (can only happen every n timesteps).",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.start_amount: IntItem = IntItem(
            value=start_amount,
            doc="The number of zero-day attacks that the red agent starts with.",
            properties=IntProperties(
                allow_null=True, default=0, min_val=0, inclusive_min=True
            ),
        )
        self.days_required: IntItem = IntItem(
            value=days_required,
            doc="The amount of 'progress' that need to have passed before the red agent gains a zero day attack.",
            properties=IntProperties(
                allow_null=True, default=0, min_val=0, inclusive_min=True
            ),
        )
        super().__init__(doc)


class AttackSourceGroup(ConfigGroup):
    """The ConfigGroup to represent to the source of the red agents attacks."""

    def __init__(
        self,
        doc: Optional[str] = None,
        only_red_agent_node: Optional[bool] = False,
        any_red_node: Optional[bool] = False,
    ):
        self.only_red_agent_node = BoolItem(
            value=only_red_agent_node,
            doc="Red agent can only attack from its main node on that turn.",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.any_red_node = BoolItem(
            value=any_red_node,
            doc="Red can attack from any node that it controls.",
            properties=BoolProperties(allow_null=False, default=False),
        )

        super().__init__(doc)


class NaturalSpreadChanceGroup(AnyNonZeroGroup):
    """The ConfigGroup to represent the chances of reads natural spreading to different node types."""

    def __init__(
        self,
        doc: Optional[str] = None,
        to_connected_node: Optional[Union[int, float]] = 0,
        to_unconnected_node: Optional[Union[int, float]] = 0,
    ):
        self.to_connected_node = FloatItem(
            value=to_connected_node,
            doc=" If a node is connected to a compromised node what chance does it have to become compromised every turn through natural spreading.",
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
        )
        self.to_unconnected_node = FloatItem(
            value=to_unconnected_node,
            doc="If a node is not connected to a compromised node what chance does it have to become randomly infected through natural spreading.",
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
        )
        print("NAT SPREAD CHANCE")
        super().__init__(doc)


class TargetNodeGroup(ConfigGroup):
    """The Config group to represent the information relevant to the red agents target node."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        target: Optional[str] = None,
        always_choose_shortest_distance: Optional[bool] = False,
    ):
        self.use: BoolItem = BoolItem(
            value=use,
            doc="Red targets a specific node.",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.target: StrItem = StrItem(
            value=target,
            doc="The name of a node that the red agent targets.",
            properties=StrProperties(allow_null=False),
        )
        self.always_choose_shortest_distance: BoolItem = BoolItem(
            value=always_choose_shortest_distance,
            doc="Whether red should pick the absolute shortest distance to the target node or choose nodes to attack based on a chance weighted inversely by distance",
            properties=BoolProperties(allow_null=True),
        )
        super().__init__(doc)


# --- Tier 1 groups ---


class RedActionSetGroup(ConfigGroup):
    """The ConfigGroup to represent all permissable actions the red agent can perform."""

    def __init__(
        self,
        doc: Optional[str] = "All permissable actions the red agent can perform.",
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
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()

        try:
            if not any(e.use.value for e in self.get_config_elements().values()):
                msg = f"At least one of {', '.join(self.get_config_elements().keys())} should be used."
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)

        return self.validation


class RedAgentAttackGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents attacks."""

    def __init__(
        self,
        doc: Optional[
            str
        ] = "The ConfigGroup to represent the information related to the red agents attacks.",
        ignores_defences: Optional[bool] = False,
        always_succeeds: Optional[bool] = False,
        skill: UseValueGroup = UseValueGroup(
            doc="Red uses its skill modifier when attacking nodes."
        ),
        attack_from: AttackSourceGroup = AttackSourceGroup(
            doc=(
                "The red agent will only ever be in one node however it can control any amount of nodes. "
                "Can the red agent only attack from its one main node or can it attack from any node that it controls."
            )
        ),
    ):
        self.ignores_defences = BoolItem(
            value=ignores_defences,
            doc="The red agent ignores the defences of nodes.",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.always_succeeds = BoolItem(
            value=always_succeeds,
            doc="Reds attacks always succeed.",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.skill = skill
        self.attack_from = attack_from
        super().__init__(doc)


class RedNaturalSpreadingGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents natural spreading ability."""

    def __init__(
        self,
        doc: Optional[
            str
        ] = "The information related to the red natural agents spreading ability.",
        capable: Optional[bool] = False,
        chance: NaturalSpreadChanceGroup = NaturalSpreadChanceGroup(
            doc="the chances of reads natural spreading to different node types."
        ),
    ):
        self.capable = capable
        self.chance = chance
        super().__init__(doc)


class RedTargetMechanismGroup(ConfigGroup):
    """The ConfigGroup to represent all possible target mechanism the red agent can use."""

    def __init__(
        self,
        doc: Optional[str] = None,
        random: Optional[bool] = False,
        prioritise_connected_nodes: Optional[bool] = False,
        prioritise_unconnected_nodes: Optional[bool] = False,
        prioritise_vulnerable_nodes: Optional[bool] = False,
        prioritise_resilient_nodes: Optional[bool] = False,
        target: TargetNodeGroup = TargetNodeGroup(
            doc="The Config group to represent the information relevant to the red agents target node."
        ),
    ):
        self.random = random
        self.prioritise_connected_nodes = prioritise_connected_nodes
        self.prioritise_unconnected_nodes = prioritise_unconnected_nodes
        self.prioritise_vulnerable_nodes = prioritise_vulnerable_nodes
        self.prioritise_resilient_nodes = prioritise_resilient_nodes
        self.target = target
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()
        try:
            if not self.random and not any(
                v is True
                for v in [
                    self.prioritise_connected_nodes,
                    self.prioritise_unconnected_nodes,
                    self.prioritise_vulnerable_nodes,
                    self.prioritise_resilient_nodes,
                    self.target.use.value,
                ]
            ):
                msg = "If the red agent does not target nodes randomly a method of targeting nodes must be set."
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


# --- Tier 2 group ---


class Red(ConfigGroup):
    """The ConfigGroup to represent all items necessary to configure the Red agent."""

    def __init__(
        self,
        doc: Optional[str] = None,
        agent_attack: RedAgentAttackGroup = RedAgentAttackGroup(
            doc="All information related to the red agents attacks."
        ),
        action_set: RedActionSetGroup = RedActionSetGroup(
            doc="All permissable actions the red agent can perform."
        ),
        natural_spreading: RedNaturalSpreadingGroup = RedNaturalSpreadingGroup(
            doc="The information related to the red agents natural spreading ability."
        ),
        target_mechanism: RedTargetMechanismGroup = RedTargetMechanismGroup(
            doc="all possible target mechanism the red agent can use."
        ),
    ):
        self.agent_attack = agent_attack
        self.action_set = action_set
        self.natural_spreading = natural_spreading
        self.target_mechanism = target_mechanism
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()

        try:
            if self.agent_attack.ignores_defences and (
                self.target_mechanism.prioritise_vulnerable_nodes
                or self.target_mechanism.prioritise_resilient_nodes
            ):
                msg = "If the red agent ignores defences then targeting based on this trait is impossible as it is ignored."
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)

        return self.validation


# target_mechanism = RedTargetMechanismGroup()

# target_mechanism.set_from_dict({
#     "random": True,
#     "prioritise_connected_nodes": 0,
#     "prioritise_unconnected_nodes": False,
#     "prioritise_vulnerable_nodes": False,
#     "prioritise_resilient_nodes": False,
#     "target_node":{
#         "use": False,
#         #"target": "",
#         "always_choose_shortest_distance": False
#     }
# })

# target_mechanism.validation.log("target_mechanism")

# natural_spread = RedNaturalSpreadingGroup()
# natural_spread.set_from_dict({
#     "capable": True,
#     "chance":{
#         "to_connected_node": 0.5,
#         "to_unconnected_node": 0.5
#     }
# })

# natural_spread.validation.log("natural_spread")

# red_action_set = RedActionSetGroup()
# red_action_set.set_from_dict({
#     "spread":{
#         "use":False,
#         "likelihood": 5,
#         "chance": 5
#     },
#     "random_infect":{
#         "use":False,
#         "likelihood": 0.5,
#         "chance": 0.5
#     },
#     "move":{
#         "use":False,
#         "likelihood":0.5,
#     },
#     "basic_attack":{
#         "use":False,
#         "likelihood":0.5,
#     },
#     "do_nothing":{
#         "use":False,
#         "likelihood":0.5,
#     },
#     "zero_day":{
#         "use":False,
#         "likelihood":0.5,
#     },
# })

# print(red_action_set.spread.validation)
# red_action_set.validation.log("action_set")


# red_attack = RedAgentAttackGroup()
# red_attack.set_from_dict({
#     "ignores_defences": True,
#     "always_succeeds": False,
#     "skill": {
#         "use": False
#     },
#     "attack_from": {
#         "only_red_agent_node": True
#     }
# })
# print(red_attack.to_dict())
# red_attack.validation.log()


red = Red()
red.set_from_dict(
    {
        "agent_attack": {
            "ignores_defences": False,
            "always_succeeds": False,
            "skill": {"use": True, "value": 0.5},
            "attack_from": {"only_red_node": False, "any_red_node": True},
        },
        "action_set": {
            "spread": {"use": False, "likelihood": 0.5, "chance": 0.5},
            "random_infect": {"use": False, "likelihood": 0.5, "chance": 0.5},
            "move": {
                "use": False,
                "likelihood": 0.5,
            },
            "basic_attack": {
                "use": False,
                "likelihood": 0.5,
            },
            "do_nothing": {
                "use": False,
                "likelihood": 0.5,
            },
            "zero_day": {
                "use": False,
                "likelihood": 0.5,
            },
        },
        "natural_spreading": {
            "capable": True,
            "chance": {"to_connected_node": 0.5, "to_unconnected_node": 0.5},
        },
        "target_mechanism": {
            "random": True,
            "prioritise_connected_nodes": False,
            "prioritise_unconnected_nodes": False,
            "prioritise_vulnerable_nodes": False,
            "prioritise_resilient_nodes": False,
            "target_node": {
                "use": False,
                # "target": "",
                "always_choose_shortest_distance": False,
            },
        },
    }
)

red.validation.log("red")
