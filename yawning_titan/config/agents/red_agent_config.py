from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.helpers.environment_input_validation import (
    check_type,
    check_within_range,
)


@dataclass()
class RedAgentConfig(ConfigABC):
    """Class that validates and stores the Red Agent Configuration."""

    _red_skill: float
    _red_uses_skill: bool
    _red_ignores_defences: bool
    _red_always_succeeds: bool
    _red_can_only_attack_from_red_agent_node: bool
    _red_can_attack_from_any_red_node: bool
    _red_can_naturally_spread: bool
    _chance_to_spread_to_connected_node: float
    _chance_to_spread_to_unconnected_node: float
    _red_uses_spread_action: bool
    _spread_action_likelihood: float
    _chance_for_red_to_spread: float
    _red_uses_random_infect_action: bool
    _random_infect_action_likelihood: float
    _chance_for_red_to_random_compromise: float
    _red_uses_basic_attack_action: bool
    _basic_attack_action_likelihood: float
    _red_uses_do_nothing_action: bool
    _do_nothing_action_likelihood: float
    _red_uses_move_action: bool
    _move_action_likelihood: float
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

    # region Getters
    @property
    def red_skill(self) -> float:
        """
        Red Skill.

        The red agents skill level. Higher means that red is more likely to
        succeed in attacks.
        """
        return self._red_skill

    @property
    def red_uses_skill(self) -> bool:
        """Red uses its skill modifier when attacking nodes."""
        return self._red_uses_skill

    @property
    def red_ignores_defences(self) -> bool:
        """The red agent ignores the defences of nodes."""
        return self._red_ignores_defences

    @property
    def red_always_succeeds(self) -> bool:
        """Reds attacks always succeed."""
        return self._red_always_succeeds

    @property
    def red_can_only_attack_from_red_agent_node(self) -> bool:
        """
        Red can only attack from red agent node.

        The red agent will only ever be in one node however it can control any
        amount of nodes. Can the red agent only attack from its one main
        node or can it attack from any node that it controls.
        """
        return self._red_can_only_attack_from_red_agent_node

    @property
    def red_can_attack_from_any_red_node(self) -> bool:
        """
        Red can attack from any node.

        The red agent will only ever be in one node however it can control any
        amount of nodes. Can the red agent only attack from its one main
        node or can it attack from any node that it controls.
        """
        return self._red_can_attack_from_any_red_node

    @property
    def red_can_naturally_spread(self) -> bool:
        """The red agent naturally spreads its influence every time-step."""
        return self._red_can_naturally_spread

    @property
    def chance_to_spread_to_connected_node(self) -> float:
        """
        Chance to spread to connected node.

        If a node is connected to a compromised node what chance does it have
        to become compromised every turn through natural spreading.
        """
        return self._chance_to_spread_to_connected_node

    @property
    def chance_to_spread_to_unconnected_node(self) -> float:
        """
        Chance to spread to unconnected node.

        If a node is not connected to a compromised node what chance does it
        have to become randomly infected through natural spreading.
        """
        return self._chance_to_spread_to_unconnected_node

    @property
    def red_uses_spread_action(self) -> bool:
        """Tries to spread to every node connected to an infected node."""
        return self._red_uses_spread_action

    @property
    def spread_action_likelihood(self) -> float:
        """Weighting for red_uses_spread_action."""
        return self._spread_action_likelihood

    @property
    def chance_for_red_to_spread(self) -> float:
        """Chance for each 'spread' to succeed."""
        return self._chance_for_red_to_spread

    @property
    def red_uses_random_infect_action(self) -> bool:
        """Tries to infect every safe node in the environment."""
        return self._red_uses_random_infect_action

    @property
    def random_infect_action_likelihood(self) -> float:
        """Weighting for red_uses_random_infect_action."""
        return self._random_infect_action_likelihood

    @property
    def chance_for_red_to_random_compromise(self) -> float:
        """Chance for each 'infect' to succeed."""
        return self._chance_for_red_to_random_compromise

    @property
    def red_uses_basic_attack_action(self) -> bool:
        """
        Red uses basic attack action.

        The red agent picks a single node connected to an infected node and
        tries to attack and take over that node.
        """
        return self._red_uses_basic_attack_action

    @property
    def basic_attack_action_likelihood(self) -> float:
        """Weighting for red_uses_basic_attack_action."""
        return self._basic_attack_action_likelihood

    @property
    def red_uses_do_nothing_action(self) -> bool:
        """The red agent does nothing."""
        return self._red_uses_do_nothing_action

    @property
    def do_nothing_action_likelihood(self) -> float:
        """Chance for red_uses_do_nothing_action."""
        return self._do_nothing_action_likelihood

    @property
    def red_uses_move_action(self) -> bool:
        """The red agent moves to a different node."""
        return self._red_uses_move_action

    @property
    def move_action_likelihood(self) -> float:
        """Chance of red_uses_move_action."""
        return self._move_action_likelihood

    @property
    def red_uses_zero_day_action(self) -> bool:
        """
        Red uses zero day action.

        The red agent will pick a safe node connected to an infected node and
        take it over with a 100% chance to succeed (can only happen every n
        timesteps).
        """
        return self._red_uses_zero_day_action

    @property
    def zero_day_start_amount(self) -> float:
        """The number of zero-day attacks that the red agent starts with."""
        return self._zero_day_start_amount

    @property
    def days_required_for_zero_day(self) -> int:
        """The amount of 'progress' that need to have passed before the red agent gains a zero day attack."""
        return self._days_required_for_zero_day

    @property
    def red_chooses_target_at_random(self) -> bool:
        """Red picks nodes to attack at random."""
        return self._red_chooses_target_at_random

    @property
    def red_target_node(self) -> str:
        """Red targets a specific node."""
        return self._red_target_node

    @property
    def red_prioritises_connected_nodes(self) -> bool:
        """Red sorts the nodes it can attack and chooses the one that has the most connections."""
        return self._red_prioritises_connected_nodes

    @property
    def red_prioritises_un_connected_nodes(self) -> bool:
        """Red sorts the nodes it can attack and chooses the one that has the least connections."""
        return self._red_prioritises_un_connected_nodes

    @property
    def red_prioritises_vulnerable_nodes(self) -> bool:
        """Red sorts the nodes is can attack and chooses the one that is the most vulnerable."""
        return self._red_prioritises_vulnerable_nodes

    @property
    def red_prioritises_resilient_nodes(self) -> bool:
        """Red sorts the nodes is can attack and chooses the one that is the least vulnerable."""
        return self._red_prioritises_resilient_nodes

    @property
    def red_always_chooses_shortest_distance_to_target(self) -> bool:
        """Red always chooses the absolute shortest distance to target with no randomisation."""
        return self._red_always_chooses_shortest_distance_to_target

    # endregion

    # region Setters
    @red_skill.setter
    def red_skill(self, value):
        self._red_skill = value

    @red_uses_skill.setter
    def red_uses_skill(self, value):
        self._red_uses_skill = value

    @red_ignores_defences.setter
    def red_ignores_defences(self, value):
        self._red_ignores_defences = value

    @red_always_succeeds.setter
    def red_always_succeeds(self, value):
        self._red_always_succeeds = value

    @red_can_only_attack_from_red_agent_node.setter
    def red_can_only_attack_from_red_agent_node(self, value):
        self._red_can_only_attack_from_red_agent_node = value

    @red_can_attack_from_any_red_node.setter
    def red_can_attack_from_any_red_node(self, value):
        self._red_can_attack_from_any_red_node = value

    @red_can_naturally_spread.setter
    def red_can_naturally_spread(self, value):
        self._red_can_naturally_spread = value

    @chance_to_spread_to_connected_node.setter
    def chance_to_spread_to_connected_node(self, value):
        self._chance_to_spread_to_connected_node = value

    @chance_to_spread_to_unconnected_node.setter
    def chance_to_spread_to_unconnected_node(self, value):
        self._chance_to_spread_to_unconnected_node = value

    @red_uses_spread_action.setter
    def red_uses_spread_action(self, value):
        self._red_uses_spread_action = value

    @spread_action_likelihood.setter
    def spread_action_likelihood(self, value):
        self._spread_action_likelihood = value

    @chance_for_red_to_spread.setter
    def chance_for_red_to_spread(self, value):
        self._chance_for_red_to_spread = value

    @red_uses_random_infect_action.setter
    def red_uses_random_infect_action(self, value):
        self._red_uses_random_infect_action = value

    @random_infect_action_likelihood.setter
    def random_infect_action_likelihood(self, value):
        self._random_infect_action_likelihood = value

    @chance_for_red_to_random_compromise.setter
    def chance_for_red_to_random_compromise(self, value):
        self._chance_for_red_to_random_compromise = value

    @red_uses_basic_attack_action.setter
    def red_uses_basic_attack_action(self, value):
        self._red_uses_basic_attack_action = value

    @basic_attack_action_likelihood.setter
    def basic_attack_action_likelihood(self, value):
        self._basic_attack_action_likelihood = value

    @red_uses_do_nothing_action.setter
    def red_uses_do_nothing_action(self, value):
        self._red_uses_do_nothing_action = value

    @do_nothing_action_likelihood.setter
    def do_nothing_action_likelihood(self, value):
        self._do_nothing_action_likelihood = value

    @red_uses_move_action.setter
    def red_uses_move_action(self, value):
        self._red_uses_move_action = value

    @move_action_likelihood.setter
    def move_action_likelihood(self, value):
        self._move_action_likelihood = value

    @red_uses_zero_day_action.setter
    def red_uses_zero_day_action(self, value):
        self._red_uses_zero_day_action = value

    @zero_day_start_amount.setter
    def zero_day_start_amount(self, value):
        self._zero_day_start_amount = value

    @days_required_for_zero_day.setter
    def days_required_for_zero_day(self, value):
        self._days_required_for_zero_day = value

    @red_chooses_target_at_random.setter
    def red_chooses_target_at_random(self, value):
        self._red_chooses_target_at_random = value

    @red_target_node.setter
    def red_target_node(self, value):
        self._red_target_node = value

    @red_prioritises_connected_nodes.setter
    def red_prioritises_connected_nodes(self, value):
        self._red_prioritises_connected_nodes = value

    @red_prioritises_un_connected_nodes.setter
    def red_prioritises_un_connected_nodes(self, value):
        self._red_prioritises_un_connected_nodes = value

    @red_prioritises_vulnerable_nodes.setter
    def red_prioritises_vulnerable_nodes(self, value):
        self._red_prioritises_vulnerable_nodes = value

    @red_prioritises_resilient_nodes.setter
    def red_prioritises_resilient_nodes(self, value):
        self._red_prioritises_resilient_nodes = value

    @red_always_chooses_shortest_distance_to_target.setter
    def red_always_chooses_shortest_distance_to_target(self, value):
        self._red_always_chooses_shortest_distance_to_target = value

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> RedAgentConfig:
        """
        Creates an instance of :class:`RedAgentConfig <yawning_titan.config.agents.red_agent_config.RedAgentConfig>.

        This calls :func:`validate() <yawning_titan.config.agents.red_agent_config.RedAgentConfig.validate>.

        :param: config_dict: A config dict with the required key/values pairs.

        :return: An instance of :class:`RedAgentConfig <yawning_titan.config.agents.red_agent_config.RedAgentConfig>.
        """
        # validate red agent config values
        cls.validate(config_dict)

        red_agent_config = RedAgentConfig(
            _red_skill=config_dict["red_skill"],
            _red_uses_skill=config_dict["red_uses_skill"],
            _red_ignores_defences=config_dict["red_ignores_defences"],
            _red_always_succeeds=config_dict["red_always_succeeds"],
            _red_can_only_attack_from_red_agent_node=config_dict[
                "red_can_only_attack_from_red_agent_node"
            ],
            _red_can_attack_from_any_red_node=config_dict[
                "red_can_attack_from_any_red_node"
            ],
            _red_can_naturally_spread=config_dict["red_can_naturally_spread"],
            _chance_to_spread_to_connected_node=config_dict[
                "chance_to_spread_to_connected_node"
            ],
            _chance_to_spread_to_unconnected_node=config_dict[
                "chance_to_spread_to_unconnected_node"
            ],
            _red_uses_spread_action=config_dict["red_uses_spread_action"],
            _spread_action_likelihood=config_dict["spread_action_likelihood"],
            _chance_for_red_to_spread=config_dict["chance_for_red_to_spread"],
            _red_uses_random_infect_action=config_dict["red_uses_random_infect_action"],
            _random_infect_action_likelihood=config_dict[
                "random_infect_action_likelihood"
            ],
            _chance_for_red_to_random_compromise=config_dict[
                "chance_for_red_to_random_compromise"
            ],
            _red_uses_basic_attack_action=config_dict["red_uses_basic_attack_action"],
            _basic_attack_action_likelihood=config_dict[
                "basic_attack_action_likelihood"
            ],
            _red_uses_do_nothing_action=config_dict["red_uses_do_nothing_action"],
            _do_nothing_action_likelihood=config_dict["do_nothing_action_likelihood"],
            _red_uses_move_action=config_dict["red_uses_move_action"],
            _move_action_likelihood=config_dict["move_action_likelihood"],
            _red_uses_zero_day_action=config_dict["red_uses_zero_day_action"],
            _zero_day_start_amount=config_dict["zero_day_start_amount"],
            _days_required_for_zero_day=config_dict["days_required_for_zero_day"],
            _red_chooses_target_at_random=config_dict["red_chooses_target_at_random"],
            _red_target_node=config_dict["red_target_node"],
            _red_prioritises_connected_nodes=config_dict[
                "red_prioritises_connected_nodes"
            ],
            _red_prioritises_un_connected_nodes=config_dict[
                "red_prioritises_un_connected_nodes"
            ],
            _red_prioritises_vulnerable_nodes=config_dict[
                "red_prioritises_vulnerable_nodes"
            ],
            _red_prioritises_resilient_nodes=config_dict[
                "red_prioritises_resilient_nodes"
            ],
            _red_always_chooses_shortest_distance_to_target=config_dict[
                "red_always_chooses_shortest_distance_to_target"
            ],
        )

        return red_agent_config

    @classmethod
    def validate(cls, config_dict: dict):
        """
        Validates the red agent config dict.

        :param: config_dict: A config dict with the required key/values pairs.
        """
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
