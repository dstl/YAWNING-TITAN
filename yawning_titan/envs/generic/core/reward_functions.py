"""
A collection of reward functions used be the generic network environment.

You can select the reward function that you wish to use in the config file under settings.
The reward functions take in a parameter called args. args is a dictionary that contains the
following information:
    -network_interface: Interface with the network
    -blue_action: The action that the blue agent has taken this turn
    -blue_node: The node that the blue agent has targeted for their action
    -start_state: The state of the nodes before the blue agent has taken their action
    -end_state: The state of the nodes after the blue agent has taken their action
    -start_vulnerabilities: The vulnerabilities before blue agents turn
    -end_vulnerabilities: The vulnerabilities after the blue agents turn
    -start_isolation: The isolation status of all the nodes at the start of a turn
    -end_isolation: The isolation status of all the nodes at the end of a turn
    -start_blue: The env as the blue agent can see it before the blue agents turn
    -end_blue: The env as the blue agent can see it after the blue agents turn

The reward function returns a single number (integer or float) that is the blue agents reward for that turn.
"""

# Functions:
import math

REMOVE_RED_POINTS = []
for i in range(0, 101):
    REMOVE_RED_POINTS.append(round(math.exp(-0.004 * i), 4))

REDUCE_VULNERABILITY_POINTS = []
for i in range(1, 20):
    REDUCE_VULNERABILITY_POINTS.append(2 / (10 + math.exp(4 - 10 * (i / 20))) + 0.5)

SCANNING_USAGE_POINTS = []
for i in range(0, 100):
    SCANNING_USAGE_POINTS.append(-math.exp(-i) + 1)


def standard_rewards(args: dict) -> float:
    """
    Calculate the reward for the current state of the environment.

    Actions cost a certain amount and blue gets rewarded for removing red nodes and
    reducing the vulnerability of nodes

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    network_interface = args["network_interface"]
    blue_action = args["blue_action"]
    start_state = args["start_state"]
    end_state = args["end_state"]
    start_vulnerabilities = args["start_vulnerabilities"]
    end_vulnerabilities = args["end_vulnerabilities"]
    start_isolation = args["start_isolation"]
    end_isolation = args["end_isolation"]
    start_blue = args["start_blue"]
    end_blue = args["end_blue"]

    # cost for actions
    action_cost = {
        "reduce_vulnerability": 0.5,
        "restore_node": 1,
        "make_node_safe": 0.5,
        "scan": 0,
        "isolate": 10,
        "connect": 0,
        "do_nothing": -0.5,
        "add_deceptive_node": 8,
    }

    reward = -action_cost[blue_action]
    # calculating number of red nodes before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == "do_nothing":
        reward = reward - (0.2 * final_cumulative_states)

    if blue_action == "connect":
        if sum(end_isolation.values()) < sum(start_isolation.values()):
            reward += 5
        else:
            reward -= 5

    # rewards for removing red nodes
    if initial_cumulative_states > final_cumulative_states:
        reward += REMOVE_RED_POINTS[
            round(
                100 * final_cumulative_states / network_interface.get_number_of_nodes()
            )
        ]

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action != "make_node_safe" and blue_action != "restore_node":
        amount = final_cumulative_states / network_interface.get_number_of_nodes()
        if amount > 0.3:
            reward = reward - amount + 0.3

    # punish the blue agent for patching nodes that are already safe
    if blue_action == "make_node_safe" or blue_action == "restore_node":
        if initial_cumulative_states == final_cumulative_states:
            reward = reward - 3

    # punish the blue agent for reducing the vulnerability of a node that is already at minimum vulnerability
    if blue_action == "reduce_vulnerability" or blue_action == "restore_node":
        if sum(start_vulnerabilities.values()) == sum(end_vulnerabilities.values()):
            reward = reward - 0.5

    # reward for revealing red
    if blue_action == "scan":
        number = 0
        for node, value in end_blue.items():
            if value == 1 and start_blue[node] == 0:
                if start_state[node] == 1:
                    number += 1
        if number >= 5:
            reward += 2.5
        else:
            reward += number * 0.5

    # rewards for reducing node vulnerabilities
    if (
        network_interface.game_mode.red.red_ignores_defences is False
        and blue_action == "reduce_vulnerability"
    ):
        initial_cumulative_vuln = sum(start_vulnerabilities.values())
        final_cumulative_vuln = sum(end_vulnerabilities.values())
        reward = reward + (initial_cumulative_vuln - final_cumulative_vuln) * 4

    if blue_action == "add_deceptive_node":
        if network_interface.reached_max_deceptive_nodes:
            reward -= 5

    return reward


def experimental_rewards(args: dict) -> float:
    """
    Calculate the reward for the current state of the environment.

    Actions cost a certain amount and blue gets rewarded for removing red nodes and
    reducing the vulnerability of nodes

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    network_interface = args["network_interface"]
    blue_action = args["blue_action"]
    start_state = args["start_state"]
    end_state = args["end_state"]
    start_blue = args["start_blue"]
    end_blue = args["end_blue"]

    # cost for actions
    action_cost = {
        "reduce_vulnerability": 0,
        "restore_node": 1,
        "make_node_safe": 0,
        "scan": 0,
        "isolate": 10,
        "connect": 0,
        "do_nothing": -0.5,
        "add_deceptive_node": 2,
    }

    reward = -action_cost[blue_action]
    # calculating number of red nodes before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())
    # calculating the vulnerability of all the nodes before and after the blue agents turn
    # blue's view
    initial_blue_states = sum(start_blue.values())
    final_blue_states = sum(end_blue.values())

    # rewards for removing red nodes
    # gives between 0.5 and 1
    if blue_action == "make_node_safe" or blue_action == "restore_node":
        if initial_blue_states > final_blue_states:
            reward += REMOVE_RED_POINTS[
                round(
                    100
                    * final_cumulative_states
                    / network_interface.get_number_of_nodes()
                )
            ]
        elif initial_cumulative_states > final_cumulative_states:
            pass
        else:
            reward -= 1

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == "do_nothing":
        reward = reward - (0.5 * final_cumulative_states)

    vision_score = 0.01 * (final_cumulative_states - final_blue_states) ** 2

    reward -= vision_score

    return reward


