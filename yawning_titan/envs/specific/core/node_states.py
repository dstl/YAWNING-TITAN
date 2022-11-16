from typing import List, Tuple

import networkx as nx

"""
node_states.py

This module contains helper functions to find compromised and uncompromised nodes for
the four-node-def-v0 and five-node-def-v0 environments.
"""


def get_linked_node_state(
    current_position: int, network: nx.Graph, machine_states: List[List[float]]
) -> Tuple[List[int], List[int]]:
    """
    Calculate the state of the nodes linked the red team's current position.

    Args:
        current_position: The current Red Team's location
        network: A networkx graph representation of the network
        machine_states: The current machine states

    Returns:
        uncompromised_nodes: A list of uncompromised linked nodes
        compromised_nodes: A list of compromised linked nodes
    """
    linked_nodes = list(network.edges(current_position))
    uncompromised_nodes = []
    compromised_nodes = []

    for i in range(len(linked_nodes)):
        node = linked_nodes[i][1]

        if machine_states[node][1] == 0:
            uncompromised_nodes.append(node)
        else:
            compromised_nodes.append(node)

    return uncompromised_nodes, compromised_nodes


def get_linked_compromised_nodes(
    current_position: int, network: nx.Graph, machine_states: List[List[float]]
) -> List[int]:
    """
    Return a list containing all the linked compromised nodes relative to the red agents current position.

    Args:
        current_position: The red teams current position
        network: A networkx graph representation of the network
        machine_states: The current machine states

    Returns:
        compromised nodes: A list of comrpomised linked nodes
    """
    linked_nodes = list(network.edges(current_position))
    compromised_nodes = []

    for i in range(len(linked_nodes)):
        node = linked_nodes[i][1]

        if machine_states[node][1] == 1:
            compromised_nodes.append(node)
    return compromised_nodes


def get_linked_uncompromised_nodes(
    current_position: int, network: nx.Graph, machine_states: List[List[float]]
) -> List[int]:
    """
    Return a list containing all the linked uncompromised nodes relative to the red agents current position.

    Args:
        current_position: The red teams current position
        network: A networkx graph representation of the network
        machine_states: The current machine states

    Returns:
        compromised nodes: A list of uncomrpomised linked nodes
    """
    linked_nodes = list(network.edges(current_position))
    uncompromised_nodes = []

    for i in range(len(linked_nodes)):
        node = linked_nodes[i][1]

        if machine_states[node][1] == 0:
            uncompromised_nodes.append(node)
    return uncompromised_nodes


def get_uncompromised_nodes(machine_states: List[List[float]]) -> List[int]:
    """
    Return a list of uncompromised nodes.

    Args:
        machine_states: The current machine states

    Returns:
        A list of uncompromised nodes

    Notes:
        This differs from the similar function above
        because this function does not support returning
        uncompromised nodes based on an agents current
        position
    """
    uncompromised_nodes = []

    for i in range(len(machine_states)):
        if machine_states[i][1] == 0:
            uncompromised_nodes.append(i)

    return uncompromised_nodes


def get_compromised_nodes(machine_states: List[List[float]]) -> List[int]:
    """
    Return a list of compromised nodes.

    Args:
        machine_states: The current machine states

    Returns:
        A list of compromised nodes

    Notes:
        This differs from the similar function above
        because this function does not support returning
        uncompromised nodes based on an agents current
        position
    """
    compromised_nodes = []

    for i in range(len(machine_states)):
        if machine_states[i][1] == 1:
            compromised_nodes.append(i)

    return compromised_nodes
