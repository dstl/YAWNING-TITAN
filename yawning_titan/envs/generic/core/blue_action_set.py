import random
from typing import List, Tuple, Union

from yawning_titan.envs.generic.core.network_interface import NetworkInterface

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

    def reduce_node_vulnerability(self, node: str) -> Tuple[str, str]:
        """
        Reduce the vulnerability of the target node.

        Will not reduce the vulnerability past the lower bound setting in the
        configuration file:
            - BLUE: node_vulnerability_lower_bound

        Args:
            node: the node to reduce the vulnerability of

        Returns:
            The name of the action taken ("reduce_vulnerability")
            The node the action was taken on
        """
        node = str(node)
        # gets the current vulnerability
        current_vulnerability = self.network_interface.get_single_node_vulnerability(
            node
        )
        # updates the vulnerability of the node
        new = current_vulnerability - 0.2
        if (
            new
            < self.network_interface.game_mode.game_rules.node_vulnerability_lower_bound
        ):
            new = (
                self.network_interface.game_mode.game_rules.node_vulnerability_lower_bound
            )
        self.network_interface.update_single_node_vulnerability(node, new)
        return "reduce_vulnerability", node

    def restore_node(self, node: str) -> Tuple[str, str]:
        """
        Restore a node to its starting state: safe and with its starting vulnerability.

        Args:
            node: the node to restore

        Returns:
            The name of the action ("restore_node")
            The name of the node the action was taken on
        """
        node = str(node)
        self.network_interface.make_node_safe(node)
        self.network_interface.reset_single_node_vulnerability(node)

        return "restore_node", node

    def make_safe_node(self, node: str) -> Tuple[str, str]:
        """
        Make a target node safe.

        Can also affect the vulnerability of the node. There are settings that can change how this
        action works in the configuration file:
            - BLUE: making_node_safe_modifies_vulnerability
            - BLUE: vulnerability_change_during_node_patch
            - BLUE: making_node_safe_gives_random_vulnerability

        Args:
            The name of the action ("make_safe_node")
            The name of the node to make safe
        """
        node = str(node)
        self.network_interface.make_node_safe(node)

        # Settings change the effects of making a node safe
        if (
            self.network_interface.game_mode.blue.making_node_safe_modifies_vulnerability
        ):
            # Modifies the vulnerability by a set amount (cannot increase it past the limit in the config file)
            change_amount = (
                self.network_interface.game_mode.blue.vulnerability_change_during_node_patch
            )
            current_vulnerability = (
                self.network_interface.get_single_node_vulnerability(node)
            )
            new = change_amount + current_vulnerability
            # checks to make sure that the new value does not go out of the range for vulnerability
            if (
                new
                > self.network_interface.game_mode.game_rules.node_vulnerability_upper_bound
            ):
                new = (
                    self.network_interface.game_mode.game_rules.node_vulnerability_upper_bound
                )
            elif (
                new
                > self.network_interface.game_mode.game_rules.node_vulnerability_lower_bound
            ):
                new = (
                    self.network_interface.game_mode.game_rules.node_vulnerability_lower_bound
                )
            self.network_interface.update_single_node_vulnerability(node, new)

        elif (
            self.network_interface.game_mode.blue.making_node_safe_gives_random_vulnerability
        ):
            # Gives the node a new random vulnerability
            upper = (
                self.network_interface.game_mode.game_rules.node_vulnerability_upper_bound
            )
            lower = (
                self.network_interface.game_mode.game_rules.node_vulnerability_lower_bound
            )
            new = round(random.uniform(lower, upper), 2)
            self.network_interface.update_single_node_vulnerability(node, new)

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
        nodes = self.network_interface.get_nodes()
        for node in nodes:
            self.network_interface.scan_node(node)
        return "scan", None

    def isolate_node(self, node: str) -> Tuple[str, str]:
        """
        Isolate a node by disabling all of its connections to other nodes.

        Args:
            node: the node to disable

        Returns:
            The name of the action ("isolate")
            The node affected
        """
        node = str(node)
        self.network_interface.isolate_node(node)

        return "isolate", node

    def reconnect_node(self, node: str) -> Tuple[str, str]:
        """
        Enable all of the connections to and from a node.

        Args:
            node: the node to enable to connections to

        Returns:
            The name of the action ("connect")
            The node affected
        """
        node = str(node)
        self.network_interface.reconnect_node(node)

        return "connect", node

    def do_nothing(self) -> Tuple[str, None]:
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
        node_name = self.network_interface.add_deceptive_node(nodes[0], nodes[1])
        if node_name is False:
            return "do_nothing", None
        else:
            return "add_deceptive_node", [node_name, nodes]
