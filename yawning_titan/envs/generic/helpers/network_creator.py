import math
import random
from itertools import combinations, groupby
from typing import List, Tuple, Union

import networkx as nx
import numpy as np


def check_if_nearby(pos: List[float], full_list: dict, value: int) -> bool:
    """Check if a randomly generated point is close to the points already generated."""
    for i in full_list.values():
        if i[0] - value <= pos[0] <= i[0] + value:
            if i[1] - value <= pos[1] <= i[1] + value:
                return True
    return False


def generate_node_positions(adj_matrix: np.array) -> dict:
    """
    Generate a random position for each node and saves it as a dictionary.

    Args:
        adj_matrix: The adjacency matrix for the network

    Returns:
        A dictionary of node positions
    """
    positions = {}
    for i in range(0, len(adj_matrix)):
        # generates a random x,y position for a node
        rand_pos = [
            random.randint(0, len(adj_matrix) * 4),
            random.randint(0, len(adj_matrix) * 4),
        ]
        fails = 0
        value = 5
        while check_if_nearby(rand_pos, positions, value):
            # if that position has already been used then generate a new point
            rand_pos = [
                random.randint(0, len(adj_matrix) * 4),
                random.randint(0, len(adj_matrix) * 4),
            ]
            fails += 1
            if fails % 10 == 0:
                value -= 1
                if value == -1:
                    value = 0
        positions[str(i)] = rand_pos

    return positions


def save_network(network_name: str, adj_matrix: np.array, positions: dict):
    """
    Save a network in a text file so that it can be used multiple times.

    Args:
        network_name: The name of the network
        adj_matrix: The adjacency matrix for the network
        positions: A dictionary of node positions

    """
    # generates a save string
    string_encoded_network = ""
    size = len(adj_matrix)
    string_encoded_network += str(size) + ","
    for i in adj_matrix:
        for j in i:
            string_encoded_network += str(j) + ","

    string_encoded_network = string_encoded_network[:-1]
    string_encoded_network += "/"

    for node, pos in positions.items():
        [x, y] = pos
        string_encoded_network += str(node) + ":" + str(x) + "," + str(y) + "/"

    string_encoded_network = string_encoded_network[:-1]

    # saves the save string to a text file
    with open(network_name, "w") as file:
        file.write(string_encoded_network)


def load_network(network_name: str) -> Tuple[np.array, dict]:
    """
    Load a saved network so that it can be used by the generic network environment.

    Args:
        network_name: The name of the network

    Returns:
        The adjacency matrix
        A position dictionary for all the nodes
    """
    # loads the file where the data is saved
    with open(network_name, "r") as file:
        lines = file.read()
    split_lines = lines.split("/")
    adj_matrix = split_lines[0]
    positions = split_lines[1:]

    # extracts the adj matrix from the saved string
    adj_matrix = list(map(float, adj_matrix.split(",")))
    adj_matrix = list(map(int, adj_matrix))

    size = adj_matrix[0]

    adj_matrix = np.asarray(adj_matrix[1:]).reshape((size, size))
    # extracts the position dict from the saved string
    positions_dic = {}
    for i in positions:
        positions_dic[str(int(i[: i.index(":")]))] = [
            float(i[i.index(":") + 1 : i.index(",")]),
            float(i[i.index(",") + 1 :]),
        ]

    return adj_matrix, positions_dic


