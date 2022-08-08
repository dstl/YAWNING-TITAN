import random
from typing import List, Tuple

import networkx as nx
import numpy as np

from yawning_titan.envs.specific.core.nsa_node import Node


class NodeCollection:
    """Class representing a collection of nodes for the 18-node Ridley Environment."""

    def __init__(self, network: Tuple[np.array, dict], chance_to_spread_during_patch):

        self.adj_matrix = network[0]
        self.pos_dic = network[1]
        self.nodes = []
        for i in range(0, len(self.adj_matrix)):
            self.nodes.append(Node())
        self.chance_to_spread_during_patch = chance_to_spread_during_patch

    def get_number_of_nodes(self) -> int:
        """
        Return the number of nodes in the network.

        Returns:
            The number of nodes in the network (int)
        """
        return len(self.nodes)

    def get_observation(self) -> np.array:
        """
        Get the states of all the nodes in the network.

        Returns:
            observation: The current state of the environment (numpy array)
        """
        observation = np.zeros(
            (len(self.nodes), (len(self.nodes) + 2)), dtype=np.float32
        )

        for i in range(0, len(self.nodes)):
            data = self.nodes[i].get_condition()
            observation[i][0] = data[0]
            observation[i][1] = data[1]

            for j in range(0, len(self.nodes)):
                if self.nodes[i].get_condition()[0]:
                    observation[i][j + 2] = 0
                else:
                    observation[i][j + 2] = self.adj_matrix[i][j]
        return observation

    def modify_node(self, number: int, changes: Tuple[bool, int]):
        """
        Change the state of a single node.

        Args:
            number: the number of the node to change
            changes: a list with two variables in [isolate, compromise]
                isolate: A boolean that will if true change the isolation status of the node (true -> false,
                         false -> true) (boolean)
                compromise: a mode signal that will change the state of a node. 0 does nothing, 1 makes it safe and
                            2 compromises the node (int)

        """
        [isolate, compromise] = changes
        if isolate:
            self.nodes[number].change_isolated()
        self.nodes[number].change_compromised(compromise)

    def get_compromised_nodes(self) -> List[int]:
        """
        Create a list of all the nodes in the network that are compromised.

        Returns:
            compromised_nodes: A list of nodes that are compromised (list of ints)
        """
        compromised_nodes = []
        for i in range(0, len(self.nodes)):
            if self.nodes[i].get_condition()[1]:
                # check if compromised
                compromised_nodes.append(i)
        return compromised_nodes

    def get_un_compromised_nodes(self) -> List[int]:
        """
        Create a list of all the safe nodes in the network.

        Returns:
            un_compromised_nodes: A list of nodes that are safe (list of ints)
        """
        un_compromised_nodes = []
        for i in range(0, len(self.nodes)):
            if not self.nodes[i].get_condition()[1]:
                un_compromised_nodes.append(i)
        return un_compromised_nodes

    def get_isolated_nodes(self) -> List[int]:
        """
        Create a list of all the isolated nodes in the network.

        Returns:
            isolated_nodes: A list of nodes that are isolated (list of ints)
        """
        isolated_nodes = []
        for i in range(0, len(self.nodes)):
            if self.nodes[i].get_condition()[0]:
                isolated_nodes.append(i)
        return isolated_nodes

    def get_number_of_isolated(self) -> int:
        """
        Get the number of isolated nodes in the network.

        Returns:
            the number of isolated nodes in the network (int)
        """
        return len(self.get_isolated_nodes())

    def get_number_of_un_compromised(self) -> int:
        """
        Get the number of safe nodes in the network.

        Returns:
            the number of safe nodes in the network (int)
        """
        return len(self.get_un_compromised_nodes())

    def get_connected_nodes(self, number: int) -> List[int]:
        """
        When given a node returns a list of all of the nodes connected to that node.

        Args:
            number: the number of the node to run on

        Returns:
            a list of all the nodes connected to a specified node (list of ints)
        """
        if self.nodes[number].get_condition()[0]:
            return []
        else:
            # checks the connected nodes though the adj matrix and checks if the nodes are not isolated
            return [
                i
                for i in range(0, len(self.nodes))
                if self.adj_matrix[number][i] == 1
                and self.nodes[i].get_condition()[0] is False
            ]

    def spread(self, number: int):
        """
        Spread the red agent through all connected nodes.

        Args:
            number: the number of the node to spread from

        """
        if (
            self.nodes[number].get_condition()[0]
            or self.nodes[number].get_condition()[1] is False
        ):
            # If the nodes is isolated or not infected
            pass
        else:
            # get all the connected nodes
            connected_nodes = self.get_connected_nodes(number)

            for i in connected_nodes:
                n = random.randint(1, 100)
                # attempt to spread
                if n < self.chance_to_spread_during_patch * 100:
                    self.nodes[i].change_compromised(2)

    def calculate_reward(self) -> float:
        """
        Calculate a reward for the current networks state.

        Returns:
            reward: the reward for being in the current state
        """
        reward = 0
        for i in self.nodes:
            # gets the conditions of all the nodes
            node_state = i.get_condition()
            if node_state[1] is False:
                # reward for safe
                reward = reward + 0.2
            elif node_state[1] is True and node_state[0]:
                # reward for unsafe but isolated
                reward = reward + 0.01

        return reward

    def get_netx_graph(self) -> nx.Graph:
        """
        Get the underlying networkx graph.

        Returns:
            A networkx graph object
        """
        nodes = [str(i) for i in range(self.get_number_of_nodes())]
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        for i in range(len(self.adj_matrix)):
            for j in range(len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] == 1:
                    graph.add_edge(str(i), str(j))

        return graph

    def get_netx_pos(self) -> dict:
        """Get graph positions."""
        return self.pos_dic
