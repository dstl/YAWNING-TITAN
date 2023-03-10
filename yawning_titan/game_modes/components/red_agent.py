from __future__ import annotations

from typing import Optional, Union

from yawning_titan.config.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.groups.core import (
    ActionLikelihoodChanceGroup,
    ActionLikelihoodGroup,
    UseValueGroup,
)
from yawning_titan.config.groups.validation import AnyNonZeroGroup, AnyUsedGroup
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.config.item_types.int_item import IntItem, IntProperties
from yawning_titan.config.item_types.str_item import StrItem, StrProperties
from yawning_titan.db.schemas import GameModeConfigurationSchema
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
            query=GameModeConfigurationSchema.RED.ACTION_SET.ZERO_DAY.USE,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_uses_zero_day_action",
        )
        self.start_amount: IntItem = IntItem(
            value=start_amount,
            doc="The number of zero-day attacks that the red agent starts with.",
            query=GameModeConfigurationSchema.RED.ACTION_SET.ZERO_DAY.START_AMOUNT,
            properties=IntProperties(
                allow_null=True, default=0, min_val=0, inclusive_min=True
            ),
            alias="zero_day_start_amount",
        )
        self.days_required: IntItem = IntItem(
            value=days_required,
            doc="The amount of 'progress' that need to have passed before the red agent gains a zero day attack.",
            query=GameModeConfigurationSchema.RED.ACTION_SET.ZERO_DAY.DAYS_REQUIRED,
            properties=IntProperties(
                allow_null=True, default=0, min_val=0, inclusive_min=True
            ),
            alias="days_required_for_zero_day",
        )
        super().__init__(doc)