# A very simple example reward function
def one_per_timestep(args: dict) -> float:
    """
    Give a reward for 0.1 for every timestep that the blue agent is alive.

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        0.1
    """
    return 0.1


def zero_reward(args: dict) -> float:
    """
    Return zero reward per timestep.

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        0
    """
    return 0


def safe_nodes_give_rewards(args: dict) -> float:
    """
    Give 1 reward for every safe node at that timestep.

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    end_state = args["end_state"]

    final_cumulative_states = sum(end_state.values())

    # reward is equal to the number of safe nodes
    reward = len(end_state) - final_cumulative_states

    return reward


def punish_bad_actions(args: dict) -> float:
    """
    Just punishes bad actions bad moves.

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent

    """
    # Get information about the current state of the game
    network_interface = args["network_interface"]
    blue_action = args["blue_action"]
    start_state = args["start_state"]
    end_state = args["end_state"]
    start_vulnerabilities = args["start_vulnerabilities"]
    end_vulnerabilities = args["end_vulnerabilities"]

    # Get number of safe states before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())

    reward = 0

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == "do_nothing":
        reward = reward - (0.5 * final_cumulative_states)
    # punish the blue agent for patching nodes that are already safe
    if blue_action == "make_node_safe" or blue_action == "restore_node":
        if initial_cumulative_states == final_cumulative_states:
            reward = reward - (0.2 * initial_cumulative_states)

    # punish the blue agent for reducing the vulnerability of a node that is already at minimum vulnerability
    if blue_action == "reduce_vulnerability" and (
        sum(start_vulnerabilities.values()) == sum(end_vulnerabilities.values())
    ):
        reward = reward - 1

    # punish for relocating deceptive nodes (after it has already been placed)
    if blue_action == "add_deceptive_node":
        if network_interface.reached_max_deceptive_nodes:
            reward = reward - 5

    return reward


def num_nodes_safe(args: dict) -> float:
    """
    Provide reward based on the proportion of nodes safe within the environment.

    Args:
        args: A dictionary containing information from the
        environment for the given timestep

    Returns:
        The calculated reward
    """
    total_n_nodes = len(args["end_state"].values())
    n_compromised = sum(args["end_state"].values())
    n_safe = total_n_nodes - n_compromised

    return n_safe / total_n_nodes


def dcbo_cost_func(args: dict) -> float:
    """
    Calculate the cost function for DCBO using a set of fixed action cost values.

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The cost for DCBO
    """
    # Get information about the current state of the environment
    blue_action = args["blue_action"]
    end_state = args["end_state"]

    # cost for actions
    action_cost = {
        "reduce_vulnerability": 0,
        "restore_node": 1,
        "make_node_safe": 1,
        "scan": 0,
        "isolate": 1,
        "connect": 0,
        "do_nothing": 0,
        "add_deceptive_node": 0,
    }

    reward = action_cost[blue_action]
    # calculating number of red nodes before and after the blue agents turn
    final_cumulative_states = sum(end_state.values())

    cost = final_cumulative_states * 10 + reward

    return 0 - cost
