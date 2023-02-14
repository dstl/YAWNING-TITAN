from __future__ import annotations

import copy
import itertools
import json
import math
import random
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List, Tuple, Union

import networkx as nx
import numpy as np

from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.networks.network import Network
from yawning_titan.networks.node import Node

_LOGGER = getLogger(__name__)


class NetworkInterface:
    """The primary interface between both red and blue agents and the underlying environment."""

    def __init__(self, game_mode: GameMode, network: Network):
        """
        Initialise the Network Interface and initialises all the necessary components.

        :param game_mode: the :class:`~yawning_titan.game_modes.game_mode.GameMode` that defines the abilities of the agents.
        :param network: the :class:`~yawning_titan.networks.network.Network` that defines the network within which the agents act.
        """
        # opens the fle the user has specified to be the location of the game_mode

        self.game_mode: GameMode = game_mode
        self.current_graph: Network = network

        self.random_seed = self.game_mode.miscellaneous.random_seed.value

        # initialise the base graph
        self.base_graph = copy.deepcopy(self.current_graph)
        self.initial_base_graph = copy.deepcopy(self.current_graph)

        # initialises the deceptive nodes and their names and amount
        self.initialise_deceptive_nodes()

        # a pointer to to point to the current deceptive node (when a new node is added but the max is reached the
        # oldest node is replaced)
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False

        # a edge dictionary to give each edge a unique single number
        self.initialise_edge_map()

        self.red_current_location: Node = None

        # a list of all of the failed attacks that occurred on this turn
        self.true_attacks = []
        # a list of all the failed attacks that blue has been able to detect
        self.detected_attacks = []

        edges_per_node = len(self.current_graph.edges) / (
            2 * len(self.current_graph.nodes)
        )

        self.connectivity = -math.exp(-0.1 * edges_per_node) + 1

        self.adj_matrix = nx.to_numpy_array(self.current_graph)

    """
    GETTERS
    The following block of code contains the getters for the network interface. Getters are methods that (given
    parameters) will return some attribute from the class
    """

    def get_shortest_distances_to_target(self, nodes: List[Node]) -> List[float]:
        """Get a list of the shortest distances from each node to the target."""
        # TODO: add option where only shortest distance provided

        dist_matrix = dict(
            nx.single_source_shortest_path_length(
                self.current_graph, self.get_target_node()
            )
        )
        distances = [dist_matrix[n] for n in nodes]
        return distances

    def get_target_node(self) -> Node:
        """
        Get the node which is being targeted in the config.

        Returns:
            The target node if it exists
        """
        return self.current_graph.get_node_from_name(
            self.game_mode.red.target_mechanism.target_specific_node.target.value
        )

    def get_total_num_nodes(self) -> int:
        """
        Get the total number of nodes including any yet to be placed deceptive nodes.

        Returns:
            The number of nodes that there are including deceptive nodes that may not have been placed yet
        """
        return (
            self.current_graph.number_of_nodes()
            + self.get_number_unused_deceptive_nodes()
        )

    def get_midpoint(self, node1: Node, node2: Node) -> Tuple[float, float]:
        """
        Get the midpoint between the position of two nodes.

        Args:
            node1: the name of the first node to get the midpoint from
            node2: the name of the second node to get the midpoint from

        Returns:
            The x and y coordinates of the midpoint between two nodes
        """
        # calculate midpoint
        x = (float(node1.x_pos) + float(node2.x_pos)) / 2
        y = (float(node1.y_pos) + float(node2.y_pos)) / 2

        return x, y

    def get_current_connected_nodes(self, node: Node) -> List[Node]:
        """
        Get all of the nodes currently connected to a target node.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return [
            self.current_graph.get_node_from_uuid(n.uuid)
            for n in self.current_graph.neighbors(node)
        ]

    def get_base_connected_nodes(self, node: Node) -> List[Node]:
        """
        Get all of the nodes connected to the given node in the base graph.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return [
            self.base_graph.get_node_from_uuid(n.uuid)
            for n in self.base_graph.neighbors(node)
        ]

    def get_current_graph_as_dict(self) -> Dict:
        """
        Get the current networkx graph for the environment and convert it to a dict of dicts.

        Returns:
            The networkx graph as a dict  of dicts
        """
        return nx.to_dict_of_dicts(self.current_graph)

    def get_attributes_from_key(self, key: str, key_by_uuid: bool = True) -> dict:
        """
        Take in a key and return a dictionary.

        The keys are the names of the nodes and the values are the attribute values that are stored for
        that node under the specified key

        :param key: The name of the attribute to extract
        :param key_by_uuid: Use the nodes uuid attribute as the key if True otherwise use the node object itself.

        Returns:
            A dictionary of attributes
        """
        if key_by_uuid:
            return {n.uuid: getattr(n, key) for n in self.current_graph.get_nodes()}
        return {n: getattr(n, key) for n in self.current_graph.get_nodes()}

    def get_all_vulnerabilities(self) -> dict:
        """Get a dictionary of vulnerability scores."""
        return self.get_attributes_from_key("vulnerability_score")

    def get_all_isolation(self) -> dict:
        """Get a dictionary of the isolation status of all the nodes."""
        return self.get_attributes_from_key("isolated")

    def get_all_node_compromised_states(self) -> dict:
        """Get a dictionary of compromised states."""
        return self.get_attributes_from_key("true_compromised_status")

    def get_all_node_blue_view_compromised_states(self) -> dict:
        """Get a dictionary of compromised states."""
        return self.get_attributes_from_key("blue_view_compromised_status")

    def get_all_node_positions(self) -> dict:
        """Get a dictionary of node positions."""
        return self.get_attributes_from_key("node_position", key_by_uuid=False)

    def get_number_unused_deceptive_nodes(self):
        """Get the current number of unused deceptive nodes."""
        return (
            self.game_mode.blue.action_set.deceptive_nodes.max_number.value
            - self.current_deceptive_nodes
        )

    def get_current_observation(self) -> np.array:
        """
        Get the current observation of the environment.

        The composition of the observation space is based on the configuration file used for the scenario.

        Returns:
            numpy array containing the above details
        """
        # number of spaces open for deceptive nodes
        open_spaces = self.get_number_unused_deceptive_nodes()

        # Builds the observation space using multiple different metrics from the env

        # Gets the adj matrix for the current graph
        node_connections = []

        # Gets the isolation states for each node
        isolated_state = []
        if self.game_mode.blue_can_observe.node_connections.value:
            node_connections = self.adj_matrix
            # pads the array to account for any missing deceptive nodes that may not have been placed yet
            node_connections = np.pad(node_connections, (0, open_spaces), "constant")

            # array used to keep track of which nodes are being isolated
            isolated_state = np.asarray(
                list(self.get_attributes_from_key("isolated").values())
            ).astype(int)

            # pad array to account for deceptive nodes
            isolated_state = np.pad(isolated_state, (0, open_spaces), "constant")

        # Gets the current safe/compromised status of all of the nodes
        compromised_state = []
        if self.game_mode.blue_can_observe.compromised_status.value:
            compromised_state = np.asarray(
                list(
                    self.get_attributes_from_key(
                        "blue_view_compromised_status"
                    ).values()
                )
            )
            compromised_state = np.pad(compromised_state, (0, open_spaces), "constant")
        # Gets the vulnerability score of all of the nodes
        vulnerabilities = []
        if self.game_mode.blue_can_observe.vulnerabilities.value:
            vulnerabilities = np.asarray(
                list(self.get_attributes_from_key("vulnerability_score").values())
            )
            vulnerabilities = np.pad(vulnerabilities, (0, open_spaces), "constant")

        # Gets the average vulnerability of all the nodes
        avg_vuln = []
        if self.game_mode.blue_can_observe.average_vulnerability.value:
            all_vuln = self.get_attributes_from_key("vulnerability_score").values()
            avg_vuln = [sum(all_vuln) / len(all_vuln)]

        # Gets the connectivity of the graph, closer to 1 means more edges per node
        connectivity = []
        if self.game_mode.blue_can_observe.graph_connectivity.value:
            connectivity = [self.connectivity]

        # Gets the attacks that the blue agent detected
        attacking_nodes = []
        attacked_nodes = []
        if (
            self.game_mode.blue_can_observe.attacking_nodes.value
            or self.game_mode.blue_can_observe.attacked_nodes.value
        ):
            attacking = {n: 0 for n in self.current_graph.get_nodes()}
            attacked = {n: 0 for n in self.current_graph.get_nodes()}
            for node_set in self.detected_attacks:
                if node_set[0] is not None:
                    # extract the attacking node (as long as the attacking node is not None)
                    attacking[node_set[0]] = 1
                # extract the node that was attacked
                attacked[node_set[1]] = 1
            if self.game_mode.blue_can_observe.attacking_nodes.value:
                # attacking nodes
                attacking_nodes = list(attacking.values())
                attacking_nodes = np.pad(attacking_nodes, (0, open_spaces), "constant")
            if self.game_mode.blue_can_observe.attacked_nodes.value:
                # nodes attacked
                attacked_nodes = list(attacked.values())
                attacked_nodes = np.pad(attacked_nodes, (0, open_spaces), "constant")

        # Gets the locations of any special nodes in the network (entry nodes and high value nodes)
        entry_nodes = []
        nodes = []
        target_nodes = []

        if self.game_mode.blue_can_observe.special_nodes.value:
            # gets the entry nodes
            entry_nodes = {n: 0 for n in self.current_graph.get_nodes()}
            for n in self.current_graph.entry_nodes:
                entry_nodes[n] = 1
            entry_nodes = list(entry_nodes.values())
            entry_nodes = np.pad(entry_nodes, (0, open_spaces), "constant")

            if self.game_mode.game_rules.blue_loss_condition.target_node_lost.value:
                # gets the target node
                target_nodes = {n: 0 for n in self.current_graph.get_nodes()}
                target_nodes[self.get_target_node()] = 1
                target_nodes = list(target_nodes.values())
                target_nodes = np.pad(target_nodes, (0, open_spaces), "constant")

            if self.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value:
                # gets the high value node nodes
                nodes = {n: 0 for n in self.current_graph.get_nodes()}

                # set high value nodes to 1
                for node in self.current_graph.high_value_nodes:
                    nodes[node] = 1

                nodes = list(nodes.values())
                nodes = np.pad(nodes, (0, open_spaces), "constant")

        # gets the skill of the red agent
        skill = []
        if self.game_mode.blue_can_observe.red_agent_skill.value:
            skill = [self.game_mode.red.agent_attack.skill.value.value]

        # combines all of the env observations together to create the observation that the blue agent gets
        obs = np.concatenate(
            (
                node_connections,
                isolated_state,
                compromised_state,
                vulnerabilities,
                avg_vuln,
                connectivity,
                attacking_nodes,
                attacked_nodes,
                entry_nodes,
                nodes,
                target_nodes,
                skill,
            ),
            axis=None,
            dtype=np.float32,
        )
        return obs

    def get_observation_size_base(self, with_feather: bool) -> int:
        """
        Get the size of the observation space.

        This is based on the game_mode that are turned on/off.

        Returns:
            The size of the observation space
        """
        # gets the max number of nodes in the env (including deceptive nodes)
        observation_size = 0
        max_number_of_nodes = self.get_total_num_nodes()
        if with_feather:
            node_connections = 500
        else:
            node_connections = max_number_of_nodes * max_number_of_nodes

        # calculate the size of the observation space
        # the size depends on what observations are turned on/off in the config file
        if self.game_mode.blue_can_observe.node_connections.value:
            observation_size += node_connections
        if self.game_mode.blue_can_observe.compromised_status.value:
            observation_size += max_number_of_nodes
        if self.game_mode.blue_can_observe.vulnerabilities.value:
            observation_size += max_number_of_nodes
        if self.game_mode.blue_can_observe.average_vulnerability.value:
            observation_size += 1
        if self.game_mode.blue_can_observe.graph_connectivity.value:
            observation_size += 1
        if self.game_mode.blue_can_observe.attacking_nodes.value:
            observation_size += max_number_of_nodes
        if self.game_mode.blue_can_observe.attacked_nodes.value:
            observation_size += max_number_of_nodes
        if self.game_mode.blue_can_observe.special_nodes.value:
            observation_size += max_number_of_nodes
            if self.game_mode.game_rules.blue_loss_condition.target_node_lost.value:
                observation_size += max_number_of_nodes
            if self.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value:
                observation_size += max_number_of_nodes

        if self.game_mode.blue_can_observe.red_agent_skill.value:
            observation_size += 1
        return observation_size

    def get_observation_size(self) -> int:
        """Use base observation size calculator with feather switched off."""
        return self.get_observation_size_base(False)

    """
    SETTERS
    The following block of code contains the setters for the network_interface. Setters are a type of method that update
    or change a class attribute
    """

    def initialise_deceptive_nodes(self):
        """Create a separate list of :class: `~yawning_titan.networks.node.Node` objects take represent deceptive nodes."""
        self.available_deceptive_nodes: List[Node] = []
        for i in range(self.game_mode.blue.action_set.deceptive_nodes.max_number.value):
            name = "d" + str(i)
            deceptive_node = Node(
                name=name,
                vulnerability=self.current_graph._generate_random_vulnerability(),
            )
            deceptive_node.deceptive_node = True
            self.available_deceptive_nodes.append(deceptive_node)

    def initialise_edge_map(self):
        """Create a lookup that maps a unique integer key to an networkx edge (node pair)."""
        self.edge_map = {}
        edges: List[Tuple[Node, Node]] = self.current_graph.edges
        for i, node_pair in enumerate(edges):
            self.edge_map[i] = node_pair

    def update_stored_attacks(
        self, attacking_nodes: List[Node], target_nodes: List[Node], success: List[bool]
    ):
        """
        Update this turns current attacks.

        This function collects all of the failed attacks and stores them for the
        blue agent to use in their action decision

        Args:
            attacking_nodes: Nodes red has attacked from
            target_nodes: Nodes red is attacking
            success: If the attacks were a success or not
        """
        # Runs through all the nodes attacked
        for attacking_node, target_node, success in zip(
            attacking_nodes, target_nodes, success
        ):
            # Deceptive nodes have a different chance of detecting attacks
            if target_node.deceptive_node:
                if success:
                    # chance of seeing the attack if the attack succeeded
                    if (
                        100
                        * self.game_mode.blue.attack_discovery.succeeded_attacks_known_compromise.chance.deceptive_node.value
                        > random.randint(0, 99)
                    ):
                        self.detected_attacks.append([attacking_node, target_node])
                else:
                    # chance of seeing the attack if the attack fails
                    if (
                        100
                        * self.game_mode.blue.attack_discovery.failed_attacks.chance.deceptive_node.value
                        > random.randint(0, 99)
                    ):
                        self.detected_attacks.append([attacking_node, target_node])
            else:
                # If the attack did not succeed
                if success is False:
                    if self.game_mode.blue.attack_discovery.failed_attacks.use.value:
                        if (
                            100
                            * self.game_mode.blue.attack_discovery.failed_attacks.chance.standard_node.value
                            > random.randint(0, 99)
                        ):
                            # Adds the attack to the list of current attacks for this turn
                            self.detected_attacks.append([attacking_node, target_node])
                else:
                    # If the attack succeeded and the blue agent detected it
                    if target_node.blue_view_compromised_status == 1:
                        if (
                            self.game_mode.blue.attack_discovery.succeeded_attacks_known_compromise.use.value
                        ):
                            if (
                                self.game_mode.blue.attack_discovery.succeeded_attacks_known_compromise.chance.standard_node.value
                                > random.randint(0, 99)
                            ):
                                self.detected_attacks.append(
                                    [attacking_node, target_node]
                                )
                    else:
                        # If the attack succeeded but blue did not detect it
                        if (
                            self.game_mode.blue.attack_discovery.succeeded_attacks_unknown_compromise.use.value
                        ):
                            if (
                                100
                                * self.game_mode.blue.attack_discovery.succeeded_attacks_unknown_compromise.chance.standard_node.value
                                > random.randint(0, 99)
                            ):
                                self.detected_attacks.append(
                                    [attacking_node, target_node]
                                )
            # Also compiles a list of all the attacks even those that blue did not "see"
            self.true_attacks.append([attacking_node, target_node])

    """
    RESET METHODS
    The following block of code contains the methods that are used to reset some portion of the network interface
    """

    def reset_stored_attacks(self):
        """
        Reset the attacks list.

        This needs to be called every timestep to ensure that only the current attacks are contained.
        """
        self.true_attacks = []
        self.detected_attacks: List[List[Node]] = []

    def reset(self):
        """Reset the network back to its default state."""
        # red location
        self.red_current_location = None

        # resets the network graph from the saved base graph
        self.current_graph = copy.deepcopy(self.initial_base_graph)
        self.base_graph = copy.deepcopy(self.initial_base_graph)

        # resets the edge map to match the new current graph
        self.initialise_edge_map()
        self.initialise_deceptive_nodes()

        # pointers and helpers for deceptive nodes are reset
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False

        # any previous attacks are removed
        self.reset_stored_attacks()

        # updates the stored adj matrix
        self.adj_matrix = nx.to_numpy_array(self.current_graph)

        if self.game_mode.on_reset.choose_new_entry_nodes.value:
            self.current_graph.reset_random_entry_nodes()

        # set high value nodes
        if self.game_mode.on_reset.choose_new_high_value_nodes.value:
            self.current_graph.reset_random_high_value_nodes()

        if self.game_mode.on_reset.randomise_vulnerabilities.value:
            self.current_graph.reset_random_vulnerabilities()

    """
    STANDARD METHODS
    The following block of code contains the standard methods that are used to interact with the network interface in
    in some complex way.
    """

    def __push_red(self):
        """
        Remove red from the target node and move to a new location.

        If the blue agent patches the node that the red agent is in the red agent will be pushed to a connected
        compromised node. If there are none then the red agent will be pushed out of the network
        """
        connected = self.get_current_connected_nodes(self.red_current_location)
        # Randomises the order of the nodes to pick a random one
        random.shuffle(connected)
        done = False
        for node in connected:
            if node.true_compromised_status == 1:
                self.red_current_location = node
                done = True
                break
        if done is False:
            # If there were no nodes then the agent is removed from the network
            self.red_current_location = None

    def add_deceptive_node(self, node1: Node, node2: Node) -> Union[bool, Node]:
        """
        Add a deceptive node into the network.

        The deceptive node will sit between two actual nodes and act as a normal node in all
        regards other than the fact that it give more information when it is attacked

        Args:
            node1: Name of the first node to connect to the deceptive node
            node2: Name of the second to connect to the deceptive node

        Returns:
            False if failed, the name of the new node if succeeded

        """
        # Check if there exists an edge between the two nodes
        if self.base_graph.has_edge(node1, node2):
            # If the red agent is in the deceptive node at its old position, push it out to a surrounding node
            if (
                self.red_current_location is not None
                and self.red_current_location.deceptive_node
            ):
                self.__push_red()

            # get the new node and add the new node
            deceptive_node = self.available_deceptive_nodes[self.deceptive_node_pointer]

            # If the node is already in use, remove it from the base graph
            if self.base_graph.has_node(deceptive_node):
                self.__remove_node_yt(deceptive_node, self.base_graph)

            # inserts a new node on the base graph
            # self.__insert_node_between(copy.deepcopy(deceptive_node), node1, node2, self.base_graph)
            self.__insert_node_between(deceptive_node, node1, node2, self.base_graph)

            # If the node is already in use, remove it from the current graph
            if self.current_graph.has_node(deceptive_node):
                self.__remove_node_yt(deceptive_node, self.current_graph)

            # check the isolation status of the nodes
            if not node1.isolated and not node2.isolated:
                # neither are isolated: use the insert between method to insert the new node on the current graph
                self.__insert_node_between(
                    deceptive_node, node1, node2, self.current_graph
                )
            elif not node1.isolated:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(deceptive_node)
                self.current_graph.add_edge(node1, deceptive_node)
            elif not node2.isolated:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(deceptive_node)
                self.current_graph.add_edge(node2, deceptive_node)
            else:
                # both nodes are isolated: add the node to the graph
                self.current_graph.add_node(deceptive_node)

            # increase the pointer to point to the next element in the list (the next deceptive node to use)
            self.deceptive_node_pointer += 1
            if not self.reached_max_deceptive_nodes:
                # checks if all the deceptive nodes are in play
                self.current_deceptive_nodes += 1
            if (
                self.deceptive_node_pointer
                == self.game_mode.blue.action_set.deceptive_nodes.max_number.value
            ):
                self.deceptive_node_pointer = 0
            if (
                self.current_deceptive_nodes
                == self.game_mode.blue.action_set.deceptive_nodes.max_number.value
            ):
                self.reached_max_deceptive_nodes = True
            if (
                self.game_mode.blue.action_set.deceptive_nodes.new_node_on_relocate.value
            ):
                # TODO: check if the following can be replaced by a node reset method
                deceptive_node.vulnerability = (
                    self.current_graph._generate_random_vulnerability()
                )
                deceptive_node.true_compromised_status = 0
                deceptive_node.blue_view_compromised_status = 0
                deceptive_node.node_position = [0, 0]
                deceptive_node.deceptive_node = True
                deceptive_node.blue_knows_intrusion = False
                deceptive_node.isolated = False

            # updates the position of the node based on its new location
            deceptive_node.node_position = self.get_midpoint(node1, node2)
            # updates the current adjacency matrix
            self.adj_matrix = nx.to_numpy_array(self.current_graph)
            return deceptive_node
        else:
            # If no edge return false as the deceptive node cannot be put here
            return False

    def __remove_node_yt(self, node: Node, graph: nx.Graph) -> None:
        """
        Remove a node from a graph.

        Removing a node removes all connections to and from that node

        Args:
            node: the name of the node to remove
            graph: the networkx graph to remove the node from
        """
        self.reconnect_node(
            node
        )  # TODO: check this is correct. This is a workaround to reattach connections to the node to delete so as to establish
        # the correct paths to reform.

        # extracts the 0th element from a list where a variable "to_remove" has been removed
        extract_connections = lambda x, to_remove: list(  # noqa
            filter(lambda z: z != to_remove, x)  # noqa
        )[
            0
        ]  # noqa

        # gets all of the edges from a node
        links = graph.edges(node)

        # gets the connections to this node using the extract_connections lambda function
        connections = [extract_connections(x, node) for x in links]
        if len(connections) >= 2:
            # generates the new connections
            new_links = list(itertools.combinations(connections, 2))
            # adds the new edges
            graph.add_edges_from(new_links)
        # removes the old node
        graph.remove_node(node)

    def __insert_node_between(
        self, new_node: Node, node1: Node, node2: Node, graph: Network
    ) -> None:
        """
        Insert a node in between two nodes.

        Args:
            new_node: the name of the new node
            node1: the name of the first node the new node will be connected to
            node2: the name of the second node the new node will be connected to
            graph: the networkx graph to add the new node to

        """
        # removes the old edge between the nodes
        if graph.has_edge(node1, node2):
            graph.remove_edge(node1, node2)
        graph.add_node(new_node)
        # adds the new node in and updates the edges
        graph.add_edge(node1, new_node)
        graph.add_edge(new_node, node2)

    def isolate_node(self, node: Node):
        """
        Isolate a node (disable all of the nodes connections).

        Args:
            node: the node to disable the connections of

        """
        node.isolated = True
        current_connections = self.get_current_connected_nodes(node)
        for cn in current_connections:
            self.current_graph.remove_edge(node, cn)

        self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def reconnect_node(self, node: Node):
        """
        Re-enable any connections that may have previously been disabled.

        Args:
            node: the node to re-enable
        """
        if node.isolated:
            node.isolated = False
            base_connections = self.get_base_connected_nodes(node)
            for bn in base_connections:
                cn = self.current_graph.get_node_from_uuid(bn.uuid)
                if (
                    not cn.isolated
                ):  # ensure a different isolated node cannot be reconnected
                    self.current_graph.add_edge(node, cn)

            self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def attack_node(
        self,
        node: Node,
        skill: float = 0.5,
        use_skill: bool = False,
        use_vulnerability: bool = False,
        guarantee: bool = False,
    ) -> bool:
        """
        Attack a target node.

        Uses a random chance to succeed that is modified by the skill of the attack and the
        vulnerability of the node. Both the skill and the vulnerability can be toggled to either be used or not

        Args:
            node: The name of the node to target
            skill: The skill of the attacker
            use_skill: A boolean value that is used to determine if skill is used in the calculation to check if the
                       attack succeeds
            use_vulnerability: A boolean value that is used to determine if vulnerability is used in the calculation to
                               check if the attack succeeds
            guarantee: If True then attack automatically succeeds

        Returns:
            A boolean value that represents if the attack succeeded or not
        """
        # check if vulnerability and score are being used. If they are not then select a value
        if use_vulnerability:
            defence = 1 - node.vulnerability_score
        else:
            defence = 0
        if not use_skill:
            skill = 1

        # calculate the attack score, the higher the score the more likely the attack is to succeed
        attack_score = ((skill * skill) / (skill + defence)) * 100
        # check if the attack hits based on the attack score
        if guarantee or (attack_score > random.randint(0, 100)):
            node.true_compromised_status = 1
            self.__immediate_attempt_view_update(node)
            return True
        else:
            return False

    def make_node_safe(self, node: Node):
        """
        Make the state for a given node safe.

        Args:
            node: the node to make safe
        """
        node.true_compromised_status = 0
        node.blue_view_compromised_status = 0
        if self.red_current_location == node:
            # If the red agent is in the node that just got made safe then the red agent needs to be pushed back
            self.__push_red()
        node.blue_knows_intrusion = False

    def __immediate_attempt_view_update(self, node: Node, chance: float = None):
        """
        Attempt to update the view of a specific node for the blue agent.

        There is a chance that intrusions will not be detected.

        :param node: the node to try and update the view for
        """
        if node.blue_knows_intrusion is True:
            # if we have seen the intrusion before we don't want to forget about it
            node.blue_view_compromised_status = node.true_compromised_status
        if node.true_compromised_status == 1:
            if chance is None and (
                random.randint(0, 99)
                < self.game_mode.blue.intrusion_discovery_chance.immediate.standard_node.value
                * 100
                or node.deceptive_node
            ):
                node.blue_view_compromised_status = node.true_compromised_status
                # remember this intrusion so we don't forget about it
                node.blue_knows_intrusion = True
            elif chance is not None and (random.randint(0, 99) < chance * 100):
                node.blue_view_compromised_status = node.true_compromised_status

        else:
            node.blue_view_compromised_status = node.true_compromised_status

    def scan_node(self, node: Node) -> None:
        """
        Scan a target node to determine compromise based on the chance of discovery of compromise.

        Args:
            node: The node to be scanned
        """
        if node.blue_knows_intrusion:
            node.blue_view_compromised_status = 1
        elif node.true_compromised_status == 1:
            if (
                random.randint(0, 99)
                < self.game_mode.blue.intrusion_discovery_chance.on_scan.standard_node.value
                * 100
                or node.deceptive_node
            ):
                node.blue_knows_intrusion = True
                node.blue_view_compromised_status = 1

    def save_json(self, data_dict: dict, ts: int) -> None:
        """
        Save a given dictionary to a json file.

        Args:
            data_dict: Data to save to the json file
            ts: The current timestamp of the data
        """
        now = datetime.now()
        time_stamp = str(datetime.timestamp(now)).replace(".", "")
        name = (
            "yawning_titan/envs/helpers/json_timesteps/output_"
            + str(ts)
            + "_"
            + str(time_stamp)
            + ".json"
        )
        with open(name, "w+") as json_file:
            json.dump(data_dict, json_file)

    def create_json_time_step(self) -> dict:
        """
        Create a dictionary that contains the current state of the environment and returns it.

        Returns:
            A dictionary containing the node connections, states and vulnerability scores
        """
        convert_str = lambda x: str(x) if x is not None else None  # noqa

        # Gets the edges from the networkx object
        connections = [
            list(map(convert_str, list(e))) for e in self.current_graph.edges
        ]
        # Gets the vulnerability and compromised status
        node_states = self.get_all_node_compromised_states()
        node_vulnerabilities = self.get_all_vulnerabilities()

        # Combines the features into a defaultdict and then returns a dictionary
        combined_features = defaultdict(list)

        for feature in (node_states, node_vulnerabilities):
            for key, value in feature.items():
                combined_features[key].append(value)

        current_state_dict = {"edges": connections, "features": combined_features}

        return current_state_dict
