"""
Network Creator module enables the creation of pre-defined types of networks.

Networks that can be created are:

- The standard 18-node network from the Ridley 2017 paper.
- The DCBO network used in the RL Baseline module.
- A mesh network.
- A star network.
- A ring network.
- A P2P network.
- A randomly generated binominal network.
- A custom network using user-input options.
"""
import math
import random
from itertools import combinations, groupby
from typing import Any, Dict, List, Union

import networkx as nx
import numpy as np

from yawning_titan.networks.network import Network
from yawning_titan.networks.node import Node


def check_if_nearby(pos: List[float], full_list: dict, value: int) -> bool:
    """
    Check if a randomly generated point is close to points already generated.

    :param pos: The x,y position as a list.
    :param full_list: The full list of positions.
    :param value: The separation value.
    :return: True if nearby, otherwise False.
    """
    for i in full_list.values():
        if i[0] - value <= pos[0] <= i[0] + value:
            if i[1] - value <= pos[1] <= i[1] + value:
                return True
    return False


def generate_node_positions(matrix: np.array) -> dict:
    """
    Generate a random position for each node and saves it as a dictionary.

    :param matrix: The adjacency matrix for the network.

    :return: A dictionary of node positions.
    """
    positions = {}
    for i in range(0, len(matrix)):
        # generates a random x,y position for a node
        rand_pos = [
            random.randint(0, len(matrix) * 4),
            random.randint(0, len(matrix) * 4),
        ]
        fails = 0
        value = 5
        while check_if_nearby(rand_pos, positions, value):
            # if that position has already been used then generate a new point
            rand_pos = [
                random.randint(0, len(matrix) * 4),
                random.randint(0, len(matrix) * 4),
            ]
            fails += 1
            if fails % 10 == 0:
                value -= 1
                if value == -1:
                    value = 0
        positions[str(i)] = rand_pos
    return positions


def get_network_from_matrix_and_positions(
    matrix: np.ndarray,
    positions: Dict[str, List[int]],
) -> Network:
    """
    Get nodes and edges from a numpy matrix and a dictionary of positions.

    :param matrix: A 2D numpy array adjacency matrix.
    :param positions: The node positions on a graph.
    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    network = Network()
    edges = []
    # Create all Nodes
    nodes: Dict[Any, Node] = {i: Node(name=str(i)) for i in range(len(matrix))}
    for y_i, y_node in enumerate(matrix):
        # Retrieve the Node and add to the Network
        network.add_node(nodes[y_i])  # Retrieve the positions and set on the Node
        if str(y_i) in positions.keys():
            x, y = positions[str(y_i)]
            nodes[y_i].x_pos = x
            nodes[y_i].y_pos = y  # If the edge hasn't already been added, add it
        for x_i, x_node in enumerate(y_node):
            if x_node == 1:
                edge = tuple(sorted([y_i, x_i]))
                if edge not in edges:
                    network.add_edge(nodes[edge[0]], nodes[edge[1]])
    return network


def get_18_node_network_mesh() -> Network:
    """
    The standard 18 node network found in the Ridley 2017 research paper.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    matrix = np.asarray(
        [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
    )
    positions = {
        "0": [1, 7],
        "1": [2, 7],
        "2": [3, 7],
        "3": [4, 7],
        "4": [5, 7],
        "5": [3, 6],
        "6": [1, 4],
        "7": [3, 4],
        "8": [4, 4],
        "9": [6, 5],
        "10": [6, 4],
        "11": [6, 3],
        "12": [3, 2],
        "13": [1, 1],
        "14": [2, 1],
        "15": [3, 1],
        "16": [4, 1],
        "17": [5, 1],
    }
    return get_network_from_matrix_and_positions(matrix, positions)


def dcbo_base_network() -> Network:
    """
    Creates the same network used to generated DCBO data.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.

    .. node::
        This function replaces the network that was defined in
        `yawning_titan/integrations/dcbo/base_net.txt`.

    .. versionadded:: 1.0.1

    """
    matrix = np.asarray(
        [
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
        ]
    )
    positions = {
        "0": [3, 8],
        "1": [2, 9],
        "2": [9, 2],
        "3": [7, 4],
        "4": [0, 3],
        "5": [10, 6],
        "6": [6.0, 1],
        "7": [9, 4],
        "8": [7, 2],
        "9": [3, 6],
    }
    return get_network_from_matrix_and_positions(matrix, positions)


def create_mesh(size: int = 100, connectivity: float = 0.7) -> Network:
    """
    Create a mesh node environment.

    :param size: The number of nodes in the environment.
    :param connectivity: How connected each of the nodes should be (percentage
        chance for any node to be connected to
        any other).

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    matrix = np.zeros((size, size))
    for i in range(0, size):
        for j in range(i + 1, size):
            if random.randint(0, 99) < connectivity * 100:
                matrix[i][j] = 1
                matrix[j][i] = 1

    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)


def create_star(
    first_layer_size: int = 8, group_size: int = 5, group_connectivity: float = 0.5
) -> Network:
    """
    Create a star node environment.

    This is one node in the middle with groups of nodes around it. There is
    only one connection between a group and the center node. Groups cannot
    connect to each other.

    :param first_layer_size: The number of collections of nodes in first "outer
        ring".
    :param group_size: How many nodes are in each collection.
    :param group_connectivity: How connected the nodes in the connections are.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    number_of_nodes = 1 + first_layer_size * group_size

    matrix = np.zeros((number_of_nodes, number_of_nodes))

    # creates the groups and connects them
    for i in range(first_layer_size):
        for j in range(0, group_size):
            for k in range(j + 1, group_size):
                if random.randint(0, 99) < group_connectivity * 100:
                    matrix[j + 1 + i * group_size][k + 1 + i * group_size] = 1
                    matrix[k + 1 + i * group_size][j + 1 + i * group_size] = 1
    # connects the groups to the center node
    for i in range(0, first_layer_size):
        connector = random.randint(0, group_size - 1)
        matrix[0][1 + i * group_size + connector] = 1
        matrix[1 + i * group_size + connector][0] = 1

    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)


