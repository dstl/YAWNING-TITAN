from typing import Union, List

import yawning_titan.envs.generic.core.reward_functions as reward_functions


def check_type(data: dict, name: str, types: list):
    """
    Check data types contained within a dictionary is one of a list of types.

    Args:
        data: The dictionary
        name: The name of the key of the item to check
        types: A list of types that the item must belong to
    """
    if type(data[name]) not in types:
        raise ValueError(
            "'" + name + "' needs to be of type: " + " or ".join(map(str, types))
        )


def check_within_range(
        data: dict,
        name: str,
        lower: Union[None, float],
        upper: Union[None, float],
        l_inclusive: bool,
        u_inclusive: bool,
):
    """
    Check that an item belonging to a dictionary fits within a certain numerical range (either inclusive or not).

    If upper or lower are None then ignores that direction.

    Args:
        data: The dictionary where the item is held
        name: The name of the key that corresponds to the item
        lower: The lower bound for the range (None means no lower bound)
        upper: The upper bound for the range (None means no upper bound)
        l_inclusive: Boolean - True for inclusive, False for not
        u_inclusive: Boolean - True for inclusive, False for not
    """
    if lower is not None:
        if l_inclusive is False:
            if data[name] <= lower:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value greater than: "
                    + str(lower)
                    + " (not inclusive)"
                )
        else:
            if data[name] < lower:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value greater than: "
                    + str(lower)
                    + " (inclusive)"
                )
    if upper is not None:
        if u_inclusive is False:
            if data[name] >= upper:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value less than: "
                    + str(upper)
                    + " (not inclusive)"
                )
        else:
            if data[name] > upper:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value less than: "
                    + str(upper)
                    + " (inclusive)"
                )


def check_red(data: dict):
    """
    Check all of the settings relating to the red agent.

    Args:
        data: The dictionary for settings relating to the red agent

    """
    # type of data is either int or float
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


