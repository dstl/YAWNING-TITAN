from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any

from yawning_titan.config.environment.network_config import NetworkConfig
from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type, check_within_range


@dataclass()
class GameRulesConfig(ConfigGroupABC):
    """
    Class that validates and stores Game Rules Configuration
    """

    gr_min_number_of_network_nodes: int = field(metadata="The minimum number of nodes the game mode will be allowed to run on")
    """The minimum number of nodes the game mode will be allowed to run on"""

    gr_node_vuln_lower: float = field(metadata="Lower bound of the node vulnerability")
    """Lower bound of the node vulnerability"""

    gr_node_vuln_upper: float = field(metadata="Upper bound of the node vulnerability")
    """Upper bound of the node vulnerability"""

    gr_max_steps: int = field(metadata="Timesteps the game will go on for")
    """Timesteps the game will go on for"""

    gr_loss_total_compromise: bool = field(metadata="Is true if the game ends when all nodes are lost")
    """Is true if the game ends when all nodes are lost"""

    gr_loss_pc_nodes_compromised: bool = field(metadata="Is true if the game ends when a percentage of nodes is compromised")
    """Is true if the game ends when a percentage of nodes is compromised"""

    gr_loss_pc_node_compromised_pc: float = field(metadata="Percentage of the nodes becoming infected for the game to be considered lost by the blue agent")
    """Percentage of the nodes becoming infected for the game to be considered lost by the blue agent"""

    gr_number_of_high_value_targets: int = field(metadata="Number of nodes to be marked as high value in network")
    """Number of nodes to be marked as high value in network"""

    gr_loss_hvt: bool = field(metadata="Is true if the game ends if the high value node is lost")
    """Is true if the game ends if the high value node is lost"""

    gr_loss_hvt_random_placement: bool = field(metadata="Is true if the high value nodes are set randomly across the network")
    """Is true if the high value nodes are set randomly across the network"""

    gr_loss_hvt_furthest_away: bool = field(metadata="Is true if the high value nodes are set furthest away from the entry nodes")
    """Is true if the high value nodes are set furthest away from the entry nodes"""

    gr_random_entry_nodes: bool = field(metadata="Is true if the entry nodes will be placed randomly across the network")
    """Is true if the entry nodes will be placed randomly across the network"""

    gr_num_entry_nodes: int = field(metadata="Number of nodes to be marked as entry nodes in network")
    """Number of nodes to be marked as entry nodes in network"""

    gr_prefer_central_entry: bool = field(metadata="Is true if the entry nodes will be placed centrally in the network")
    """Is true if the entry nodes will be placed centrally in the network"""

    gr_prefer_edge_nodes: bool = field(metadata="Is true if the entry nodes will be placed on the edges of the network")
    """Is true if the entry nodes will be placed on the edges of the network"""

    gr_grace_period: int = field(metadata="Number of timesteps the blue agent has to prepare")
    """Number of timesteps the blue agent has to prepare"""

    @classmethod
    def create(
            cls,
            settings: Dict[str, Any]
    ) -> GameRulesConfig:
        cls._validate(settings)

        game_rule_config = GameRulesConfig(
            gr_min_number_of_network_nodes=settings["min_number_of_network_nodes"],
            gr_node_vuln_lower=settings[
                "node_vulnerability_lower_bound"
            ],
            gr_node_vuln_upper=settings[
                "node_vulnerability_upper_bound"
            ],
            gr_max_steps=settings["max_steps"],
            gr_loss_total_compromise=settings[
                "lose_when_all_nodes_lost"
            ],
            gr_loss_pc_nodes_compromised=settings[
                "lose_when_n_percent_of_nodes_lost"
            ],
            gr_loss_pc_node_compromised_pc=settings[
                "percentage_of_nodes_compromised_equals_loss"
            ],
            gr_number_of_high_value_targets=settings["number_of_high_value_targets"],
            gr_loss_hvt=settings["lose_when_high_value_target_lost"],
            gr_loss_hvt_random_placement=settings[
                "choose_high_value_targets_placement_at_random"
            ],
            gr_loss_hvt_furthest_away=settings[
                "choose_high_value_targets_furthest_away_from_entry"
            ],
            gr_random_entry_nodes=settings[
                "choose_entry_nodes_randomly"
            ],
            gr_num_entry_nodes=
            settings["number_of_entry_nodes"],
            gr_prefer_central_entry=settings[
                "prefer_central_nodes_for_entry_nodes"
            ],
            gr_prefer_edge_nodes=settings[
                "prefer_edge_nodes_for_entry_nodes"
            ],
            gr_grace_period=settings["grace_period_length"]
        )

        return game_rule_config

    @classmethod
    def _validate(
            cls,
            data: dict
    ):
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
            )
        check_type(data, "max_steps", [int])
        check_type(data, "number_of_entry_nodes", [int])
        check_type(data, "grace_period_length", [int])
        check_type(data, "min_number_of_network_nodes", [int])
        check_type(data, "number_of_high_value_targets", [int])
        # make sure high value targets is not more than the number of minimum number of nodes in network
        check_within_range(data, "number_of_high_value_targets", 0, data["min_number_of_network_nodes"], True, True)

        check_within_range(data, "grace_period_length", 0, 100, True, True)
        check_within_range(data, "max_steps", 0, 10000000, False, True)
        # make sure entry nodes is not more than the number of minimum number of nodes in network
        check_within_range(data, "number_of_entry_nodes", 0, data["min_number_of_network_nodes"], False, True)

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

        if data["grace_period_length"] > data["max_steps"]:
            raise ValueError(
                "'grace_period_length', 'max_steps' -> The grace period cannot be the entire length of the game"
            )
