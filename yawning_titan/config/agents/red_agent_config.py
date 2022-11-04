from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type, check_within_range


@dataclass
class RedAgentConfig(ConfigGroupABC):
    """
    Class that validates and stores the Red Agent Configuration
    """

    # red agent skill
    red_skill: float
    """Red agent's skill modifier"""

    red_use_skill: bool
    """Is true if red agent will use the skill modifier when attacking a node"""

    # red agent attack pattern
    red_ignores_defences: bool
    """Is true if red agent will ignore node defences"""

    red_always_succeeds: bool
    """Is true if red agent will always succeed when attacking"""

    red_attack_from_current_position: bool
    """Is true if red agent can only attack from its current position"""

    red_attack_from_any_node: bool
    """Is true if red can attack any safe node anywhere in the network"""

    # red spread
    red_naturally_spread: bool
    """Is true if red can naturally spread every timestep"""

    red_chance_to_spread_to_connected_node: float
    """Chance of red agent spreading to a connected safe node"""

    red_chance_to_spread_to_unconnected_node: float
    """Chance of red agent spreading to an unconnected safe node"""

    red_spread_action: bool
    """Is true if red can try to spread to every connected safe node"""

    red_spread_action_likelihood: float
    """Chance of red agent to try and spread to every connected safe node"""

    red_spread_success_chance: float
    """Chance for red agent spread action to succeed"""

    red_random_infection_action: bool
    """Is true if red agent can attack any safe node in the network"""

    red_random_infection_likelihood: float
    """Chance of the red agent attacking any random safe node"""

    red_random_infection_success_chance: float
    """Chance of the random safe node attacks from succeeding"""

    red_basic_attack_action: bool
    """Is true if red uses a basic attack to take over a safe node connected to an infected node"""

    red_basic_attack_likelihood: float
    """Chance of the basic attack succeeding"""

    # red do nothing
    red_do_nothing_action: bool
    """Is true if the red agent can choose to do nothing"""
    red_do_nothing_likelihood: float
    """Chance of the red agent from doing nothing"""

    # red movement
    red_move_action: bool
    """Is true if the red agent can choose to move to another infected node"""

    red_move_action_likelihood: float
    """Chance of red agent choosing to move to another infected node"""

    # red zero days
    red_zero_day_action: bool
    """Is true if the red agent can use a zero day to infect a node with 100% success"""

    red_zero_day_start_amount: int
    """Integer value specifying how many zero days the red agent can use at the start of the game"""

    red_zero_day_days_required_to_create: int
    """Integer value specifying how many timesteps is needed until the red agent can get another zero day"""

    # red targeting
    red_targeting_random: bool
    """Is true if the red agent targets safe nodes at random"""

    red_targeting_prioritise_connected_nodes: bool
    """Is true if the red agent prioritises attacking nodes with the most connections"""

    red_targeting_prioritise_unconnected_nodes: bool
    """Is true if the red agent prioritises attacking nodes with the least connections"""

    red_targeting_prioritise_vulnerable_nodes: bool
    """Is true if the red agent prioritises attacking nodes with the most vulnerability"""

    red_targeting_prioritise_resilient_nodes: bool
    """Is true if the red agent prioritises attacking nodes with the least vulnerability"""

    @classmethod
    def create(cls,settings: Dict[str, Any]) -> RedAgentConfig:
        # validate red agent config values
        cls._validate(settings)

        red_agent = RedAgentConfig(

            red_skill=settings["red_skill"],
            red_use_skill=settings["red_uses_skill"],
            red_ignores_defences=settings["red_ignores_defences"],
            red_always_succeeds=settings["red_always_succeeds"],
            red_attack_from_current_position=settings[
                "red_can_only_attack_from_red_agent_node"
            ],
            red_attack_from_any_node=settings[
                "red_can_attack_from_any_red_node"
            ],
            red_naturally_spread=settings["red_can_naturally_spread"],
            red_chance_to_spread_to_connected_node=settings[
                "chance_to_spread_to_connected_node"
            ],
            red_chance_to_spread_to_unconnected_node=settings[
                "chance_to_spread_to_unconnected_node"
            ],
            red_spread_action=settings["red_uses_spread_action"],
            red_spread_action_likelihood=settings[
                "spread_action_likelihood"
            ],
            red_spread_success_chance=settings["chance_for_red_to_spread"],
            red_random_infection_action=settings[
                "red_uses_random_infect_action"
            ],
            red_random_infection_likelihood=settings[
                "random_infect_action_likelihood"
            ],
            red_random_infection_success_chance=settings[
                "chance_for_red_to_random_compromise"
            ],
            red_basic_attack_action=settings["red_uses_basic_attack_action"],
            red_basic_attack_likelihood=settings[
                "basic_attack_action_likelihood"
            ],
            red_do_nothing_action=settings["red_uses_do_nothing_action"],
            red_do_nothing_likelihood=settings[
                "do_nothing_action_likelihood"
            ],
            red_move_action=settings["red_uses_move_action"],
            red_move_action_likelihood=settings["move_action_likelihood"],
            red_zero_day_action=settings["red_uses_zero_day_action"],
            red_zero_day_start_amount=settings["zero_day_start_amount"],
            red_zero_day_days_required_to_create=settings[
                "days_required_for_zero_day"
            ],
            red_targeting_random=settings["red_chooses_target_at_random"],
            red_targeting_prioritise_connected_nodes=settings[
                "red_prioritises_connected_nodes"
            ],
            red_targeting_prioritise_unconnected_nodes=settings[
                "red_prioritises_un_connected_nodes"
            ],
            red_targeting_prioritise_vulnerable_nodes=settings[
                "red_prioritises_vulnerable_nodes"
            ],
            red_targeting_prioritise_resilient_nodes=settings[
                "red_prioritises_resilient_nodes"
            ]
        )

        return red_agent

    @classmethod
    def _validate(
            cls,
            data: dict
    ):
        """
        Validate the red agent configuration

        Args:
            data: dictionary of the red agent configuration
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
            check_type(data, name, [int, float])

        # int
        for name in ["zero_day_start_amount", "days_required_for_zero_day"]:
            check_type(data, name, [int])

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
        ]:
            check_type(data, name, [bool])

        # data satisfies 0 <= data <= 1
        for name in [
            "red_skill",
            "chance_for_red_to_spread",
            "chance_for_red_to_random_compromise",
            "chance_to_spread_to_connected_node",
            "chance_to_spread_to_unconnected_node",
        ]:
            check_within_range(data, name, 0, 1, True, True)

        # data satisfies 0 < data
        for name in [
            "spread_action_likelihood",
            "random_infect_action_likelihood",
            "basic_attack_action_likelihood",
            "do_nothing_action_likelihood",
            "move_action_likelihood",
        ]:
            check_within_range(data, name, 0, None, False, True)

        # data satisfies 0 <= data
        for name in ["zero_day_start_amount", "days_required_for_zero_day"]:
            check_within_range(data, name, 0, None, True, True)

        # misc
        if (
                (not data["red_uses_skill"])
                and (not data["red_always_succeeds"])
                and data["red_ignores_defences"]
        ):
            raise ValueError(
                "'red_uses_skill', 'red_always_succeeds', 'red_ignores_defences' -> Red must either use skill, always succeed or not ignore the defences of the nodes"
                # noqa
            )
        if (
                (not data["red_uses_spread_action"])
                and (not data["red_uses_random_infect_action"])
                and (not data["red_uses_zero_day_action"])
                and (not data["red_uses_basic_attack_action"])
                and (not data["red_uses_do_nothing_action"])
        ):
            raise ValueError(
                "'red_uses_*****' -> Red must have at least one action activated"
            )
        if (
                (not data["red_chooses_target_at_random"])
                and (not data["red_prioritises_connected_nodes"])
                and (not data["red_prioritises_un_connected_nodes"])
                and (not data["red_prioritises_vulnerable_nodes"])
                and (not data["red_prioritises_resilient_nodes"])
        ):
            raise ValueError(
                "'red_prioritises_****' -> Red must choose its target in some way. If you are unsure select 'red_chooses_target_at_random'"
                # noqa
            )
        if (not data["red_can_only_attack_from_red_agent_node"]) and (
                not data["red_can_attack_from_any_red_node"]
        ):
            raise ValueError(
                "'red_can_only_attack_from_red_agent_node', 'red_can_attack_from_any_red_node' -> The red agent must be able to attack either from every red node or just the red central node"
                # noqa
            )
        if (
                data["red_prioritises_vulnerable_nodes"]
                or data["red_prioritises_resilient_nodes"]
        ):
            if data["red_ignores_defences"]:
                raise ValueError(
                    "'red_ignores_defences', 'red_prioritises_vulnerable_nodes', 'red_prioritises_resilient_nodes' -> It makes no sense for red to prioritise nodes based on a stat that is ignored (vulnerability)"
                    # noqa
                )
        # spread both 0 but spreading on?
        if data["red_can_naturally_spread"]:
            if (
                    data["chance_to_spread_to_connected_node"] == 0
                    and data["chance_to_spread_to_unconnected_node"] == 0
            ):
                raise ValueError(
                    "'red_can_naturally_spread', 'chance_to_spread_to_connected_node', 'chance_to_spread_to_unconnected_node' -> If red can naturally spread however the probabilities for both types of spreading are 0"
                    # noqa
                )