def check_blue(data: dict):
    """
    Check all of the settings relating to the blue agent.

    Args:
        data: The dictionary of settings for the blue agent
    """
    # data is int or float
    for name in [
        "chance_to_immediately_discover_intrusion",
        "chance_to_discover_intrusion_on_scan",
        "vulnerability_change_during_node_patch",
        "chance_to_discover_failed_attack",
        "chance_to_discover_succeeded_attack_compromise_known",
        "chance_to_discover_succeeded_attack_compromise_not_known",
        "chance_to_immediately_discover_intrusion_deceptive_node",
        "chance_to_discover_intrusion_on_scan_deceptive_node",
        "chance_to_discover_failed_attack_deceptive_node",
        "chance_to_discover_succeeded_attack_deceptive_node",
        "vulnerability_change_during_node_patch",
    ]:
        check_type(data, name, [int, float])
    # data is int
    for name in ["max_number_deceptive_nodes"]:
        check_type(data, name, [int])

    # data is bool
    for name in [
        "making_node_safe_modifies_vulnerability",
        "making_node_safe_gives_random_vulnerability",
        "blue_uses_reduce_vulnerability",
        "blue_uses_restore_node",
        "blue_uses_make_node_safe",
        "blue_uses_scan",
        "blue_uses_isolate_node",
        "blue_uses_reconnect_node",
        "blue_uses_do_nothing",
        "blue_uses_deceptive_nodes",
        "can_discover_failed_attacks",
        "can_discover_succeeded_attacks_if_compromise_is_discovered",
        "can_discover_succeeded_attacks_if_compromise_is_not_discovered",
        "relocating_deceptive_nodes_generates_a_new_node",
    ]:
        check_type(data, name, [bool])

    # data is between 0 and 1 inclusive
    for name in [
        "chance_to_immediately_discover_intrusion",
        "chance_to_immediately_discover_intrusion_deceptive_node",
        "chance_to_discover_intrusion_on_scan_deceptive_node",
        "chance_to_discover_intrusion_on_scan",
        "chance_to_discover_failed_attack",
        "chance_to_discover_succeeded_attack_compromise_known",
        "chance_to_discover_succeeded_attack_compromise_not_known",
        "chance_to_discover_failed_attack_deceptive_node",
        "chance_to_discover_succeeded_attack_deceptive_node",
    ]:
        check_within_range(data, name, 0, 1, True, True)

    check_within_range(
        data, "vulnerability_change_during_node_patch", -1, 1, True, True
    )

    # misc
    if (
            not data["blue_uses_reduce_vulnerability"]
            and (not data["blue_uses_restore_node"])
            and (not data["blue_uses_make_node_safe"])
            and (not data["blue_uses_scan"])
            and (not data["blue_uses_isolate_node"])
            and (not data["blue_uses_reconnect_node"])
            and (not data["blue_uses_do_nothing"])
            and (not data["blue_uses_deceptive_nodes"])
    ):
        raise ValueError(
            "'blue_uses_****' -> Blue must have at least one action selected. If you want blue to do nothing set 'blue_uses_do_nothing' to True"
            # noqa
        )

    if (data["blue_uses_isolate_node"] and (not data["blue_uses_reconnect_node"])) or (
            (not data["blue_uses_isolate_node"]) and data["blue_uses_reconnect_node"]
    ):
        raise ValueError(
            "'blue_uses_isolate_node', 'blue_uses_reconnect_node' -> Blue should be able to reconnect or isolate nodes if the other is true"
            # noqa
        )

    check_within_range(data, "max_number_deceptive_nodes", 0, None, True, True)

    if data["blue_uses_deceptive_nodes"] and (0 == data["max_number_deceptive_nodes"]):
        raise ValueError(
            "'blue_uses_deceptive_nodes', 'max_number_deceptive_nodes' -> If blue can use deceptive nodes then max_number_deceptive_nodes."
            # noqa
        )

    if data["blue_uses_scan"]:
        if data["chance_to_immediately_discover_intrusion"] == 1:
            raise ValueError(
                "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> The scan action is selected yet blue has 100% chance to spot detections. There is no need for the blue to have the scan action in this case"
                # noqa
            )
    else:
        if data["chance_to_immediately_discover_intrusion"] != 1:
            raise ValueError(
                "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> If the blue agent cannot scan nodes then it should be able to automtically detect the intrusions"
                # noqa
            )

    if (
            data["chance_to_discover_intrusion_on_scan_deceptive_node"]
            <= data["chance_to_discover_intrusion_on_scan"]
    ):
        if data["chance_to_discover_intrusion_on_scan_deceptive_node"] != 1:
            raise ValueError(
                "'chance_to_discover_intrusion_on_scan_deceptive_node', 'chance_to_discover_intrusion_on_scan' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                # noqa
            )

    if (
            data["chance_to_discover_failed_attack_deceptive_node"]
            <= data["chance_to_discover_failed_attack"]
    ):
        if data["chance_to_discover_failed_attack_deceptive_node"] != 1:
            raise ValueError(
                "'chance_to_discover_failed_attack_deceptive_node', 'chance_to_discover_failed_attack' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                # noqa
            )

    if (
            data["chance_to_discover_succeeded_attack_deceptive_node"]
            <= data["chance_to_discover_succeeded_attack_compromise_known"]
    ):
        if data["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
            raise ValueError(
                "'chance_to_discover_succeeded_attack_deceptive_node', 'chance_to_discover_succeeded_attack_compromise_known' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                # noqa
            )

    if (
            data["chance_to_discover_succeeded_attack_deceptive_node"]
            <= data["chance_to_discover_succeeded_attack_compromise_not_known"]
    ):
        if data["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
            raise ValueError(
                "'chance_to_discover_succeeded_attack_deceptive_node', 'chance_to_discover_succeeded_attack_compromise_not_known' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                # noqa
            )

    if (
            data["making_node_safe_gives_random_vulnerability"]
            and data["making_node_safe_modifies_vulnerability"]
    ):
        raise ValueError(
            "'making_node_safe_gives_random_vulnerability', 'making_node_safe_modifies_vulnerability' -> Does not make sense to give a node a random vulnerability and to increase its vulnerability when a node is made safe"
            # noqa
        )

    if (
            data["chance_to_immediately_discover_intrusion_deceptive_node"]
            <= data["chance_to_immediately_discover_intrusion"]
    ):
        if data["chance_to_immediately_discover_intrusion_deceptive_node"] != 1:
            raise ValueError(
                "'chance_to_immediately_discover_intrusion_deceptive_node', 'chance_to_immediately_discover_intrusion' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                # noqa
            )


def check_game_rules(data: dict, number_of_nodes: int, high_value_targets: List[str]):
    """
    Check the settings relating to the game rules.

    Args:
        data: The dictionary relating to the game rules settings
        number_of_nodes: The number of nodes in the network
        high_value_targets: The list containing the high value targets

    """
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
    check_type(data, "number_of_high_value_targets", [int])
    check_within_range(data, "grace_period_length", 0, 100, True, True)
    check_within_range(data, "max_steps", 0, 10000000, False, True)
    check_within_range(data, "number_of_entry_nodes", 0, number_of_nodes, False, True)
    check_within_range(data, "number_of_high_value_targets", 1, number_of_nodes, True, True)
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
                "Provided high value targets: " + str(high_value_targets) + " 'choose_high_value_targets_placement_at_random', 'choose_high_value_targets_furthest_away_from_entry' -> Only one method of selecting a high value target should be selected"
                # noqa
            )

    if data["grace_period_length"] > data["max_steps"]:
        raise ValueError(
            "'grace_period_length', 'max_steps' -> The grace period cannot be the entire length of the game"
        )


def check_reset(data: dict):
    """
    Check the settings relating to resets.

    Args:
        data: The settings related to resets
    """
    for name in [
        "randomise_vulnerabilities_on_reset",
        "choose_new_high_value_targets_on_reset",
        "choose_new_entry_nodes_on_reset",
    ]:
        check_type(data, name, [bool])


def check_rewards(data: dict):
    """
    Check the settings relating to the rewards.

    Args:
        data: The dictionary of settings for the rewards
    """
    check_type(data, "rewards_for_loss", [int, float])
    check_type(data, "rewards_for_reaching_max_steps", [int, float])
    check_type(data, "end_rewards_are_multiplied_by_end_state", [bool])
    check_type(data, "reduce_negative_rewards_for_closer_fails", [bool])


def check_reward_function_exists(data: dict):
    """
    Check that the reward function that the settings file contains exists.

    Args:
        data: The dictionary containing reward settings
    """
    if not hasattr(reward_functions, data["reward_function"]):
        raise ValueError(
            "The reward function '"
            + data["reward_function"]
            + "' does not exist inside: yawning_titan.envs.helpers.reward_functions"
        )


def check_misc(data: dict):
    """
    Check the misc settings.

    Args:
        data: The dictionary for the misc settings

    """
    check_type(data, "output_timestep_data_to_json", [bool])


def check_observation_space(data: dict):
    """Check the observation space settings."""
    all_obs = [
        "compromised_status",
        "vulnerabilities",
        "node_connections",
        "average_vulnerability",
        "graph_connectivity",
        "attacking_nodes",
        "attacked_nodes",
        "special_nodes",
        "red_agent_skill",
    ]
    for name in all_obs:
        check_type(data, name, [bool])

    if True not in list(map(lambda x: data[x], all_obs)):
        raise ValueError(
            "At least one option from OBSERVATION_SPACE must be enabled. The observation space must contain at least one item"
        )


def check_input(data: dict, number_of_nodes: int, high_value_targets: List[str]):
    """
    Check the settings file making sure that all the required settings are there and that they contain suitable values.

    Args:
        data: The settings file (A dictionary)
        number_of_nodes: The number of nodes in the network
        high_value_targets: The list containing the high value targets
    """
    try:
        red = data["RED"]
        blue = data["BLUE"]
        game = data["GAME_RULES"]
        rewards = data["REWARDS"]
        misc = data["MISCELLANEOUS"]
        observation_space = data["OBSERVATION_SPACE"]
        reset = data["RESET"]

        # runs the checks for each section of the settings
        check_red(red)
        check_blue(blue)
        check_game_rules(game, number_of_nodes, high_value_targets)
        check_rewards(rewards)
        check_reward_function_exists(rewards)
        check_misc(misc)
        check_observation_space(observation_space)
        check_reset(reset)

        # tests based on multiple sections
        if red["red_ignores_defences"]:
            if blue["making_node_safe_modifies_vulnerability"]:
                raise ValueError(
                    "If red ignores defences then there is no reason for the node vulnerabilities to change"
                )
            if blue["making_node_safe_gives_random_vulnerability"]:
                raise ValueError(
                    "If red ignores defences then there is no reason for the node vulnerabilities to change"
                )
            if blue["blue_uses_reduce_vulnerability"]:
                raise ValueError(
                    "If red ignores defences then there is no reason for the node vulnerabilities to change"
                )
    except KeyError as error:
        # If a setting does not exist, error
        raise IOError(
            "Config file corrupted or missing information. Error received : "
            + repr(error)
        )
