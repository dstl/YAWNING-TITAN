from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.helpers.environment_input_validation import (
    check_type,
    check_within_range,
)


@dataclass()
class GameRulesConfig(ConfigABC):
    """Class that validates and stores Game Rules Configuration."""

    _min_number_of_network_nodes: int
    _node_vulnerability_lower_bound: float
    _node_vulnerability_upper_bound: float
    _max_steps: int
    _lose_when_all_nodes_lost: bool
    _lose_when_n_percent_of_nodes_lost: bool
    _percentage_of_nodes_compromised_equals_loss: float
    _lose_when_high_value_node_lost: bool
    _lose_when_target_node_lost: bool
    _number_of_high_value_nodes: int
    _choose_high_value_nodes_placement_at_random: bool
    _choose_high_value_nodes_furthest_away_from_entry: bool
    _choose_entry_nodes_randomly: bool
    _number_of_entry_nodes: int
    _prefer_central_nodes_for_entry_nodes: bool
    _prefer_edge_nodes_for_entry_nodes: bool
    _grace_period_length: int

    # region Getters
    @property
    def min_number_of_network_nodes(self) -> int:
        """Minimum number of nodes the network this game mode is allowed to run on."""
        return self._min_number_of_network_nodes

    @property
    def node_vulnerability_lower_bound(self) -> float:
        """A lower vulnerability means that a node is less likely to be compromised."""
        return self._node_vulnerability_lower_bound

    @property
    def node_vulnerability_upper_bound(self) -> float:
        """A higher vulnerability means that a node is more vulnerable."""
        return self._node_vulnerability_upper_bound

    @property
    def max_steps(self) -> int:
        """The max steps that a game can go on for. If the blue agent reaches this they win."""
        return self._max_steps

    @property
    def lose_when_all_nodes_lost(self) -> bool:
        """The blue agent loses if all the nodes become compromised."""
        return self._lose_when_all_nodes_lost

    @property
    def lose_when_n_percent_of_nodes_lost(self) -> bool:
        """The blue agent loses if n% of the nodes become compromised."""
        return self._lose_when_n_percent_of_nodes_lost

    @property
    def percentage_of_nodes_compromised_equals_loss(self) -> float:
        """The percentage of nodes that need to be lost for blue to lose."""
        return self._percentage_of_nodes_compromised_equals_loss

    @property
    def lose_when_high_value_node_lost(self) -> bool:
        """Blue loses if a special 'high value' target is lost (a node picked in the environment)."""
        return self._lose_when_high_value_node_lost

    @property
    def lose_when_target_node_lost(self) -> bool:
        """Blue loses if the target node is lost (a node picked in the environment)."""
        return self._lose_when_target_node_lost

    @property
    def number_of_high_value_nodes(self) -> int:
        """If no high value nodes are supplied, how many should be chosen."""
        return self._number_of_high_value_nodes

    @property
    def choose_high_value_nodes_placement_at_random(self) -> bool:
        """The high value node is picked at random."""
        return self._choose_high_value_nodes_placement_at_random

    @property
    def choose_high_value_nodes_furthest_away_from_entry(self) -> bool:
        """The node the furthest away from the entry points to the network is picked as the target."""
        return self._choose_high_value_nodes_furthest_away_from_entry

    @property
    def choose_entry_nodes_randomly(self) -> bool:
        """If no entry nodes are supplied choose some at random."""
        return self._choose_entry_nodes_randomly

    @property
    def number_of_entry_nodes(self) -> int:
        """If no entry nodes are supplied then how many should be chosen."""
        return self._number_of_entry_nodes

    @property
    def prefer_central_nodes_for_entry_nodes(self) -> bool:
        """If no entry nodes are supplied then what bias is applied to the  nodes when choosing random entry nodes."""
        return self._prefer_central_nodes_for_entry_nodes

    @property
    def prefer_edge_nodes_for_entry_nodes(self) -> bool:
        """If no entry nodes are supplied then what bias is applied to the nodes when choosing random entry nodes."""
        return self._prefer_edge_nodes_for_entry_nodes

    @property
    def grace_period_length(self) -> int:
        """
        The length of a grace period at the start of the game.

        During this time the red agent cannot act. This gives the blue agent a chance to "prepare" (A length of 0
        means that there is no grace period).
        """
        return self._grace_period_length

    # endregion

    # region Setters
    @min_number_of_network_nodes.setter
    def min_number_of_network_nodes(self, value):
        self._min_number_of_network_nodes = value

    @node_vulnerability_lower_bound.setter
    def node_vulnerability_lower_bound(self, value):
        self._node_vulnerability_lower_bound = value

    @node_vulnerability_upper_bound.setter
    def node_vulnerability_upper_bound(self, value):
        self._node_vulnerability_upper_bound = value

    @max_steps.setter
    def max_steps(self, value):
        self._max_steps = value

    @lose_when_all_nodes_lost.setter
    def lose_when_all_nodes_lost(self, value):
        self._lose_when_all_nodes_lost = value

    @lose_when_n_percent_of_nodes_lost.setter
    def lose_when_n_percent_of_nodes_lost(self, value):
        self._lose_when_n_percent_of_nodes_lost = value

    @percentage_of_nodes_compromised_equals_loss.setter
    def percentage_of_nodes_compromised_equals_loss(self, value):
        self._percentage_of_nodes_compromised_equals_loss = value

    @lose_when_high_value_node_lost.setter
    def lose_when_high_value_node_lost(self, value):
        self._lose_when_high_value_node_lost = value

    @lose_when_target_node_lost.setter
    def lose_when_target_node_lost(self, value):
        self._lose_when_target_node_lost = value

    @number_of_high_value_nodes.setter
    def number_of_high_value_nodes(self, value):
        self._number_of_high_value_nodes = value

    @choose_high_value_nodes_placement_at_random.setter
    def choose_high_value_nodes_placement_at_random(self, value):
        self._choose_high_value_nodes_placement_at_random = value

    @choose_high_value_nodes_furthest_away_from_entry.setter
    def choose_high_value_nodes_furthest_away_from_entry(self, value):
        self._choose_high_value_nodes_furthest_away_from_entry = value

    @choose_entry_nodes_randomly.setter
    def choose_entry_nodes_randomly(self, value):
        self._choose_entry_nodes_randomly = value

    @number_of_entry_nodes.setter
    def number_of_entry_nodes(self, value):
        self._number_of_entry_nodes = value

    @prefer_central_nodes_for_entry_nodes.setter
    def prefer_central_nodes_for_entry_nodes(self, value):
        self._prefer_central_nodes_for_entry_nodes = value

    @prefer_edge_nodes_for_entry_nodes.setter
    def prefer_edge_nodes_for_entry_nodes(self, value):
        self._prefer_edge_nodes_for_entry_nodes = value

    @grace_period_length.setter
    def grace_period_length(self, value):
        self._grace_period_length = value

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> GameRulesConfig:
        """
        Creates an instance of `GameRulesConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        cls.validate(config_dict)

        game_rule_config = GameRulesConfig(
            _min_number_of_network_nodes=config_dict["min_number_of_network_nodes"],
            _node_vulnerability_lower_bound=config_dict[
                "node_vulnerability_lower_bound"
            ],
            _node_vulnerability_upper_bound=config_dict[
                "node_vulnerability_upper_bound"
            ],
            _max_steps=config_dict["max_steps"],
            _lose_when_all_nodes_lost=config_dict["lose_when_all_nodes_lost"],
            _lose_when_n_percent_of_nodes_lost=config_dict[
                "lose_when_n_percent_of_nodes_lost"
            ],
            _percentage_of_nodes_compromised_equals_loss=config_dict[
                "percentage_of_nodes_compromised_equals_loss"
            ],
            _lose_when_high_value_node_lost=config_dict[
                "lose_when_high_value_node_lost"
            ],
            _lose_when_target_node_lost=config_dict["lose_when_target_node_lost"],
            _number_of_high_value_nodes=config_dict["number_of_high_value_nodes"],
            _choose_high_value_nodes_placement_at_random=config_dict[
                "choose_high_value_nodes_placement_at_random"
            ],
            _choose_high_value_nodes_furthest_away_from_entry=config_dict[
                "choose_high_value_nodes_furthest_away_from_entry"
            ],
            _choose_entry_nodes_randomly=config_dict["choose_entry_nodes_randomly"],
            _number_of_entry_nodes=config_dict["number_of_entry_nodes"],
            _prefer_central_nodes_for_entry_nodes=config_dict[
                "prefer_central_nodes_for_entry_nodes"
            ],
            _prefer_edge_nodes_for_entry_nodes=config_dict[
                "prefer_edge_nodes_for_entry_nodes"
            ],
            _grace_period_length=config_dict["grace_period_length"],
        )

        return game_rule_config

    @classmethod
    def validate(cls, config_dict: dict):
        """
        Validates the game rules config dict.

        :param: config_dict: A config dict with the required key/values pairs.
        """
        # data is int or float
        for name in [
            "node_vulnerability_lower_bound",
            "node_vulnerability_upper_bound",
            "percentage_of_nodes_compromised_equals_loss",
        ]:
            check_type(config_dict, name, [float, int])
        # data s between 0 and 1 inclusive
        for name in [
            "node_vulnerability_lower_bound",
            "node_vulnerability_upper_bound",
        ]:
            check_within_range(config_dict, name, 0, 1, True, True)

        if (
            config_dict["node_vulnerability_lower_bound"]
            > config_dict["node_vulnerability_upper_bound"]
        ):
            raise ValueError(
                "'node_vulnerability_lower_bound', 'node_vulnerability_upper_bound' -> The lower bound for the node "
                "vulnerabilities should be less than the upper bound "
            )
        check_type(config_dict, "max_steps", [int])
        check_type(config_dict, "number_of_entry_nodes", [int])
        check_type(config_dict, "grace_period_length", [int])
        check_type(config_dict, "min_number_of_network_nodes", [int])
        check_type(config_dict, "number_of_high_value_nodes", [int])
        # make sure high value nodes is not more than the number of minimum number of nodes in network
        check_within_range(
            config_dict,
            "number_of_high_value_nodes",
            0,
            config_dict["min_number_of_network_nodes"],
            True,
            True,
        )

        check_within_range(config_dict, "grace_period_length", 0, 100, True, True)
        check_within_range(config_dict, "max_steps", 0, 10000000, False, True)
        # make sure entry nodes is not more than the number of minimum number of nodes in network
        check_within_range(
            config_dict,
            "number_of_entry_nodes",
            0,
            config_dict["min_number_of_network_nodes"],
            False,
            True,
        )

        # data is boolean
        for name in [
            "lose_when_all_nodes_lost",
            "lose_when_n_percent_of_nodes_lost",
            "lose_when_high_value_node_lost",
            "lose_when_target_node_lost",
            "choose_high_value_nodes_placement_at_random",
            "choose_high_value_nodes_furthest_away_from_entry",
            "choose_entry_nodes_randomly",
            "prefer_central_nodes_for_entry_nodes",
            "prefer_edge_nodes_for_entry_nodes",
        ]:
            check_type(config_dict, name, [bool])

        check_within_range(
            config_dict,
            "percentage_of_nodes_compromised_equals_loss",
            0,
            1,
            False,
            False,
        )
        if (
            config_dict["prefer_central_nodes_for_entry_nodes"]
            and config_dict["prefer_edge_nodes_for_entry_nodes"]
        ):
            raise ValueError(
                "'prefer_central_nodes_for_entry_nodes', 'prefer_edge_nodes_for_entry_nodes' -> cannot prefer both "
                "central and edge nodes "
                # noqa
            )

        if (
            (not config_dict["lose_when_all_nodes_lost"])
            and (not config_dict["lose_when_n_percent_of_nodes_lost"])
            and (not config_dict["lose_when_high_value_node_lost"])
            and (not config_dict["lose_when_target_node_lost"])
        ):
            raise ValueError(
                "'lose_when_target_node_lost', 'lose_when_all_nodes_lost', 'lose_when_n_percent_of_nodes_lost', "
                "'lose_when_high_value_node_lost' -> At least one loose condition must be turned on "
                # noqa
            )

        if config_dict["lose_when_high_value_node_lost"]:
            # if there is no way to set high value nodes
            if (
                not config_dict["choose_high_value_nodes_placement_at_random"]
                and not config_dict["choose_high_value_nodes_furthest_away_from_entry"]
            ):
                raise ValueError(
                    "'choose_high_value_nodes_placement_at_random', "
                    "'choose_high_value_nodes_furthest_away_from_entry' -> A method of selecting a high value node "
                    "must be chosen "
                    # noqa
                )
            # if there are conflicting configurations
            if (
                config_dict["choose_high_value_nodes_placement_at_random"]
                and config_dict["choose_high_value_nodes_furthest_away_from_entry"]
            ):
                raise ValueError(
                    "'choose_high_value_nodes_placement_at_random', "
                    "'choose_high_value_nodes_furthest_away_from_entry' -> Only one method of selecting a high value "
                    "node should be selected "
                    # noqa
                )

        if config_dict["grace_period_length"] > config_dict["max_steps"]:
            raise ValueError(
                "'grace_period_length', 'max_steps' -> The grace period cannot be the entire length of the game"
            )
