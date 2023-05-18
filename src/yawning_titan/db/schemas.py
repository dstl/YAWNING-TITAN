from __future__ import annotations

from typing import Final

from yawning_titan.db.query import YawningTitanQuery

# generic


# Game Rules
class NodeCountSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RESTRICT: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.node_count.restrict
    MIN: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.node_count.min
    MAX: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.node_count.max


class EntryNodeCountSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RESTRICT: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.entry_node_count.restrict
    MIN: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.entry_node_count.min
    MAX: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.entry_node_count.max


class HighValueNodeCountSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RESTRICT: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().game_rules.network_compatibility.high_value_node_count.restrict
    )
    MIN: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.high_value_node_count.min
    MAX: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.network_compatibility.high_value_node_count.max


class NetworkCompatibilitySchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    NODE_COUNT: Final[NodeCountSchema] = NodeCountSchema
    ENTRY_NODE_COUNT: Final[EntryNodeCountSchema] = EntryNodeCountSchema
    HIGH_VALUE_NODE_COUNT: Final[HighValueNodeCountSchema] = HighValueNodeCountSchema


class NPercentNodesLostSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.blue_loss_condition.n_percent_nodes_lost.use
    VALUE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.blue_loss_condition.n_percent_nodes_lost.value


class BlueLossConditionSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    ALL_NODES_LOST: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.blue_loss_condition.all_nodes_lost
    HIGH_VALUE_NODE_LOST: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.blue_loss_condition.high_value_node_lost
    TARGET_NODE_LOST: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.blue_loss_condition.target_node_lost
    N_PERCENT_NODES_LOST: Final[NPercentNodesLostSchema] = NPercentNodesLostSchema


# Blue Agent


class MakeNodeSafeSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.make_node_safe.use
    INCREASES_VULNERABILITY: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.make_node_safe.increases_vulnerability
    GIVES_RANDOM_VULNERABILITY: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.make_node_safe.gives_random_vulnerability
    VULNERABILITY_CHANGE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.make_node_safe.vulnerability_change


class DeceptiveNodeSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.deceptive_nodes.use
    MAX_NUMBER: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.deceptive_nodes.max_number
    NEW_NODE_ON_RELOCATE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.deceptive_nodes.new_node_on_relocate


class BlueActionSetSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    REDUCE_VULNERABILITY: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.reduce_vulnerability
    RESTORE_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.restore_node
    SCAN: Final[YawningTitanQuery] = YawningTitanQuery().blue.action_set.scan
    ISOLATE_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.isolate_node
    RECONNECT_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.reconnect_node
    DO_NOTHING: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.action_set.do_nothing
    MAKE_NODE_SAFE: Final[MakeNodeSafeSchema] = MakeNodeSafeSchema
    DECEPTIVE_NODES: Final[DeceptiveNodeSchema] = DeceptiveNodeSchema


class OnScanSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    STANDARD_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.intrusion_discovery_chance.on_scan.standard_node
    DECEPTIVE_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.intrusion_discovery_chance.on_scan.deceptive_node


class ImmediateSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    STANDARD_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.intrusion_discovery_chance.immediate.standard_node
    DECEPTIVE_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.intrusion_discovery_chance.immediate.deceptive_node


class BlueIntrusionDiscoverySchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    IMMEDIATE: Final[ImmediateSchema] = ImmediateSchema
    ON_SCAN: Final[OnScanSchema] = OnScanSchema


class FailedAttackChanceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    STANDARD_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.attack_discovery.failed_attacks.chance.standard_node
    DECEPTIVE_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.attack_discovery.failed_attacks.chance.deceptive_node


class FailedAttackSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.attack_discovery.failed_attacks.use
    CHANCE: Final[FailedAttackChanceSchema] = FailedAttackChanceSchema


class SucceededAttackKnownCompromiseChanceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    STANDARD_NODE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().blue.attack_discovery.succeeded_attacks_known_compromise.chance.standard_node
    )
    DECEPTIVE_NODE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().blue.attack_discovery.succeeded_attacks_known_compromise.chance.deceptive_node
    )


class SucceededAttackKnownCompromiseSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().blue.attack_discovery.succeeded_attacks_known_compromise.use
    CHANCE: Final[
        SucceededAttackKnownCompromiseChanceSchema
    ] = SucceededAttackKnownCompromiseChanceSchema


class SucceededAttackUnknownCompromiseChanceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    STANDARD_NODE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().blue.attack_discovery.succeeded_attacks_unknown_compromise.chance.standard_node
    )
    DECEPTIVE_NODE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().blue.attack_discovery.succeeded_attacks_unknown_compromise.chance.deceptive_node
    )


class SucceededAttackUnknownCompromiseSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().blue.attack_discovery.succeeded_attacks_unknown_compromise.use
    )
    CHANCE: Final[
        SucceededAttackUnknownCompromiseChanceSchema
    ] = SucceededAttackUnknownCompromiseChanceSchema


class BlueAttackDiscoverySchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    FAILED_ATTACKS: Final[FailedAttackSchema] = FailedAttackSchema
    SUCCEEDED_ATTACKS_KNOWN_COMPROMISE: Final[
        SucceededAttackKnownCompromiseSchema
    ] = SucceededAttackKnownCompromiseSchema
    SUCCEEDED_ATTACKS_UNKNOWN_COMPROMISE: Final[
        SucceededAttackUnknownCompromiseSchema
    ] = SucceededAttackUnknownCompromiseSchema


# Red Agent
class ZeroDaySchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.zero_day.use
    START_AMOUNT: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.zero_day.start_amount
    DAYS_REQUIRED: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.zero_day.days_required


class AttackSourceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    ONLY_MAIN_RED_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.agent_attack.attack_from.only_main_red_node
    ANY_RED_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.agent_attack.attack_from.any_red_node


class NaturalSpreadChanceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    TO_CONNECTED_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.natural_spreading.chance.to_connected_node
    TO_UNCONNECTED_NODE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.natural_spreading.chance.to_unconnected_node


class TargetNodeSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.target_specific_node.use
    TARGET: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.target_specific_node.target
    ALWAYS_CHOOSE_SHORTEST_DISTANCE: Final[
        YawningTitanQuery
    ] = (
        YawningTitanQuery().red.target_mechanism.target_specific_node.always_choose_shortest_distance
    )


class SpreadSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.spread.use
    LIKELIHOOD: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.spread.likelihood
    CHANCE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.spread.chance


class RandomInfectSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.random_infect.use
    LIKELIHOOD: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.random_infect.likelihood
    CHANCE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.random_infect.chance


class MoveSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.move.use
    LIKELIHOOD: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.move.likelihood


class BasicAttackSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.basic_attack.use
    LIKELIHOOD: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.basic_attack.likelihood


class DoNothingSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.action_set.do_nothing.use
    LIKELIHOOD: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.action_set.do_nothing.likelihood


class RedActionSetSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    SPREAD: Final[SpreadSchema] = SpreadSchema
    RANDOM_INFECT: Final[RandomInfectSchema] = RandomInfectSchema
    MOVE: Final[MoveSchema] = MoveSchema
    BASIC_ATTACK: Final[BasicAttackSchema] = BasicAttackSchema
    DO_NOTHING: Final[DoNothingSchema] = DoNothingSchema
    ZERO_DAY: Final[ZeroDaySchema] = ZeroDaySchema


class SkillSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    USE: Final[YawningTitanQuery] = YawningTitanQuery().red.agent_attack.skill.use
    VALUE: Final[YawningTitanQuery] = YawningTitanQuery().red.agent_attack.skill.value


class RedAgentAttackSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    IGNORES_DEFENCES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.agent_attack.ignores_defences
    ALWAYS_SUCCEEDS: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.agent_attack.always_succeeds
    SKILL: Final[SkillSchema] = SkillSchema
    ATTACK_FROM: Final[AttackSourceSchema] = AttackSourceSchema


class RedNaturalSpreadingSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    CAPABLE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.natural_spreading.capable
    CHANCE: Final[NaturalSpreadChanceSchema] = NaturalSpreadChanceSchema


class RedTargetMechanismSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RANDOM: Final[YawningTitanQuery] = YawningTitanQuery().red.target_mechanism.random
    PRIORITISE_CONNECTED_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.prioritise_connected_nodes
    PRIORITISE_UNCONNECTED_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.prioritise_unconnected_nodes
    PRIORITISE_VULNERABLE_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.prioritise_vulnerable_nodes
    PRIORITISE_RESILIENT_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().red.target_mechanism.prioritise_resilient_nodes
    TARGET_SPECIFIC_NODE: Final[TargetNodeSchema] = TargetNodeSchema


# Game Mode Sections


class ResetSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RANDOMISE_VULNERABILITIES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().on_reset.randomise_vulnerabilities
    CHOOSE_NEW_HIGH_VALUE_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().on_reset.choose_new_high_value_nodes
    CHOOSE_NEW_ENTRY_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().on_reset.choose_new_entry_nodes


class RewardsSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    FOR_LOSS: Final[YawningTitanQuery] = YawningTitanQuery().reward.for_loss
    FOR_REACHING_MAX_STEPS: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().reward.for_reaching_max_steps
    END_REWARDS_ARE_MULTIPLIED_BY_END_STATE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().reward.end_rewards_are_multiplied_by_end_state
    REDUCE_NEGATIVE_REWARDS_FOR_CLOSER_FAILS: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().reward.reduce_negative_rewards_for_closer_fails
    FUNCTION: Final[YawningTitanQuery] = YawningTitanQuery().reward.function


class MiscellaneousSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RANDOM_SEED: Final[YawningTitanQuery] = YawningTitanQuery().miscellaneous.for_loss
    OUTPUT_TIMESTEP_DATA_TO_JSON: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().miscellaneous.for_loss


class ObservationSpaceSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    COMPROMISED_STATUS: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.compromised_status
    VULNERABILITIES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.vulnerabilities
    NODE_CONNECTIONS: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.node_connections
    AVERAGE_VULNERABILITY: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.average_vulnerability
    GRAPH_CONNECTIVITY: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.graph_connectivity
    ATTACKING_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.attacking_nodes
    ATTACKED_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.attacked_nodes
    SPECIAL_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.special_nodes
    RED_AGENT_SKILL: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().observation_space.red_agent_skill


class GameRulesSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    GRACE_PERIOD_LENGTH: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().game_rules.grace_period_length
    MAX_STEPS: Final[YawningTitanQuery] = YawningTitanQuery().game_rules.max_steps
    BLUE_LOSS_CONDITION: Final[BlueLossConditionSchema] = BlueLossConditionSchema
    NETWORK_COMPATIBILITY: Final[
        NetworkCompatibilitySchema
    ] = NetworkCompatibilitySchema


class BlueSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    ACTION_SET: Final[BlueActionSetSchema] = BlueActionSetSchema
    INTRUSION_DISCOVERY_CHANCE: Final[
        BlueIntrusionDiscoverySchema
    ] = BlueIntrusionDiscoverySchema
    ATTACK_DISCOVERY: Final[BlueAttackDiscoverySchema] = BlueAttackDiscoverySchema


class RedSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    AGENT_ATTACK: Final[RedAgentAttackSchema] = RedAgentAttackSchema
    ACTION_SET: Final[RedActionSetSchema] = RedActionSetSchema
    NATURAL_SPREADING: Final[RedNaturalSpreadingSchema] = RedNaturalSpreadingSchema
    TARGET_MECHANISM: Final[RedTargetMechanismSchema] = RedTargetMechanismSchema


class GameModeConfigurationSchema:
    """Schema to describe a `~yawning_titan.config.core.ConfigGroup` object."""

    RED: RedSchema = RedSchema
    BLUE: BlueSchema = BlueSchema
    GAME_RULES: GameRulesSchema = GameRulesSchema
    BLUE_CAN_OBSERVE: ObservationSpaceSchema = ObservationSpaceSchema
    ON_RESET: ResetSchema = ResetSchema
    REWARD: RewardsSchema = RewardsSchema
    MISCELLANEOUS: MiscellaneousSchema = MiscellaneousSchema
