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

    _node_vulnerability_lower_bound: float
    _node_vulnerability_upper_bound: float
    _max_steps: int
    _lose_when_all_nodes_lost: bool
    _lose_when_n_percent_of_nodes_lost: bool
    _percentage_of_nodes_compromised_equals_loss: float
    _lose_when_high_value_node_lost: bool
    _lose_when_target_node_lost: bool
    _grace_period_length: int

    # region Getters

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
    def grace_period_length(self) -> int:
        """
        The length of a grace period at the start of the game.

        During this time the red agent cannot act. This gives the blue agent a chance to "prepare" (A length of 0
        means that there is no grace period).
        """
        return self._grace_period_length

    # endregion

    # region Setters
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
            _node_vulnerability_lower_bound=config_dict[
                "node_vulnerability_min"
            ],
            _node_vulnerability_upper_bound=config_dict[
                "node_vulnerability_max"
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
            "node_vulnerability_min",
            "node_vulnerability_max",
            "percentage_of_nodes_compromised_equals_loss",
        ]:
            check_type(config_dict, name, [float, int])
        # data s between 0 and 1 inclusive
        for name in [
            "node_vulnerability_min",
            "node_vulnerability_max",
        ]:
            check_within_range(config_dict, name, 0, 1, True, True)

        if (
            config_dict["node_vulnerability_min"]
            > config_dict["node_vulnerability_max"]
        ):
            raise ValueError(
                "'node_vulnerability_min', 'node_vulnerability_max' -> The lower bound for the node "
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

        # data is boolean
        for name in [
            "lose_when_all_nodes_lost",
            "lose_when_n_percent_of_nodes_lost",
            "lose_when_high_value_node_lost",
            "lose_when_target_node_lost",
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
            pass

        if config_dict["grace_period_length"] > config_dict["max_steps"]:
            raise ValueError(
                "'grace_period_length', 'max_steps' -> The grace period cannot be the entire length of the game"
            )
