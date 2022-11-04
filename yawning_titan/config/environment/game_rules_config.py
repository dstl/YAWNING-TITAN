from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List

from yawning_titan.config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type,check_within_range


@dataclass
class GameRulesConfig(ConfigGroupABC):
    """
    Class that validates and stores Game Rules Configuration
    """

    gr_node_vuln_lower: float
    """A lower vulnerability means that a node is less likely to be compromised"""
    
    gr_node_vuln_upper: float
    """A higher vulnerability means that a node is more vulnerable"""

    gr_max_steps: int
    """The max steps that a game can go on for. If the blue agent reaches this they win"""

    gr_loss_total_compromise: bool
    """The blue agent loses if all the nodes become compromised"""

    gr_loss_pc_nodes_compromised: float
    """The percentage of nodes that need to be lost for blue to lose"""

    gr_loss_pc_node_compromised_pc: bool
    """The blue agent loses if n% of the nodes become compromised"""

    gr_number_of_high_value_targets: int
    """If no high value targets are supplied, how many should be chosen"""

    gr_loss_hvt: bool
    """Blue loses if a special 'high value' target it lost (a node picked in the environment)"""

    gr_loss_hvt_random_placement: bool
    """The high value target is picked at random"""

    gr_loss_hvt_furthest_away: bool
    """The node furthest away from the entry points to the network is picked as the target"""
    
    gr_random_entry_nodes: bool
    """If no entry nodes are supplied choose some at random"""

    gr_num_entry_nodes: int
    """If no entry nodes are supplied then how many should be chosen"""

    gr_prefer_central_entry: bool
    """If no entry nodes are supplied then what bias is applied to centrally placed nodes when choosing random entry nodes"""

    gr_prefer_edge_nodes: bool
    """If no entry nodes are supplied then what bias is applied to nodes closer to the edge when choosing random entry nodes"""

    gr_grace_period: int
    """The length of a grace period at the start of the game. During this time the red agent cannot act. This gives the blue agent a chance to "prepare" (A length of 0 means that there is no grace period)"""

    @classmethod
    def create(cls, settings: Dict[str, Any], high_value_targets :List[str], number_of_nodes:int):
        cls._validate(settings,high_value_targets,number_of_nodes)
        game_rules = GameRulesConfig(
            gr_node_vuln_lower = settings[
                "node_vulnerability_lower_bound"
            ],
            gr_node_vuln_upper = settings[
                "node_vulnerability_upper_bound"
            ],
            gr_max_steps = settings["max_steps"],
            gr_loss_total_compromise = settings[
                "lose_when_all_nodes_lost"
            ],
            gr_loss_pc_nodes_compromised = settings[
                "lose_when_n_percent_of_nodes_lost"
            ],
            gr_loss_pc_node_compromised_pc = settings[
                "percentage_of_nodes_compromised_equals_loss"
            ],
            gr_number_of_high_value_targets = settings["number_of_high_value_targets"],
            gr_loss_hvt = settings["lose_when_high_value_target_lost"],
            gr_loss_hvt_random_placement = settings[
                "choose_high_value_targets_placement_at_random"
            ],
            gr_loss_hvt_furthest_away = settings[
                "choose_high_value_targets_furthest_away_from_entry"
            ],
            gr_random_entry_nodes = settings[
                "choose_entry_nodes_randomly"
            ],
            gr_num_entry_nodes = settings["number_of_entry_nodes"],
            gr_prefer_central_entry = settings[
                "prefer_central_nodes_for_entry_nodes"
            ],
            gr_prefer_edge_nodes = settings[
                "prefer_edge_nodes_for_entry_nodes"
            ],
            gr_grace_period = settings["grace_period_length"]
        )

        return game_rules

    @classmethod
    def _validate(cls, data: dict, high_value_targets:List[str], number_of_nodes:int):
        # data is int or float
        for name in [
            "node_vulnerability_lower_bound",
            "node_vulnerability_upper_bound",
            "percentage_of_nodes_compromised_equals_loss",
        ]:
            check_type(data, name, [float, int])
        # data s between 0 and 1 inclusive
        for name in ["node_vulnerability_lower_bound", "node_vulnerability_upper_bound"]:
            check_within_range(data, name, 0, 1, True, True)

        if data["node_vulnerability_lower_bound"] > data["node_vulnerability_upper_bound"]:
            raise ValueError(
                "'node_vulnerability_lower_bound', 'node_vulnerability_upper_bound' -> The lower bound for the node vulnerabilities should be less than the upper bound"
                # noqa
            )
        check_type(data, "max_steps", [int])
        check_type(data, "number_of_entry_nodes", [int])
        check_type(data, "grace_period_length", [int])

        check_within_range(data, "grace_period_length", 0, 100, True, True)
        check_within_range(data, "max_steps", 0, 10000000, False, True)
        check_within_range(data, "number_of_entry_nodes", 0, number_of_nodes, False, True)

        # data is boolean
        for name in [
            "lose_when_all_nodes_lost",
            "lose_when_n_percent_of_nodes_lost",
            "lose_when_high_value_target_lost",
            "choose_high_value_targets_placement_at_random",
            "choose_high_value_targets_furthest_away_from_entry",
            "choose_entry_nodes_randomly",
            "prefer_central_nodes_for_entry_nodes",
            "prefer_edge_nodes_for_entry_nodes",
        ]:
            check_type(data, name, [bool])

        check_within_range(
            data, "percentage_of_nodes_compromised_equals_loss", 0, 1, False, False
        )
        if (
            data["prefer_central_nodes_for_entry_nodes"]
            and data["prefer_edge_nodes_for_entry_nodes"]
        ):
            raise ValueError(
                "'prefer_central_nodes_for_entry_nodes', 'prefer_edge_nodes_for_entry_nodes' -> cannot prefer both central and edge nodes"
                # noqa
            )

        if (
            (not data["lose_when_all_nodes_lost"])
            and (not data["lose_when_n_percent_of_nodes_lost"])
            and (not data["lose_when_high_value_target_lost"])
        ):
            raise ValueError(
                "'lose_when_all_nodes_lost', 'lose_when_n_percent_of_nodes_lost', 'lose_when_high_value_target_lost' -> At least one loose condition must be turned on"
                # noqa
            )

        if data["lose_when_high_value_target_lost"]:
            # if there is no way to set high value targets
            if (
                not high_value_targets and
                not data["choose_high_value_targets_placement_at_random"] and
                not data["choose_high_value_targets_furthest_away_from_entry"]
            ):
                raise ValueError(
                    "'choose_high_value_targets_placement_at_random', 'choose_high_value_targets_furthest_away_from_entry' -> A method of selecting the high value target must be chosen"
                    # noqa
                )
            # if there are conflicting configurations
            if (
                    data["choose_high_value_targets_placement_at_random"]
                    and data["choose_high_value_targets_furthest_away_from_entry"]
            ):
                raise ValueError(
                    "'choose_high_value_targets_placement_at_random', 'choose_high_value_targets_furthest_away_from_entry' -> Only one method of selecting a high value target should be selected"
                    # noqa
                )
            # if high value targets are set and these configurations are also set
            if (
                    high_value_targets and
                    (data["choose_high_value_targets_placement_at_random"]
                    or data["choose_high_value_targets_furthest_away_from_entry"])
            ):
                raise ValueError(
                    "'high_value_targets_user_defined'choose_high_value_targets_placement_at_random', 'choose_high_value_targets_furthest_away_from_entry' -> Only one method of selecting a high value target should be selected"
                    # noqa
                )
            data["number_of_high_value_targets"] = data.get("number_of_high_value_targets",len(high_value_targets) if high_value_targets is not None else 0)
            check_type(data, "number_of_high_value_targets", [int])
            check_within_range(data, "number_of_high_value_targets", 1, number_of_nodes, True, True)

        if data["grace_period_length"] > data["max_steps"]:
            raise ValueError(
                "'grace_period_length', 'max_steps' -> The grace period cannot be the entire length of the game"
            )