def create_18_node_network() -> Tuple[np.array, dict]:
    """
    Create the standard 18 node network found in the Ridley 2017 research paper.

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
    """
    adj_matrix = np.asarray(
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
    return adj_matrix, positions


def dcbo_base_network() -> Tuple[np.array, dict]:
    """
    Creates the same network used to generated DCBO data.

    :returns: The adjacency matrix that represents the network and a dictionary
        of positions of the nodes.

    .. node::
        This function replaces the network that was defined in
        `yawning_titan/integrations/dcbo/base_net.txt`.

    .. versionadded:: 1.0.1

    """
    matrix = [
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
    positions = {
        "0": [3.0, 8.0],
        "1": [2.0, 9.0],
        "2": [9.0, 2.0],
        "3": [7.0, 4.0],
        "4": [0.0, 3.0],
        "5": [10.0, 6.0],
        "6": [6.0, 1.0],
        "7": [9.0, 4.0],
        "8": [7.0, 2.0],
        "9": [3.0, 6.0],
    }
    return matrix, positions


def create_mesh(size: int = 100, connectivity: float = 0.7) -> Tuple[np.array, dict]:
    """
    Create a mesh node environment.

    Args:
        size: the number of nodes in the environment
        connectivity: how connected each of the nodes should be (percentage chance for any node to be connected to
        any other)

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
    """
    adj_matrix = np.zeros((size, size))
    for i in range(0, size):
        for j in range(i + 1, size):
            if random.randint(0, 99) < connectivity * 100:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions


def create_star(
    first_layer_size: int = 8, group_size: int = 5, group_connectivity: float = 0.5
) -> Tuple[np.array, dict]:
    """
    Create a star node environment.

    This is one node in the middle with groups of nodes around it. There is only one
    connection between a group and the center node. Groups cannot connect to each other.

    Args:
        first_layer_size: the number of collections of nodes in first "outer ring"
        group_size: how many nodes are in each collection
        group_connectivity: how connected the nodes in the connections are

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
    """
    number_of_nodes = 1 + first_layer_size * group_size

    adj_matrix = np.zeros((number_of_nodes, number_of_nodes))

    # creates the groups and connects them
    for i in range(first_layer_size):
        for j in range(0, group_size):
            for k in range(j + 1, group_size):
                if random.randint(0, 99) < group_connectivity * 100:
                    adj_matrix[j + 1 + i * group_size][k + 1 + i * group_size] = 1
                    adj_matrix[k + 1 + i * group_size][j + 1 + i * group_size] = 1
    # connects the groups to the center node
    for i in range(0, first_layer_size):
        connector = random.randint(0, group_size - 1)
        adj_matrix[0][1 + i * group_size + connector] = 1
        adj_matrix[1 + i * group_size + connector][0] = 1

    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions


def create_p2p(
    group_size: int = 5,
    inter_group_connectivity: float = 0.1,
    group_connectivity: int = 1,
) -> Tuple[np.array, dict]:
    """
    Create a two group network.

    You can modify the connectivity between the two groups and the connectivity within the groups.

    Args:
        group_size: the amount of nodes in each group (before random variance)
        inter_group_connectivity: the connectivity between the two groups
        group_connectivity: the connectivity within the group

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
    """
    # creates the sizes of the groups
    group1_size = (
        group_size + random.randint(0, int(group_size / 2)) - int(group_size / 4)
    )
    group2_size = (
        group_size + random.randint(0, int(group_size / 2)) - int(group_size / 4)
    )
    total_size = group1_size + group2_size

    adj_matrix = np.zeros((total_size, total_size))

    # connections between group 1
    for i in range(0, group1_size):
        for j in range(i + 1, group1_size):
            if random.randint(0, 99) < group_connectivity * 100:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

    # connections between group 2
    for i in range(group1_size, total_size):
        for j in range(i + 1, total_size):
            if random.randint(0, 99) < group_connectivity * 100:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

    connections = math.ceil(inter_group_connectivity * total_size)
    # connections between the two groups
    for i in range(0, connections):
        g1 = random.randint(0, group1_size - 1)
        g2 = random.randint(group1_size, total_size - 1)

        adj_matrix[g1][g2] = 1
        adj_matrix[g2][g1] = 1

    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions


def create_ring(
    break_probability: float = 0.3, ring_size: int = 60
) -> Tuple[np.array, dict]:
    """
    Create a ring network.

    Args:
        break_probability: the probability that two nodes will not be connected
        ring_size: the number of nodes in the network

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
    """
    adj_matrix = np.zeros((ring_size, ring_size))

    # runs through the nodes connecting each one to the next
    for i in range(0, ring_size - 1):
        if random.randint(1, 99) > break_probability * 100:
            adj_matrix[i][i + 1] = 1
            adj_matrix[i + 1][i] = 1
    if random.randint(1, 99) > break_probability * 100:
        adj_matrix[ring_size - 1][0] = 1
        adj_matrix[0][ring_size - 1] = 1

    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions


def custom_network() -> Union[Tuple[np.array, dict], Tuple[None, None]]:
    """
    Create custom network through user interaction.

    Returns:
        The adjacency matrix that represents the network and A dictionary of
        positions of the nodes. If the size input is not a valid int,
        `None`, `None` is returned.
    """
    # nodes start at 0
    size = input("How many nodes in the network? ")
    try:
        size = int(size)
    except ValueError:
        print(f"Error in input - '{size}' is not an int")
        return None, None

    adj_matrix = np.zeros((size, size))
    for i in range(0, size):
        connected_nodes = input(
            "Node: " + str(i) + " is connected to: (separate with comma)"
        )
        try:
            connected_nodes_list = map(int, connected_nodes.split(","))
        except TypeError:
            print("error in node input")
            return None, None
        for j in connected_nodes_list:
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1

    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions


def gnp_random_connected_graph(
    n_nodes: int, probability_of_edge: float
) -> Union[Tuple[np.array, dict], None]:
    """
    Create a randomly connected graph but with the guarntee that each node will have at least one connection.

    This is taken from the following stack overflow Q&A with a bit of a refactor
    for clarity

    Args:
        n_nodes: the number of nodes in the graph
        probability_of_edge: the probability for a node to have an edge

    Returns:
        The adjacency matrix that represents the network
        A dictionary of positions of the nodes
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

    adj_matrix = nx.to_numpy_array(graph)
    positions = generate_node_positions(adj_matrix)

    return adj_matrix, positions
