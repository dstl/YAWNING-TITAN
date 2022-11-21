from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC, ConfigItem
from yawning_titan.envs.generic.helpers.environment_input_validation import (
    check_type,
    check_within_range,
)


@dataclass()
class RedAgentConfig(ConfigABC):
    """Class that validates and stores the Red Agent Configuration."""

    _red_skill: int
    _red_uses_skill: bool
    _red_ignores_defences: bool
    _red_always_succeeds: bool
    _red_can_only_attack_from_red_agent_node: bool
    _red_can_attack_from_any_red_node: bool
    _red_can_naturally_spread: bool
    _chance_to_spread_to_connected_node: int
    _chance_to_spread_to_unconnected_node: int
    _red_uses_spread_action: bool
    _spread_action_likelihood: int
    _chance_for_red_to_spread: int
    _red_uses_random_infect_action: bool
    _random_infect_action_likelihood: int
    _chance_for_red_to_random_compromise: int
    _red_uses_basic_attack_action: bool
    _basic_attack_action_likelihood: int
    _red_uses_do_nothing_action: bool
    _do_nothing_action_likelihood: int
    _red_uses_move_action: bool
    _move_action_likelihood: int
    _red_uses_zero_day_action: bool
    _zero_day_start_amount: int
    _days_required_for_zero_day: int
    _red_chooses_target_at_random: bool
    _red_target_node: str
    _red_prioritises_connected_nodes: bool
    _red_prioritises_un_connected_nodes: bool
    _red_prioritises_vulnerable_nodes: bool
    _red_prioritises_resilient_nodes: bool
    _red_always_chooses_shortest_distance_to_target: bool

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> RedAgentConfig:
        """
        Creates an instance of `RedAgentConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        # validate red agent config values
        cls._validate(config_dict)

        red_agent_config = RedAgentConfig(
            _red_skill=ConfigItem(
                config_dict["red_skill"],
                float,
                "The red agents skill level. Higher means that red is more likely to succeed in attacks"
            ),
            _red_uses_skill=ConfigItem(
                config_dict["red_uses_skill"],
                bool,
                "Red uses its skill modifier when attacking nodes"
            ),
            _red_ignores_defences=ConfigItem(
                config_dict["red_ignores_defences"],
                bool,
                "The red agent ignores the defences of nodes"
            ),
            _red_always_succeeds=ConfigItem(
                config_dict["red_always_succeeds"],
                bool,
                "Reds attacks always succeed"
            ),
            _red_can_only_attack_from_red_agent_node=ConfigItem(
                config_dict["red_can_only_attack_from_red_agent_node"],
                bool,
                group="red_attack_source",
            ),
            _red_can_attack_from_any_red_node=ConfigItem(
                config_dict["red_can_attack_from_any_red_node"],
                bool,
                group="red_attack_source"
            ),
            _red_can_naturally_spread=ConfigItem(
                config_dict["red_can_naturally_spread"],
                bool,
                "The red agent naturally spreads its influence every time-step"
            ),
            _chance_to_spread_to_connected_node=ConfigItem(
                config_dict["chance_to_spread_to_connected_node"],
                float,
                "If a node is connected to a compromised node what chance does it have to become compromised every turn through natural spreading",
                depends_on=['red_can_naturally_spread']
            ),
            _chance_to_spread_to_unconnected_node=ConfigItem(
                config_dict["chance_to_spread_to_unconnected_node"],
                float,
                "If a node is not connected to a compromised node what chance does it have to become randomly infected through natural spreading",
                depends_on=['red_can_naturally_spread']
            ),
            _red_uses_spread_action=ConfigItem(
                config_dict["red_uses_spread_action"],
                bool,
                "Tries to spread to every node connected to an infected node"
            ),
            _spread_action_likelihood=ConfigItem(
                config_dict["spread_action_likelihood"],
                float,
                "Weighting for spread action",
                depends_on=['red_uses_spread_action']
            ),
            _chance_for_red_to_spread=ConfigItem(
                config_dict["chance_for_red_to_spread"],
                float,
                "Chance for each 'spread' to succeed",
                depends_on=['red_uses_spread_action']
            ),
            _red_uses_random_infect_action=ConfigItem(
                config_dict["red_uses_random_infect_action"],
                bool,
                "Red tries to infect every safe node in the environment"
            ),
            _random_infect_action_likelihood=ConfigItem(
                config_dict["random_infect_action_likelihood"],
                float,
                "Weighting for random infection action",
                depends_on=['red_uses_random_infect_action']
            ),
            _chance_for_red_to_random_compromise=ConfigItem(
                config_dict["chance_for_red_to_random_compromise"],
                float,
                "Chance for each 'infect' to succeed",
                depends_on=['red_uses_random_infect_action']
            ),
            _red_uses_basic_attack_action=ConfigItem(
                config_dict["red_uses_basic_attack_action"],
                bool,
                "The red agent picks a single node connected to an infected node and tries to attack and take over that node"
            ),
            _basic_attack_action_likelihood=ConfigItem(
                config_dict["basic_attack_action_likelihood"],
                float,
                "Weighting for basic attack action",
                depends_on=['red_uses_basic_attack_action']
            ),
            _red_uses_do_nothing_action=ConfigItem(
                config_dict["red_uses_do_nothing_action"],
                bool,
                "The red agent does nothing"
            ),
            _do_nothing_action_likelihood=ConfigItem(
                config_dict["do_nothing_action_likelihood"],
                float,
                "Weighting for do nothing action",
                depends_on=['red_uses_do_nothing_action']
            ),
            _red_uses_move_action=ConfigItem(
                config_dict["red_uses_move_action"],
                bool,
                "The red agent moves to a different node"
            ),
            _move_action_likelihood=ConfigItem(
                config_dict["move_action_likelihood"],
                float,
                "Weighting for move action",
                depends_on=['move_action_likelihood']
            ),
            _red_uses_zero_day_action=ConfigItem(
                config_dict["red_uses_zero_day_action"],
                bool,
                "The red agent will pick a safe node connected to an infect node and take it over with a 100% chance to succeed (can only happen every n timesteps)"
            ),
            _zero_day_start_amount=ConfigItem(
                config_dict["zero_day_start_amount"],
                int,
                "The number of zero day attacks that the red agent starts with",
                depends_on=['red_uses_zero_day_action']
            ),
            _days_required_for_zero_day=ConfigItem(
                config_dict["days_required_for_zero_day"],
                int,
                "The amount of 'progress' that need to have passed before the red agent gains a zero day attack",
                depends_on=['red_uses_zero_day_action']
            ),
            _red_chooses_target_at_random=ConfigItem(
                config_dict["red_chooses_target_at_random"],
                bool,
                "Red picks nodes to attack at random",
                group='red_target_mechanism'
            ),
            _red_target_node=ConfigItem(
                config_dict["red_target_node"],
                str,
                "Red targets a specific node",
                group='red_target_mechanism'
            ),
            _red_prioritises_connected_nodes=ConfigItem(
                config_dict["red_prioritises_connected_nodes"],
                bool,
                "ed sorts the nodes it can attack and chooses the one that has the most connections",
                group='red_target_mechanism'
            ),
            _red_prioritises_un_connected_nodes=ConfigItem(
                config_dict["red_prioritises_un_connected_nodes"],
                bool,
                "Red sorts the nodes it can attack and chooses the one that has the least connections",
                group='red_target_mechanism'
            ),
            _red_prioritises_vulnerable_nodes=ConfigItem(
                config_dict["red_prioritises_vulnerable_nodes"],
                bool,
                "Red sorts the nodes is can attack and chooses the one that is the most vulnerable",
                group='red_target_mechanism'
            ),
            _red_prioritises_resilient_nodes=ConfigItem(
                config_dict["red_prioritises_resilient_nodes"],
                bool,
                "Red sorts the nodes is can attack and chooses the one that is the least vulnerable",
                group='red_target_mechanism'
            ),
            _red_always_chooses_shortest_distance_to_target=ConfigItem(
                config_dict["red_always_chooses_shortest_distance_to_target"],
                bool,
                "Whether red will always pick the shortest path to target",
                depends_on=['red_target_node']
            )
        )
        return red_agent_config

    @classmethod
    def _validate(cls, config_dict: dict):
        for name in [
            "chance_for_red_to_spread",
            "chance_for_red_to_random_compromise",
            "red_skill",
            "spread_action_likelihood",
            "random_infect_action_likelihood",
            "basic_attack_action_likelihood",
            "do_nothing_action_likelihood",
            "move_action_likelihood",
            "chance_to_spread_to_connected_node",
            "chance_to_spread_to_unconnected_node",
        ]:
            check_type(config_dict, name, [int, float])

        # int
        for name in ["zero_day_start_amount", "days_required_for_zero_day"]:
            check_type(config_dict, name, [int])

        if config_dict["red_target_node"] is not None:
            check_type(config_dict, "red_target_node", [str])

        # type of data is bool
        for name in [
            "red_uses_skill",
            "red_ignores_defences",
            "red_always_succeeds",
            "red_can_only_attack_from_red_agent_node",
            "red_can_attack_from_any_red_node",
            "red_uses_spread_action",
            "red_uses_random_infect_action",
            "red_uses_zero_day_action",
            "red_uses_basic_attack_action",
            "red_uses_do_nothing_action",
            "red_uses_move_action",
            "red_chooses_target_at_random",
            "red_prioritises_connected_nodes",
            "red_prioritises_un_connected_nodes",
            "red_prioritises_vulnerable_nodes",
            "red_prioritises_resilient_nodes",
            "red_can_naturally_spread",
            "red_always_chooses_shortest_distance_to_target",
        ]:
            check_type(config_dict, name, [bool])

        # data satisfies 0 <= data <= 1
        for name in [
            "red_skill",
            "chance_for_red_to_spread",
            "chance_for_red_to_random_compromise",
            "chance_to_spread_to_connected_node",
            "chance_to_spread_to_unconnected_node",
        ]:
            check_within_range(config_dict, name, 0, 1, True, True)

        # data satisfies 0 < data
        for name in [
            "spread_action_likelihood",
            "random_infect_action_likelihood",
            "basic_attack_action_likelihood",
            "do_nothing_action_likelihood",
            "move_action_likelihood",
        ]:
            check_within_range(config_dict, name, 0, None, False, True)

        # data satisfies 0 <= data
        for name in ["zero_day_start_amount", "days_required_for_zero_day"]:
            check_within_range(config_dict, name, 0, None, True, True)

        # misc
        if (
            (not config_dict["red_uses_skill"])
            and (not config_dict["red_always_succeeds"])
            and config_dict["red_ignores_defences"]
        ):
            raise ValueError(
                "'red_uses_skill', 'red_always_succeeds', 'red_ignores_defences' -> Red must either use skill, always succeed or not ignore the defences of the nodes"
                # noqa
            )
        if (
            (not config_dict["red_uses_spread_action"])
            and (not config_dict["red_uses_random_infect_action"])
            and (not config_dict["red_uses_zero_day_action"])
            and (not config_dict["red_uses_basic_attack_action"])
            and (not config_dict["red_uses_do_nothing_action"])
        ):
            raise ValueError(
                "'red_uses_*****' -> Red must have at least one action activated"
            )
        if (
            (not config_dict["red_chooses_target_at_random"])
            and (config_dict["red_target_node"] is None)
            and (not config_dict["red_prioritises_connected_nodes"])
            and (not config_dict["red_prioritises_un_connected_nodes"])
            and (not config_dict["red_prioritises_vulnerable_nodes"])
            and (not config_dict["red_prioritises_resilient_nodes"])
        ):
            raise ValueError(
                "'red_target_node', 'red_prioritises_****' -> Red must choose its target in some way. If you are unsure select 'red_chooses_target_at_random'"
                # noqa
            )
        if (not config_dict["red_can_only_attack_from_red_agent_node"]) and (
            not config_dict["red_can_attack_from_any_red_node"]
        ):
            raise ValueError(
                "'red_can_only_attack_from_red_agent_node', 'red_can_attack_from_any_red_node' -> The red agent must be able to attack either from every red node or just the red central node"
                # noqa
            )
        if (
            config_dict["red_prioritises_vulnerable_nodes"]
            or config_dict["red_prioritises_resilient_nodes"]
        ):
            if config_dict["red_ignores_defences"]:
                raise ValueError(
                    "'red_ignores_defences', 'red_prioritises_vulnerable_nodes', 'red_prioritises_resilient_nodes' -> "
                    "It makes no sense for red to prioritise nodes based on a stat that is ignored (vulnerability) "
                    # noqa
                )
        # spread both 0 but spreading on?
        if config_dict["red_can_naturally_spread"]:
            if (
                config_dict["chance_to_spread_to_connected_node"] == 0
                and config_dict["chance_to_spread_to_unconnected_node"] == 0
            ):
                raise ValueError(
                    "'red_can_naturally_spread', 'chance_to_spread_to_connected_node', "
                    "'chance_to_spread_to_unconnected_node' -> If red can naturally spread however the probabilities "
                    "for both types of spreading are 0 "
                    # noqa
                )