class AttackSourceGroup(ConfigGroup):
    """The ConfigGroup to represent to the source of the red agents attacks."""

    def __init__(
        self,
        doc: Optional[str] = None,
        only_main_red_node: Optional[bool] = False,
        any_red_node: Optional[bool] = False,
    ):
        self.only_main_red_node = BoolItem(
            value=only_main_red_node,
            doc="Red agent can only attack from its main node on that turn.",
            query=GameModeConfigurationSchema.RED.AGENT_ATTACK.ATTACK_FROM.ONLY_MAIN_RED_NODE,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_can_only_attack_from_red_agent_node",
        )
        self.any_red_node = BoolItem(
            value=any_red_node,
            doc="Red can attack from any node that it controls.",
            query=GameModeConfigurationSchema.RED.AGENT_ATTACK.ATTACK_FROM.ANY_RED_NODE,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_can_attack_from_any_red_node",
        )

        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.only_main_red_node.value and self.any_red_node.value:
                msg = (
                    "The red agent cannot attack from multiple sources simultaneously."
                )
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class NaturalSpreadChanceGroup(ConfigGroup):
    """The ConfigGroup to represent the chances of reads natural spreading to different node types."""

    def __init__(
        self,
        doc: Optional[str] = None,
        to_connected_node: Optional[Union[int, float]] = 0,
        to_unconnected_node: Optional[Union[int, float]] = 0,
    ):
        self.doc = doc
        self.to_connected_node = FloatItem(
            value=to_connected_node,
            doc=" If a node is connected to a compromised node what chance does it have to become compromised every turn through natural spreading.",
            query=GameModeConfigurationSchema.RED.NATURAL_SPREADING.CHANCE.TO_CONNECTED_NODE,
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias="chance_to_spread_to_connected_node",
        )
        self.to_unconnected_node = FloatItem(
            value=to_unconnected_node,
            doc="If a node is not connected to a compromised node what chance does it have to become randomly infected through natural spreading.",
            query=GameModeConfigurationSchema.RED.NATURAL_SPREADING.CHANCE.TO_UNCONNECTED_NODE,
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias="chance_to_spread_to_unconnected_node",
        )
        super().__init__()


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
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.TARGET_SPECIFIC_NODE.USE,
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.target: StrItem = StrItem(
            value=target,
            doc="The name of a node that the red agent targets.",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.TARGET_SPECIFIC_NODE.TARGET,
            properties=StrProperties(allow_null=True),
            alias="red_target_node",
        )
        self.always_choose_shortest_distance: BoolItem = BoolItem(
            value=always_choose_shortest_distance,
            doc="Whether red should pick the absolute shortest distance to the target node or choose nodes to attack based on a chance weighted inversely by distance",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.TARGET_SPECIFIC_NODE.ALWAYS_CHOOSE_SHORTEST_DISTANCE,
            properties=BoolProperties(allow_null=True),
            alias="red_always_chooses_shortest_distance_to_target",
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.target.value and not self.use.value:
                msg = f"Red is set to target {self.target.value}, if the red agent is set to a specific node then the element must have `used` set to True"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


# --- Tier 1 groups ---


class RedActionSetGroup(AnyUsedGroup):
    """The ConfigGroup to represent all permissable actions the red agent can perform."""

    def __init__(
        self,
        doc: Optional[str] = "All permissable actions the red agent can perform.",
        spread: Optional[ActionLikelihoodChanceGroup] = None,
        random_infect: Optional[ActionLikelihoodChanceGroup] = None,
        move: Optional[ActionLikelihoodGroup] = None,
        basic_attack: Optional[ActionLikelihoodGroup] = None,
        do_nothing: Optional[ActionLikelihoodGroup] = None,
        zero_day: Optional[ZeroDayGroup] = None,
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param spread: The likelihood of the action.
        :param random_infect: The chance of the action.
        :param doc: An optional descriptor.
        """
        self.spread: ActionLikelihoodChanceGroup = (
            spread
            if spread
            else ActionLikelihoodChanceGroup(
                doc="Whether red tries to spread to every node connected to an infected node and the associated likelihood of this occurring."
            )
        )
        self.random_infect: ActionLikelihoodChanceGroup = (
            random_infect
            if random_infect
            else ActionLikelihoodChanceGroup(
                doc="Whether red tries to infect every safe node in the environment and the associated likelihood of this occurring."
            )
        )
        self.move: ActionLikelihoodGroup = (
            move
            if move
            else ActionLikelihoodGroup(
                doc="Whether the red agent moves to a different node and the associated likelihood of this occurring."
            )
        )
        self.basic_attack: ActionLikelihoodGroup = (
            basic_attack
            if basic_attack
            else ActionLikelihoodGroup(
                doc="Whether the red agent picks a single node connected to an infected node and tries to attack and take over that node and the associated likelihood of this occurring."
            )
        )
        self.do_nothing: ActionLikelihoodGroup = (
            do_nothing
            if do_nothing
            else ActionLikelihoodGroup(
                doc="Whether the red agent is able to perform no attack for a given turn and the likelihood of this occurring."
            )
        )
        self.zero_day: ZeroDayGroup = (
            zero_day
            if zero_day
            else ZeroDayGroup(
                doc="Group of values that collectively describe the red zero day action."
            )
        )

        self.spread.use.alias = "red_uses_spread_action"
        self.spread.use.query = GameModeConfigurationSchema.RED.ACTION_SET.SPREAD.USE

        self.random_infect.use.alias = "red_uses_random_infect_action"
        self.random_infect.use.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.RANDOM_INFECT.USE
        )

        self.move.use.alias = "red_uses_move_action"
        self.move.use.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.RANDOM_INFECT.USE
        )

        self.basic_attack.use.alias = "red_uses_basic_attack_action"
        self.basic_attack.use.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.BASIC_ATTACK.USE
        )

        self.do_nothing.use.alias = "red_uses_do_nothing_action"
        self.do_nothing.use.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.DO_NOTHING.USE
        )

        self.spread.likelihood.alias = "spread_action_likelihood"
        self.spread.likelihood.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.SPREAD.LIKELIHOOD
        )

        self.random_infect.likelihood.alias = "random_infect_action_likelihood"
        self.random_infect.likelihood.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.RANDOM_INFECT.LIKELIHOOD
        )

        self.move.likelihood.alias = "move_action_likelihood"
        self.move.likelihood.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.MOVE.LIKELIHOOD
        )

        self.basic_attack.likelihood.alias = "basic_attack_action_likelihood"
        self.basic_attack.likelihood.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.BASIC_ATTACK.LIKELIHOOD
        )

        self.do_nothing.likelihood.alias = "do_nothing_action_likelihood"
        self.do_nothing.likelihood.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.DO_NOTHING.LIKELIHOOD
        )

        self.spread.chance.alias = "chance_for_red_to_spread"
        self.spread.chance.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.SPREAD.CHANCE
        )

        self.random_infect.chance.alias = "chance_for_red_to_random_compromise"
        self.random_infect.chance.query = (
            GameModeConfigurationSchema.RED.ACTION_SET.RANDOM_INFECT.CHANCE
        )

        super().__init__(doc)


class RedAgentAttackGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents attacks."""

    def __init__(
        self,
        doc: Optional[
            str
        ] = "The ConfigGroup to represent the information related to the red agents attacks.",
        ignores_defences: Optional[bool] = False,
        always_succeeds: Optional[bool] = False,
        skill: Optional[UseValueGroup] = None,
        attack_from: Optional[AttackSourceGroup] = None,
    ):
        self.ignores_defences = BoolItem(
            value=ignores_defences,
            doc="The red agent ignores the defences of nodes.",
            query=GameModeConfigurationSchema.RED.AGENT_ATTACK.IGNORES_DEFENCES,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_ignores_defences",
        )
        self.always_succeeds = BoolItem(
            value=always_succeeds,
            doc="Reds attacks always succeed.",
            query=GameModeConfigurationSchema.RED.AGENT_ATTACK.ALWAYS_SUCCEEDS,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_always_succeeds",
        )
        self.skill = (
            skill
            if skill
            else UseValueGroup(doc="Red uses its skill modifier when attacking nodes.")
        )
        self.attack_from = (
            attack_from
            if attack_from
            else AttackSourceGroup(
                doc=(
                    "The red agent will only ever be in one node however it can control any amount of nodes. "
                    "Can the red agent only attack from its one main node or can it attack from any node that it controls."
                )
            )
        )

        self.skill.use.alias = "red_uses_skill"
        self.skill.use.query = GameModeConfigurationSchema.RED.AGENT_ATTACK.SKILL.USE

        self.skill.value.alias = "red_skill"
        self.skill.value.query = (
            GameModeConfigurationSchema.RED.AGENT_ATTACK.SKILL.VALUE
        )

        super().__init__(doc)


class RedNaturalSpreadingGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents natural spreading ability."""

    def __init__(
        self,
        doc: Optional[str] = None,
        capable: Optional[bool] = False,
        chance: Optional[NaturalSpreadChanceGroup] = None,
    ):
        self.capable = BoolItem(
            value=capable,
            doc="Whether the red agents infection can naturally spread to surrounding nodes",
            query=GameModeConfigurationSchema.RED.NATURAL_SPREADING.CAPABLE,
            properties=BoolProperties(allow_null=False, default=False),
            alias="red_can_naturally_spread",
        )
        self.chance = (
            chance
            if chance
            else NaturalSpreadChanceGroup(
                doc="the chances of reads natural spreading to different node types."
            )
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        if self.capable.value:
            try:
                elements = self.chance.get_config_elements([IntItem, FloatItem])
                if not any(
                    e.value > 0 for e in elements.values() if type(e.value) in [int, float]
                ):
                    msg = f"At least 1 of {', '.join(elements.keys())} should be above 0"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation


class RedTargetMechanismGroup(AnyUsedGroup):
    """The ConfigGroup to represent all possible target mechanism the red agent can use."""

    def __init__(
        self,
        doc: Optional[str] = None,
        random: Optional[bool] = False,
        prioritise_connected_nodes: Optional[bool] = False,
        prioritise_unconnected_nodes: Optional[bool] = False,
        prioritise_vulnerable_nodes: Optional[bool] = False,
        prioritise_resilient_nodes: Optional[bool] = False,
        target_specific_node: Optional[TargetNodeGroup] = None,
    ):
        self.random = BoolItem(
            doc="Red randomly chooses nodes to target",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.RANDOM,
            value=random,
            properties=BoolProperties(default=False, allow_null=True),
            alias="red_chooses_target_at_random",
        )
        self.prioritise_connected_nodes = BoolItem(
            doc="Red sorts the nodes it can attack and chooses the one that has the most connections",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.PRIORITISE_CONNECTED_NODES,
            value=prioritise_connected_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias="red_prioritises_connected_nodes",
        )
        self.prioritise_unconnected_nodes = BoolItem(
            doc="Red sorts the nodes it can attack and chooses the one that has the least connections",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.PRIORITISE_UNCONNECTED_NODES,
            value=prioritise_unconnected_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias="red_prioritises_un_connected_nodes",
        )
        self.prioritise_vulnerable_nodes = BoolItem(
            doc="Red sorts the nodes is can attack and chooses the one that is the most vulnerable",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.PRIORITISE_VULNERABLE_NODES,
            value=prioritise_vulnerable_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias="red_prioritises_vulnerable_nodes",
        )
        self.prioritise_resilient_nodes = BoolItem(
            doc="Red sorts the nodes is can attack and chooses the one that is the least vulnerable",
            query=GameModeConfigurationSchema.RED.TARGET_MECHANISM.PRIORITISE_RESILIENT_NODES,
            value=prioritise_resilient_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias="red_prioritises_resilient_nodes",
        )
        self.target_specific_node = (
            target_specific_node
            if target_specific_node
            else TargetNodeGroup(
                doc="The Config group to represent the information relevant to the red agents target node."
            )
        )
        super().__init__(doc)


# --- Tier 2 group ---


class Red(ConfigGroup):
    """The ConfigGroup to represent all items necessary to configure the Red agent."""

    def __init__(
        self,
        doc: Optional[str] = None,
        agent_attack: Optional[RedAgentAttackGroup] = None,
        action_set: Optional[RedActionSetGroup] = None,
        natural_spreading: Optional[RedNaturalSpreadingGroup] = None,
        target_mechanism: Optional[RedTargetMechanismGroup] = None,
    ):
        doc = "The configuration of the red agent"
        self.agent_attack = (
            agent_attack
            if agent_attack
            else RedAgentAttackGroup(
                doc="All information related to the red agents attacks."
            )
        )
        self.action_set = (
            action_set
            if action_set
            else RedActionSetGroup(
                doc="All permissable actions the red agent can perform."
            )
        )
        self.natural_spreading = (
            natural_spreading
            if natural_spreading
            else RedNaturalSpreadingGroup(
                doc="The information related to the red agents natural spreading ability."
            )
        )
        self.target_mechanism = (
            target_mechanism
            if target_mechanism
            else RedTargetMechanismGroup(
                doc="all possible target mechanism the red agent can use."
            )
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()

        try:
            if self.agent_attack.ignores_defences.value and (
                self.target_mechanism.prioritise_vulnerable_nodes.value
                or self.target_mechanism.prioritise_resilient_nodes.value
            ):
                msg = "If the red agent ignores defences then targeting based on this trait is impossible as it is ignored."
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)

        return self.validation