def create_p2p(
    group_size: int = 5,
    inter_group_connectivity: float = 0.1,
    group_connectivity: int = 1,
) -> Network:
    """
    Create a two group network.

    You can modify the connectivity between the two groups and the connectivity
    within the groups.

    :param group_size: The amount of nodes in each group (before random
        variance).
    :param inter_group_connectivity: The connectivity between the two groups.
    :param group_connectivity: The connectivity within the group.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    # creates the sizes of the groups
    group1_size = (
        group_size + random.randint(0, int(group_size / 2)) - int(group_size / 4)
    )
    group2_size = (
        group_size + random.randint(0, int(group_size / 2)) - int(group_size / 4)
    )
    total_size = group1_size + group2_size

    matrix = np.zeros((total_size, total_size))

    # connections between group 1
    for i in range(0, group1_size):
        for j in range(i + 1, group1_size):
            if random.randint(0, 99) < group_connectivity * 100:
                matrix[i][j] = 1
                matrix[j][i] = 1

    # connections between group 2
    for i in range(group1_size, total_size):
        for j in range(i + 1, total_size):
            if random.randint(0, 99) < group_connectivity * 100:
                matrix[i][j] = 1
                matrix[j][i] = 1

    connections = math.ceil(inter_group_connectivity * total_size)
    # connections between the two groups
    for i in range(0, connections):
        g1 = random.randint(0, group1_size - 1)
        g2 = random.randint(group1_size, total_size - 1)

        matrix[g1][g2] = 1
        matrix[g2][g1] = 1

    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)


def create_ring(break_probability: float = 0.3, ring_size: int = 60) -> Network:
    """
    Create a ring network.

    :param break_probability: The probability that two nodes will not be
    connected.

    :param ring_size: The number of nodes in the network.
    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    matrix = np.zeros((ring_size, ring_size))

    # runs through the nodes connecting each one to the next
    for i in range(0, ring_size - 1):
        if random.randint(1, 99) > break_probability * 100:
            matrix[i][i + 1] = 1
            matrix[i + 1][i] = 1
    if random.randint(1, 99) > break_probability * 100:
        matrix[ring_size - 1][0] = 1
        matrix[0][ring_size - 1] = 1

    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)


def custom_network() -> Union[Network, None]:
    """
    Create custom network through user interaction.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    # nodes start at 0
    size = input("How many nodes in the network? ")
    try:
        size = int(size)
    except ValueError:
        print(f"Error in input - '{size}' is not an int")
        return None

    matrix = np.zeros((size, size))
    for i in range(0, size):
        connected_nodes = input(
            "Node: " + str(i) + " is connected to: (separate with comma)"
        )
        try:
            connected_nodes_list = map(int, connected_nodes.split(","))
        except TypeError:
            print("error in node input")
            return None
        for j in connected_nodes_list:
            matrix[i][j] = 1
            matrix[j][i] = 1

    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)


def gnp_random_connected_graph(
    n_nodes: int, probability_of_edge: float
) -> Union[Network, None]:
    """
    Create a randomly connected graph.

    With the guarantee that each node will have at least one connection.

    This is taken from the following stack overflow Q&A with a bit of a
    refactor for clarity.

    :param n_nodes: the number of nodes in the graph.
    :param probability_of_edge: the probability for a node to have an edge.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    edges = combinations(range(n_nodes), 2)
    graph = nx.Graph()
    graph.add_nodes_from(range(n_nodes))
    if probability_of_edge <= 0:
        return None
    if probability_of_edge >= 1:
        return nx.complete_graph(n_nodes, create_using=graph)

    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        graph.add_edge(*random_edge)
        for edge in node_edges:
            if random.random() < probability_of_edge:
                graph.add_edge(*edge)

    matrix = nx.to_numpy_array(graph)
    positions = generate_node_positions(matrix)

    return get_network_from_matrix_and_positions(matrix, positions)
