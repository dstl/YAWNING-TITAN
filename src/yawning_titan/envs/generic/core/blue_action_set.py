import random
from typing import List, Tuple, Union

from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.networks.node import Node

"""
A collection of methods that a blue agent could use. This includes multiple ways to defend a network by saving nodes or
making them harder to compromise.
"""


class BlueActionSet:
    """A class representing a Blue Agents action set."""

    def __init__(self, network_interface: NetworkInterface):
        """
        Initialise a blue agents action set.

        Args:
            network_interface: Object that allows the class to interact with the network
            settings_file: Dictionary containing configuration data
        """
        self.network_interface = network_interface

    def reduce_node_vulnerability(self, node: Node) -> Tuple[str, Node]:
        """
        Reduce the vulnerability of the target node.

        Will not reduce the vulnerability past the lower bound setting in the
        configuration file:
            - BLUE: node_vulnerability_min

        :param node: The node to reduce the vulnerability of as an instance of ``Node``.

        :returns: The name of the action taken ("reduce_vulnerability") and the ``Node`` the action was taken on.
        """
        # gets the current vulnerability
        current_vulnerability = node.vulnerability_score

        # updates the vulnerability of the node
        new_vulnerability_score = current_vulnerability - 0.2
        if (
            new_vulnerability_score
            < self.network_interface.current_graph.node_vulnerability_lower_bound
        ):
            new_vulnerability_score = (
                self.network_interface.current_graph.node_vulnerability_lower_bound
            )
        node.vulnerability_score = new_vulnerability_score
        return "reduce_vulnerability", node

    def restore_node(self, node: Node) -> Tuple[str, Node]:
        """
        Restore a node to its starting state: safe and with its starting vulnerability.

        Args:
            node: the node to restore

        Returns:
            The name of the action ("restore_node")
            The name of the node the action was taken on
        """
        self.network_interface.make_node_safe(node)
        node.reset_vulnerability()

        return "restore_node", node

    def make_safe_node(self, node: Node) -> Tuple[str, Node]:
        """
        Make a target node safe.

        Can also affect the vulnerability of the node. There are settings that can change how this
        action works in the configuration file:
            - BLUE: making_node_safe_modifies_vulnerability
            - BLUE: vulnerability_change
            - BLUE: making_node_safe_gives_random_vulnerability

        Args:
            The name of the action ("make_safe_node")
            The name of the node to make safe
        """
        self.network_interface.make_node_safe(node)
        upper = self.network_interface.current_graph.node_vulnerability_upper_bound
        lower = self.network_interface.current_graph.node_vulnerability_lower_bound

        # Settings change the effects of making a node safe
        if (
            self.network_interface.game_mode.blue.action_set.make_node_safe.increases_vulnerability.value
        ):
            # Modifies the vulnerability by a set amount (cannot increase it past the limit in the config file)
            change_amount = (
                self.network_interface.game_mode.blue.action_set.make_node_safe.vulnerability_change.value
            )
            new_vulnerability_score = change_amount + node.vulnerability_score
            # checks to make sure that the new value does not go out of the range for vulnerability
            if new_vulnerability_score > upper:
                new_vulnerability_score = upper
            elif new_vulnerability_score < lower:
                new_vulnerability_score = lower
            node.vulnerability_score = new_vulnerability_score

        elif (
            self.network_interface.game_mode.blue.action_set.make_node_safe.gives_random_vulnerability.value
        ):
            # Gives the node a new random vulnerability
            new_vulnerability_score = round(random.uniform(lower, upper), 2)
            node.vulnerability_score = new_vulnerability_score
        return "make_node_safe", node

    def scan_all_nodes(self) -> Tuple[str, None]:
        """
        Scan all of the nodes within the environment and attempt to get their states.

        The blue agents ability to see intrusions is based on the values in the config file:
            - BLUE: chance_to_discover_intrusion_on_scan
            - BLUE: chance_to_discover_intrusion_on_scan_deceptive_node

        Returns:
            The name of the action ("scan")
            The node the action was performed on (None: as scan affects all nodes, not just 1)
        """
        nodes = self.network_interface.current_graph.get_nodes()
        for node in nodes:
            self.network_interface.scan_node(node)
        return "scan", None

    def isolate_node(self, node: Node) -> Tuple[str, Node]:
        """
        Isolate a node by disabling all of its connections to other nodes.

        Args:
            node: the node to disable

        Returns:
            The name of the action ("isolate")
            The node affected
        """
        self.network_interface.isolate_node(node)

        return "isolate", node

    def reconnect_node(self, node: Node) -> Tuple[str, Node]:
        """
        Enable all of the connections to and from a node.

        Args:
            node: the node to enable to connections to

        Returns:
            The name of the action ("connect")
            The node affected
        """
        self.network_interface.reconnect_node(node)

        return "connect", node

    def do_nothing(self) -> Tuple[str, Node]:
        """
        Do Nothing.

        Returns:
            The name of the action ("do_nothing")
            The nodes affected (None: as do nothing affects no nodes)
        """
        return "do_nothing", None

    def add_deceptive_node(self, edge: int) -> Tuple[str, Union[List, None]]:
        """
        Add a deceptive node into the environment.

        Deceptive nodes are the same as standard nodes except they have a 100% chance (by default)
        to be able to detect attacks from the red agent. A deceptive node is added on an edge between two nodes.

        Args:
            edge: The edge to place the deceptive node on

        Returns:
            The name of the action performed ("add_deceptive_node" or "do_nothing" depending on if action is valid)
            A pair of nodes that the deceptive node was placed between (or None if no action performed)
        """
        # Get the nodes that are connected via the input edge
        nodes = self.network_interface.edge_map[edge]
        node = self.network_interface.add_deceptive_node(nodes[0], nodes[1])
        if not node:
            return "do_nothing", None
        else:
            return "add_deceptive_node", [node, nodes]
