import copy
import functools
import itertools
import json
import math
import pathlib
import random
from collections import Counter, defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List, Optional, Tuple, Union

import networkx as nx
import numpy as np
import pandas as pd
import yaml
from numpy.random import choice
from yaml.loader import SafeLoader

from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.helpers.environment_input_validation import \
    check_input
from yawning_titan.envs.generic.helpers.node_attribute_gen import (
    generate_vulnerabilities,
    generate_vulnerability,
)

_LOGGER = getLogger(__name__)

class NetworkInterface:
    """The primary interface between both red and blue agents and the underlying environment."""

    def __init__(
        self,
        matrix: np.array,
        positions: dict,
        settings_path: Optional[str] = None,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_target: Optional[str] = None,
    ):
        """
        Initialise the Network Interface and initialises all of the necessary components.

        Args:
            matrix: An adjacency matrix containing the connections between nodes in the network
            positions: A dictionary containing the positions of the nodes in the network (when displayed as a graph)
            settings_path: The file path that locates the settings page. If no path is supplied then the default settings page is used
            entry_nodes: A list of nodes that act as gateways or doors in the network for the red agent. While the red
            agent does not start in the network, they can access the network at these nodes.
            vulnerabilities: A dictionary containing the vulnerabilities of the nodes
            high_value_target: A name of a node that when taken means the red agent instantly wins
        """
        # opens the fle the user has specified to be the location of the settings
        if not settings_path:
            settings_path = default_game_mode_path()
        try:
            with open(settings_path) as f:
                settings = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        number_of_nodes = len(matrix)

        # check the settings are valid
        check_input(settings, number_of_nodes)

        self.settings = settings

        # Top level Groupings
        self.red_settings = settings["RED"]
        self.observation_space_settings = settings["OBSERVATION_SPACE"]
        self.blue_settings = settings["BLUE"]
        self.game_rule_settings = settings["GAME_RULES"]
        self.reset_settings = settings["RESET"]
        self.reward_settings = settings["REWARDS"]
        self.misc_settings = settings["MISCELLANEOUS"]

        # Red Settings
        self.red_skill = self.red_settings["red_skill"]
        self.red_use_skill = self.red_settings["red_uses_skill"]
        self.red_ignore_defences = self.red_settings["red_ignores_defences"]
        self.red_always_succeeds = self.red_settings["red_always_succeeds"]
        self.red_attack_from_current_position = self.red_settings[
            "red_can_only_attack_from_red_agent_node"
        ]
        self.red_attack_from_any_node = self.red_settings[
            "red_can_attack_from_any_red_node"
        ]
        self.red_naturally_spread = self.red_settings["red_can_naturally_spread"]
        self.red_chance_to_spread_to_connected_node = self.red_settings[
            "chance_to_spread_to_connected_node"
        ]
        self.red_chance_to_spread_to_unconnected_node = self.red_settings[
            "chance_to_spread_to_unconnected_node"
        ]
        self.red_spread_action = self.red_settings["red_uses_spread_action"]
        self.red_spread_action_likelihood = self.red_settings[
            "spread_action_likelihood"
        ]
        self.red_spread_success_chance = self.red_settings["chance_for_red_to_spread"]
        self.red_random_infection_action = self.red_settings[
            "red_uses_random_infect_action"
        ]
        self.red_random_infection_likelihood = self.red_settings[
            "red_uses_random_infect_action"
        ]
        self.red_random_infection_success_chance = self.red_settings[
            "chance_for_red_to_random_compromise"
        ]
        self.red_basic_attack_action = self.red_settings["red_uses_basic_attack_action"]
        self.red_basic_attack_likelihood = self.red_settings[
            "basic_attack_action_likelihood"
        ]
        self.red_do_nothing_action = self.red_settings["red_uses_do_nothing_action"]
        self.red_do_nothing_likelihood = self.red_settings[
            "do_nothing_action_likelihood"
        ]
        self.red_move_action = self.red_settings["red_uses_move_action"]
        self.red_move_action_likelihood = self.red_settings["move_action_likelihood"]
        self.red_zero_day_action = self.red_settings["red_uses_zero_day_action"]
        self.red_zero_day_start_amount = self.red_settings["zero_day_start_amount"]
        self.red_zero_day_days_required_to_create = self.red_settings[
            "days_required_for_zero_day"
        ]
        self.red_targeting_random = self.red_settings["red_chooses_target_at_random"]
        self.red_targeting_prioritise_connected_nodes = self.red_settings[
            "red_prioritises_connected_nodes"
        ]
        self.red_targeting_prioritise_unconnected_nodes = self.red_settings[
            "red_prioritises_un_connected_nodes"
        ]
        self.red_targeting_prioritise_vulnerable_nodes = self.red_settings[
            "red_prioritises_vulnerable_nodes"
        ]
        self.red_targeting_prioritise_resilient_nodes = self.red_settings[
            "red_prioritises_resilient_nodes"
        ]

        # Observation Space Settings
        self.obs_compromised_status = self.observation_space_settings[
            "compromised_status"
        ]
        self.obs_node_vuln_status = self.observation_space_settings["vulnerabilities"]
        self.obs_node_connections = self.observation_space_settings["node_connections"]
        self.obs_avg_vuln = self.observation_space_settings["average_vulnerability"]
        self.obs_graph_connectivity = self.observation_space_settings[
            "graph_connectivity"
        ]
        self.obs_attack_sources = self.observation_space_settings["attacking_nodes"]
        self.obs_attack_targets = self.observation_space_settings["attacked_nodes"]
        self.obs_special_nodes = self.observation_space_settings["special_nodes"]
        self.obs_red_agent_skill = self.observation_space_settings["red_agent_skill"]

        # Blue Settings
        self.blue_max_deceptive_nodes = self.blue_settings["max_number_deceptive_nodes"]
        self.blue_immediate_detection_chance = self.blue_settings[
            "chance_to_immediately_discover_intrusion"
        ]
        self.blue_scan_detection_chance = self.blue_settings[
            "chance_to_discover_intrusion_on_scan"
        ]
        self.blue_deception_immediate_detection_chance = self.blue_settings[
            "chance_to_immediately_discover_intrusion_deceptive_node"
        ]  # noqa
        self.blue_deception_scan_detection_chance = self.blue_settings[
            "chance_to_discover_intrusion_on_scan_deceptive_node"
        ]  # noqa
        self.blue_discover_failed_attacks = self.blue_settings[
            "can_discover_failed_attacks"
        ]
        self.blue_discover_attack_source_if_detected = self.blue_settings[
            "can_discover_succeeded_attacks_if_compromise_is_discovered"
        ]  # noqa
        self.blue_discover_attack_source_if_not_detected = self.blue_settings[
            "can_discover_succeeded_attacks_if_compromise_is_not_discovered"
        ]  # noqa
        self.blue_chance_to_discover_source_failed = self.blue_settings[
            "chance_to_discover_failed_attack"
        ]
        self.blue_chance_to_discover_source_succeed_known = self.blue_settings[
            "chance_to_discover_succeeded_attack_compromise_known"
        ]  # noqa
        self.blue_chance_to_discover_source_succeed_unknown = self.blue_settings[
            "chance_to_discover_succeeded_attack_compromise_not_known"
        ]  # noqa
        self.blue_chance_to_discover_source_deceptive_failed = self.blue_settings[
            "chance_to_discover_failed_attack_deceptive_node"
        ]  # noqa
        self.blue_chance_to_discover_source_deceptive_succeed = self.blue_settings[
            "chance_to_discover_succeeded_attack_deceptive_node"
        ]  # noqa
        self.blue_make_node_safe_modifies_vuln = self.blue_settings[
            "making_node_safe_modifies_vulnerability"
        ]
        self.blue_vuln_change_amount_make_safe = self.blue_settings[
            "vulnerability_change_during_node_patch"
        ]
        self.blue_make_safe_random_vuln = self.blue_settings[
            "making_node_safe_gives_random_vulnerability"
        ]
        self.blue_reduce_vuln_action = self.blue_settings[
            "blue_uses_reduce_vulnerability"
        ]
        self.blue_restore_node_action = self.blue_settings["blue_uses_restore_node"]
        self.blue_make_node_safe_action = self.blue_settings["blue_uses_make_node_safe"]
        self.blue_scan_action = self.blue_settings["blue_uses_scan"]
        self.blue_isolate_action = self.blue_settings["blue_uses_isolate_node"]
        self.blue_reconnect_action = self.blue_settings["blue_uses_reconnect_node"]
        self.blue_do_nothing_action = self.blue_settings["blue_uses_do_nothing"]
        self.blue_deceptive_action = self.blue_settings["blue_uses_deceptive_nodes"]
        self.blue_deceptive_node_make_new = self.blue_settings[
            "relocating_deceptive_nodes_generates_a_new_node"
        ]

        # Game Rule Settings
        self.gr_node_vuln_lower = self.game_rule_settings[
            "node_vulnerability_lower_bound"
        ]
        self.gr_node_vuln_upper = self.game_rule_settings[
            "node_vulnerability_upper_bound"
        ]
        self.gr_max_steps = self.game_rule_settings["max_steps"]
        self.gr_loss_total_compromise = self.game_rule_settings[
            "lose_when_all_nodes_lost"
        ]
        self.gr_loss_pc_nodes_compromised = self.game_rule_settings[
            "lose_when_n_percent_of_nodes_lost"
        ]
        self.gr_loss_pc_node_compromised_pc = self.game_rule_settings[
            "percentage_of_nodes_compromised_equals_loss"
        ]
        self.gr_loss_hvt = self.game_rule_settings["lose_when_high_value_target_lost"]
        self.gr_loss_hvt_random_placement = self.game_rule_settings[
            "choose_high_value_target_placement_at_random"
        ]
        self.gr_loss_hvt_furthest_away = self.game_rule_settings[
            "choose_high_value_target_furthest_away_from_entry"
        ]
        self.gr_random_entry_nodes = self.game_rule_settings[
            "choose_entry_nodes_randomly"
        ]
        self.gr_num_entry_nodes = self.game_rule_settings["number_of_entry_nodes"]
        self.gr_prefer_central_entry = self.game_rule_settings[
            "prefer_central_nodes_for_entry_nodes"
        ]
        self.gr_prefer_edge_nodes = self.game_rule_settings[
            "prefer_edge_nodes_for_entry_nodes"
        ]
        self.gr_grace_period = self.game_rule_settings["grace_period_length"]

        # Reset Settings
        self.reset_random_vulns = self.reset_settings[
            "randomise_vulnerabilities_on_reset"
        ]
        self.reset_move_hvt = self.reset_settings[
            "choose_new_high_value_target_on_reset"
        ]
        self.reset_move_entry_nodes = self.reset_settings[
            "choose_new_entry_nodes_on_reset"
        ]

        # Reward Settings
        self.reward_loss = self.reward_settings["rewards_for_loss"]
        self.reward_success = self.reward_settings["rewards_for_reaching_max_steps"]
        self.reward_end_multiplier = self.reward_settings[
            "end_rewards_are_multiplied_by_end_state"
        ]
        self.reward_reduce_negative_rewards = self.reward_settings[
            "reduce_negative_rewards_for_closer_fails"
        ]
        self.reward_function = self.reward_settings["reward_function"]

        # Misc Settings
        self.misc_json_out = self.misc_settings["output_timestep_data_to_json"]

        nodes = [str(i) for i in range(number_of_nodes)]
        df = pd.DataFrame(matrix, index=nodes, columns=nodes)
        graph = nx.from_pandas_adjacency(df)

        # initialise the current graph
        self.current_graph = graph

        # initialise the base graph
        self.base_graph = copy.deepcopy(graph)
        self.initial_base_graph = copy.deepcopy(graph)

        # initialise data storage

        self.initial_network_variables = {
            i: {
                "vulnerability_score": 0,
                "true_compromised_status": 0,
                "blue_view_compromised_status": 0,
                "node_position": 0,
                "deceptive_node": False,
                "blue_knows_intrusion": False,
                "isolated": False,
            }
            for i in nodes
        }

        # If no vulnerabilities supplied then generate some
        if vulnerabilities is None:
            vulnerabilities = generate_vulnerabilities(
                number_of_nodes, self.gr_node_vuln_lower, self.gr_node_vuln_upper
            )

        # initialise the network variables
        for node in nodes:
            # vulnerability scores
            self.initial_network_variables[node][
                "vulnerability_score"
            ] = vulnerabilities[node]
            # node positions
            self.initial_network_variables[node]["node_position"] = positions[node]

        self.initial_deceptive_vulnerabilities = {}

        # If no entry nodes supplied then the first node in the network is chosen as the initial node
        self.entry_node_weights = [1 / number_of_nodes for _ in range(number_of_nodes)]
        if entry_nodes is None:
            if self.gr_random_entry_nodes:
                try:
                    node_dict = nx.algorithms.centrality.eigenvector_centrality(
                        self.current_graph, max_iter=500
                    )
                except nx.PowerIterationFailedConvergence:
                    node_dict = {node: 0.5 for node in self.current_graph.nodes()}
                weights = list(node_dict.values())
                all_nodes = list(node_dict.keys())

                if self.gr_prefer_edge_nodes:
                    weights = list(map(lambda x: (1 / x) ** 4, weights))
                elif self.gr_prefer_central_entry:
                    weights = list(map(lambda x: x**4, weights))
                else:
                    weights = [1] * len(all_nodes)

                weights_normal = [float(i) / sum(weights) for i in weights]
                self.entry_node_weights = weights_normal
                entry_nodes = choice(
                    all_nodes,
                    self.gr_num_entry_nodes,
                    replace=False,
                    p=weights_normal,
                )

            else:
                entry_nodes = []
                for i in range(self.gr_num_entry_nodes):
                    entry_nodes.append(nodes[i])

        self.entry_nodes = entry_nodes
        self.possible_high_value_targets = [] if high_value_target is None else [high_value_target]
        number_possible_high_value = math.ceil(
            (len(self.current_graph.nodes) - len(self.entry_nodes) + 1) * 0.15
        )
        if high_value_target is None:
            # chooses a random node to be the high value target
            if self.gr_loss_hvt_random_placement:
                self.possible_high_value_targets = list(
                    set(nodes).difference(set(self.entry_nodes))
                )
            # Choose the node that is furthest away from the entry points as the high value target
            if self.gr_loss_hvt_furthest_away:
                # gets all the paths between nodes
                paths = []
                for i in self.entry_nodes:
                    paths.append(
                        dict(nx.all_pairs_shortest_path_length(self.current_graph))[i]
                    )
                sums = Counter()
                counters = Counter()
                # gets the distances to the entry points
                for itemset in paths:
                    sums.update(itemset)
                    counters.update(itemset.keys())
                # averages the distances to find the node that is, on average, the furthest away
                result = {x: float(sums[x]) / counters[x] for x in sums.keys()}
                for i in range(number_possible_high_value):
                    current = max(result, key=result.get)
                    self.possible_high_value_targets.append(current)
                    result.pop(current)

        if self.gr_loss_hvt:
            self.high_value_target = random.choices(
                population=self.possible_high_value_targets, k=1
            )[0]
        else:
            self.high_value_target = None

        # initialises the deceptive nodes and their names and amount
        self.deceptive_nodes = []
        for i in range(0, self.blue_max_deceptive_nodes):
            name = "d" + str(i)
            self.deceptive_nodes.append(name)
        # a pointer to to point to the current deceptive node (when a new node is added but the max is reached the
        # oldest node is replaced)
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False

        # a edge dictionary to give each edge a unique single number
        self.edge_map = {}
        edges = self.base_graph.edges
        for counter, i in enumerate(edges):
            self.edge_map[counter] = i

        self.red_current_location = None

        # a list of all of the failed attacks that occurred on this turn
        self.true_attacks = []
        # a list of all the failed attacks that blue has been able to detect
        self.detected_attacks = []

        self.current_network_variables = copy.deepcopy(self.initial_network_variables)

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

    def get_number_base_edges(self) -> int:
        """
        Get the number of edges in the base original graph.

        This is not affected by nodes being isolated or modified by the agents.

        Returns:
            The number of base edges in the network
        """
        return len(self.base_graph.edges)

    def get_number_current_edges(self) -> int:
        """
        Get the number of edges in the current original graph.

        This is not affected by nodes being isolated or modified by the agents.

        Returns:
            The number of base edges in the network
        """
        return len(self.current_graph.edges)

    def get_entry_nodes(self) -> List[str]:
        """
        Get the entry nodes within the environment.

        Returns:
            The entry nodes for the network
        """
        return self.entry_nodes

    def get_number_of_nodes(self) -> int:
        """
        Get the total number of nodes within the environment.

        Returns:
            The number of nodes in the network
        """
        return len(self.current_network_variables.keys())

    def get_total_num_nodes(self) -> int:
        """
        Get the total number of nodes including any yet to be placed deceptive nodes.

        Returns:
            The number of nodes that there are including deceptive nodes that may not have been placed yet
        """
        return self.get_number_of_nodes() + self.get_number_unused_deceptive_nodes()

    def get_midpoint(self, node1: str, node2: str) -> Tuple[float, float]:
        """
        Get the midpoint between the position of two nodes.

        Args:
            node1: the name of the first node to get the midpoint from
            node2: the name of the second node to get the midpoint from

        Returns:
            The x and y coordinates of the midpoint between two nodes
        """
        # get positions of nodes
        pos1_x, pos1_y = self.current_network_variables[node1]["node_position"]
        pos2_x, pos2_y = self.current_network_variables[node2]["node_position"]

        # calculate midpoint
        x = (float(pos1_x) + float(pos2_x)) / 2
        y = (float(pos1_y) + float(pos2_y)) / 2

        return x, y

    def get_current_connected_nodes(self, node: str) -> List[str]:
        """
        Get all of the nodes currently connected to a target node.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return list(self.current_graph.neighbors(node))

    def get_edge_map(self) -> dict:
        """
        Get an edge map which maps network edges to numbers.

        Returns:
            Returns the edge map
        """
        return self.edge_map

    def get_base_connected_nodes(self, node: str) -> List[str]:
        """
        Get all of the nodes connected to the given node in the base graph.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return list(self.base_graph.neighbors(node))

    def get_single_node_state(self, node: str) -> int:
        """
        Get the current state of a node (safe or compromised).

        Args:
            node: The name of the node to check the compromised status of

        Returns:
            0: safe, 1: compromised
        """
        return self.current_network_variables[node]["true_compromised_status"]

    def get_single_node_blue_view(self, node: str) -> int:
        """
        Get the current state of a node (safe or compromised).

        Args:
            node: The name of the node to check the compromised status of

        Returns:
            0: safe, 1: compromised

        """
        return self.current_network_variables[node]["blue_view_compromised_status"]

    def get_single_node_vulnerability(self, node: str) -> int:
        """
        Get the current vulnerability of a node.

        Args:
            node: The name of the node to check the vulnerability of

        Returns:
            0: safe, 1: compromised
        """
        return self.current_network_variables[node]["vulnerability_score"]

    def get_single_node_known_intrusion_status(self, node: str) -> bool:
        """
        Return True if blue knows about the intrusion in this node, False if not.

        Args:
            node: The name of the node to check the status of

        Returns:
            True if blue knows about the intrusion in this node, False if not
        """
        return self.current_network_variables[node]["blue_knows_intrusion"]

    def get_single_node_isolation_status(self, node: str) -> bool:
        """
        Get the isolation status for a single node.

        Args:
            node: The name of the node to get the isolation status for

        Returns:
            Boolean representing the isolation status of the node
        """
        return self.current_network_variables[node]["isolated"]

    def get_single_node_position(self, node: str) -> Tuple[int, int]:
        """
        Get the position of a single node.

        Args:
            node: The name of the node to get the position of

        Returns:
            A list containing an x coord and a y coord
        """
        return self.current_network_variables[node]["node_position"]

    def get_high_value_target(self):
        """Get the node index for the high value target."""
        return self.high_value_target

    def get_red_location(self) -> str:
        """Get the node index for the red agents current position."""
        return self.red_current_location

    def get_current_adj_matrix(self):
        """Get the current adjacency matrix for the environment."""
        return self.adj_matrix

    def get_current_graph_as_dict(self) -> Dict:
        """
        Get the current networkx graph for the environment and convert it to a dict of dicts.

        Returns:
            The networkx graph as a dict  of dicts
        """
        return nx.to_dict_of_dicts(self.current_graph)

    def get_attributes_from_key(self, key: str) -> dict:
        """
        Take in a key and return a dictionary.

        The keys are the names of the nodes and the values are the attribute values that are stored for
        that node under the specified key

        Args:
            key: The name of the attribute to extract

        Returns:
            A dictionary of attributes
        """
        filter_on_key = lambda x, node: {  # noqa
            node: attribute for name, attribute in x.items() if name == key  # noqa
        }  # noqa
        extract = lambda x: map(filter_on_key, x.values(), x.keys())  # noqa
        out = functools.reduce(
            lambda x, y: {**x, **y}, extract(self.current_network_variables)  # noqa
        )

        return out

    def get_nodes(
        self,
        filter_true_compromised: bool = False,
        filter_blue_view_compromised: bool = False,
        filter_true_safe: bool = False,
        filter_blue_view_safe: bool = False,
        filter_isolated: bool = False,
        filter_non_isolated: bool = False,
        filter_deceptive: bool = False,
        filter_non_deceptive: bool = False,
    ) -> List[str]:
        """
        Get all of the nodes from the network and apply a filter(s) to extract a specific subset of the nodes.

        Args:
            filter_true_compromised: Filter so only nodes that are compromised remain
            filter_blue_view_compromised: Filter so only nodes that blue can see are compromised remain
            filter_true_safe: Filter so only nodes that are safe remain
            filter_blue_view_safe: Filter so only nodes that blue can see are safe remain
            filter_isolated: Filter so only isolated nodes remain
            filter_non_isolated: Filter so only connected nodes remain
            filter_deceptive: Filter so only deceptive nodes remain
            filter_non_deceptive: Filter so only non-deceptive nodes remain

        Returns:
            A list of nodes
        """
        filter_functions = [True]
        if filter_true_compromised:
            # Return true if compromised status is 1
            filter_functions.append(
                lambda x: self.current_network_variables[x]["true_compromised_status"]
                == 1
            )
        if filter_blue_view_compromised:
            # Return True if blue view compromised status is 1
            filter_functions.append(
                lambda x: self.current_network_variables[x][
                    "blue_view_compromised_status"
                ]
                == 1
            )
        if filter_true_safe:
            # Return True if compromised status is 0
            filter_functions.append(
                lambda x: self.current_network_variables[x]["true_compromised_status"]
                == 0
            )
        if filter_blue_view_safe:
            # Return True if blue view compromised status is 0
            filter_functions.append(
                lambda x: self.current_network_variables[x][
                    "blue_view_compromised_status"
                ]
                == 0
            )
        if filter_isolated:
            # Return True if isolated is True
            filter_functions.append(
                lambda x: self.current_network_variables[x]["isolated"] is True
            )
        if filter_non_isolated:
            # Return True if isolated is False
            filter_functions.append(
                lambda x: self.current_network_variables[x]["isolated"] is False
            )
        if filter_deceptive:
            # Return True if deceptive node is True
            filter_functions.append(
                lambda x: self.current_network_variables[x]["deceptive_node"] is True
            )
        if filter_non_deceptive:
            # Return True if deceptive node is False
            filter_functions.append(
                lambda x: self.current_network_variables[x]["deceptive_node"] is False
            )

        # Combine all of the selected filters into a single statement
        combined_filters = lambda node: functools.reduce(  # noqa
            lambda x, y: x and y(node), filter_functions
        )

        # Apply the filters to the list of nodes
        filtered_nodes = list(
            filter(combined_filters, self.current_network_variables.keys())
        )
        if filtered_nodes is None:
            return []
        return filtered_nodes

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
        return self.get_attributes_from_key("node_position")

    def get_detected_attacks(self) -> List[str]:
        """
        Get a list of lists containing detected attacks.

        The format of this list of lists is [["3", "4"]] for example.
        This means that the blue agent detected an attack originating from
        node "3" which was attacking node "4".
        """
        return self.detected_attacks

    def get_true_attacks(self) -> List[str]:
        """
        Get a list of lists containing all attacks (those detected by blue and those not detected by blue).

        The format of this list of lists is the same as the ``get_detected_attacks`` function above.
        """
        return self.true_attacks

    def get_number_unused_deceptive_nodes(self):
        """Get the current number of unused deceptive nodes."""
        return self.blue_max_deceptive_nodes - self.current_deceptive_nodes

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
        if self.obs_node_connections:
            node_connections = self.adj_matrix
            # pads the array to account for any missing deceptive nodes that may not have been placed yet
            node_connections = np.pad(node_connections, (0, open_spaces), "constant")

        # Gets the current safe/compromised status of all of the nodes
        compromised_state = []
        if self.obs_compromised_status:
            compromised_state = np.asarray(
                list(self.get_attributes_from_key("true_compromised_status").values())
            )
            compromised_state = np.pad(compromised_state, (0, open_spaces), "constant")
        # Gets the vulnerability score of all of the nodes
        vulnerabilities = []
        if self.obs_node_vuln_status:
            vulnerabilities = np.asarray(
                list(self.get_attributes_from_key("vulnerability_score").values())
            )
            vulnerabilities = np.pad(vulnerabilities, (0, open_spaces), "constant")

        # Gets the average vulnerability of all the nodes
        avg_vuln = []
        if self.obs_avg_vuln:
            all_vuln = self.get_attributes_from_key("vulnerability_score").values()
            avg_vuln = [sum(all_vuln) / len(all_vuln)]

        # Gets the connectivity of the graph, closer to 1 means more edges per node
        connectivity = []
        if self.obs_graph_connectivity:
            connectivity = [self.connectivity]

        # Gets the attacks that the blue agent detected
        attacking_nodes = []
        attacked_nodes = []
        if self.obs_attack_sources or self.obs_attack_targets:
            attacking = {name: 0 for name in self.get_nodes()}
            attacked = {name: 0 for name in self.get_nodes()}
            for i in self.detected_attacks:
                if i[0] is not None:
                    # extract the attacking node (as long as the attacking node is not None)
                    attacking[i[0]] = 1
                # extract the node that was attacked
                attacked[i[1]] = 1
            if self.obs_attack_sources:
                # attacking nodes
                attacking_nodes = list(attacking.values())
                attacking_nodes = np.pad(attacking_nodes, (0, open_spaces), "constant")
            if self.obs_attack_targets:
                # nodes attacked
                attacked_nodes = list(attacked.values())
                attacked_nodes = np.pad(attacked_nodes, (0, open_spaces), "constant")

        # Gets the locations of any special nodes in the network (entry nodes and high value nodes)
        entry_nodes = []
        high_value_target = []
        if self.obs_special_nodes:
            # gets the entry nodes
            entry_nodes = {name: 0 for name in self.get_nodes()}
            for i in self.entry_nodes:
                entry_nodes[i] = 1
            entry_nodes = list(entry_nodes.values())
            entry_nodes = np.pad(entry_nodes, (0, open_spaces), "constant")

            if self.gr_loss_hvt:
                # gets the high value target node
                high_value_target = {name: 0 for name in self.get_nodes()}
                high_value_target[self.high_value_target] = 1
                high_value_target = list(high_value_target.values())
                high_value_target = np.pad(
                    high_value_target, (0, open_spaces), "constant"
                )

        # gets the skill of the red agent
        skill = []
        if self.obs_red_agent_skill:
            skill = [self.red_skill]

        # combines all of the env observations together to create the observation that the blue agent gets
        obs = np.concatenate(
            (
                node_connections,
                compromised_state,
                vulnerabilities,
                avg_vuln,
                connectivity,
                attacking_nodes,
                attacked_nodes,
                entry_nodes,
                high_value_target,
                skill,
            ),
            axis=None,
            dtype=np.float32,
        )

        return obs

    def get_observation_size(self) -> int:
        """
        Get the size of the observation space.

        This is based on the settings that are turned on/off.

        Returns:
            The size of the observation space
        """
        # gets the max number of nodes in the env (including deceptive nodes)
        observation_size = 0
        max_number_of_nodes = self.get_total_num_nodes()

        # calculate the size of the observation space
        # the size depends on what observations are turned on/off in the config file
        if self.obs_node_connections:
            observation_size += max_number_of_nodes * max_number_of_nodes
        if self.obs_compromised_status:
            observation_size += max_number_of_nodes
        if self.obs_node_vuln_status:
            observation_size += max_number_of_nodes
        if self.obs_avg_vuln:
            observation_size += 1
        if self.obs_graph_connectivity:
            observation_size += 1
        if self.obs_attack_sources:
            observation_size += max_number_of_nodes
        if self.obs_attack_targets:
            observation_size += max_number_of_nodes
        if self.obs_special_nodes:
            observation_size += max_number_of_nodes
            if self.gr_loss_hvt:
                observation_size += max_number_of_nodes
        if self.obs_red_agent_skill:
            observation_size += 1

        return observation_size

    """
    SETTERS
    The following block of code contains the setters for the network_interface. Setters are a type of method that update
    or change a class attribute
    """

    def update_single_node_compromised_status(self, node: str, value: int):
        """
        Modify the value of the compromised status of a single node.

        Args:
            node: The name of the node to affect
            value: The new value of the compromised status for the node
        """
        self.current_network_variables[node]["true_compromised_status"] = value

    def update_single_node_vulnerability(self, node: str, value: float):
        """
        Modify the value of the vulnerability status of a single node.

        Args:
            node: The name of the node to affect
            value: The new value of the vulnerability for the node
        """
        self.current_network_variables[node]["vulnerability_score"] = value

    def update_single_node_blue_view(self, node: str, status: int):
        """
        Update the blue's view of the compromised status of a node.

        Args:
            node: The name of the node to update the status for
            status: The new status of the node
        """
        self.current_network_variables[node]["blue_view_compromised_status"] = status

    def update_single_node_known_intrusions(self, node: str, value: bool):
        """
        Modify the value of the known intrusion status of a single node.

        Args:
            node: The name of the node to affect
            value: The new value of the known intrusion status for the node
        """
        self.current_network_variables[node]["blue_knows_intrusion"] = value

    def update_red_location(self, location: str):
        """
        Modify the value of the red location.

        Args:
            location: The name of the node the red agent is now occupying
        """
        self.red_current_location = location

    def update_stored_attacks(
        self, attacking_nodes: List[str], target_nodes: List[str], success: List[bool]
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
        for i, j, k in zip(attacking_nodes, target_nodes, success):
            # Deceptive nodes have a different chance of detecting attacks
            if self.current_network_variables[j]["deceptive_node"]:
                if k:
                    # chance of seeing the attack if the attack succeeded
                    if (
                        100 * self.blue_chance_to_discover_source_deceptive_succeed
                        > random.randint(0, 99)
                    ):
                        self.detected_attacks.append([i, j])
                else:
                    # chance of seeing the attack if the attack fails
                    if (
                        100 * self.blue_chance_to_discover_source_deceptive_failed
                        > random.randint(0, 99)
                    ):
                        self.detected_attacks.append([i, j])
            else:
                # If the attack did not succeed
                if k is False:
                    if self.blue_discover_failed_attacks:
                        if (
                            100 * self.blue_chance_to_discover_source_failed
                            > random.randint(0, 99)
                        ):
                            # Adds the attack to the list of current attacks for this turn
                            self.detected_attacks.append([i, j])
                else:
                    # If the attack succeeded and the blue agent detected it
                    if (
                        self.current_network_variables[j][
                            "blue_view_compromised_status"
                        ]
                        == 1
                    ):
                        if self.blue_discover_attack_source_if_detected:
                            if (
                                self.blue_chance_to_discover_source_succeed_known
                                > random.randint(0, 99)
                            ):
                                self.detected_attacks.append([i, j])
                    else:
                        # If the attack succeeded but blue did not detect it
                        if self.blue_chance_to_discover_source_succeed_unknown:
                            if (
                                100
                                * self.blue_chance_to_discover_source_succeed_unknown
                                > random.randint(0, 99)
                            ):
                                self.detected_attacks.append([i, j])
            # Also compiles a list of all the attacks even those that blue did not "see"
            self.true_attacks.append([i, j])

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
        self.detected_attacks = []

    def reset(self):
        """Reset the network back to its default state."""
        # red location
        self.red_current_location = None

        # Environment variables are reset
        self.current_network_variables = {
            node: {
                heading: value
                for heading, value in self.initial_network_variables[node].items()
            }
            for node in self.initial_network_variables.keys()
        }

        # resets the network graph from the saved base graph
        self.base_graph = nx.Graph()
        self.base_graph.add_nodes_from(self.initial_base_graph.nodes)
        self.base_graph.add_edges_from(self.initial_base_graph.edges)
        # pointers and helpers for deceptive nodes are reset
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False
        # resets the current network graph from the base graph
        self.current_graph = nx.Graph()
        self.current_graph.add_nodes_from(self.base_graph.nodes)
        self.current_graph.add_edges_from(self.base_graph.edges)
        # any previous attacks are removed
        self.true_attacks = []
        self.detected_attacks = []
        # updates the stored adj matrix
        self.adj_matrix = nx.to_numpy_array(self.current_graph)

        if self.reset_move_entry_nodes:
            # change the entry nodes to a number of new random entry nodes using the pre-made wights
            entry_nodes = choice(
                self.get_nodes(),
                self.gr_num_entry_nodes,
                replace=False,
                p=self.entry_node_weights,
            )
            self.entry_nodes = entry_nodes

            if self.gr_loss_hvt and self.reset_move_hvt:

                if self.gr_loss_hvt_random_placement:
                    self.possible_high_value_targets = list(
                        set(self.current_graph.nodes()).difference(
                            set(self.entry_nodes)
                        )
                    )

                if self.gr_loss_hvt_furthest_away:
                    self.possible_high_value_targets = []

                    # Unsure what this is here for - Unused but may be relevant
                    # number_possible_high_value = math.ceil(
                    #    (len(self.current_graph.nodes) - len(self.entry_nodes) + 1)
                    #    * 0.15
                    # )
                    # gets all the paths between nodes
                    paths = []
                    for i in self.entry_nodes:
                        paths.append(
                            dict(nx.all_pairs_shortest_path_length(self.current_graph))[
                                i
                            ]
                        )
                    sums = Counter()
                    counters = Counter()
                    # gets the distances to the entry points
                    for itemset in paths:
                        sums.update(itemset)
                        counters.update(itemset.keys())
                    # averages the distances to find the node that is, on average, the furthest away
                    result = {x: float(sums[x]) / counters[x] for x in sums.keys()}
                    current = max(result, key=result.get)
                    self.possible_high_value_targets.append(current)
        # If turned on in the config file then choose a new high value target to defend
        if self.reset_move_hvt and self.gr_loss_hvt:
            # change the position of the high value target to a new random position
            self.high_value_target = random.choices(
                population=self.possible_high_value_targets, k=1
            )[0]
        if self.reset_random_vulns:
            # change all of the node vulnerabilities to new random values
            vulnerabilities = generate_vulnerabilities(
                self.get_number_of_nodes(),
                self.gr_node_vuln_lower,
                self.gr_node_vuln_upper,
            )

            # modify the vulnerabilities to be new values
            for node in self.get_nodes():
                # update the initial stored vulnerabilities
                self.initial_network_variables[node][
                    "vulnerability_score"
                ] = vulnerabilities[node]
                self.current_network_variables[node][
                    "vulnerability_score"
                ] = vulnerabilities[node]

    def reset_single_node_vulnerability(self, node: str):
        """
        Reset a nodes vulnerability score back to the same value it started with.

        Args:
            node: The name of the node to change the vulnerability of
        """
        if "d" in node:
            self.current_network_variables[node][
                "vulnerability_score"
            ] = self.initial_deceptive_vulnerabilities[node]
        else:
            self.current_network_variables[node][
                "vulnerability_score"
            ] = self.initial_network_variables[node]["vulnerability_score"]

    """
    STANDARD METHODS
    The following block of code contains the standard methods that are used to interact with the network interface in
    in some complex way.
    """

    def push_red(self):
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
            if self.get_single_node_state(node) == 1:
                self.red_current_location = node
                done = True
                break
        if done is False:
            # If there were no nodes then the agent is removed from the network
            self.red_current_location = None

    def add_deceptive_node(self, node1: str, node2: str) -> Union[bool, str]:
        """
        Add a deceptive node into the network.

        The deceptive node will sit between two actual nodes and act as a normal node in all
        regards other than the fact that it give more information when it is attacked

        Args:
            node1: Name of the first node to connect to the deceptive node to
            node2: Name of the second to connect the deceptive node to

        Returns:
            False if failed, the name of the new node if succeeded

        """
        # Check if there exists an edge between the two nodes
        if self.base_graph.has_edge(node1, node2):
            # If the red agent is in the deceptive node at its old position, push it out to a surrounding node
            if self.red_current_location == "d" + str(self.deceptive_node_pointer):
                self.push_red()
            # get the name of the new node and add the new node

            node_name = self.deceptive_nodes[self.deceptive_node_pointer]
            # If the node is already in use, remove it from the base graph
            if self.base_graph.has_node(node_name):
                self.remove_node_yt(node_name, self.base_graph)

            # inserts a new node on the base graph
            self.insert_node_between(node_name, node1, node2, self.base_graph)

            # If the node is already in use, remove it from the current graph
            if self.current_graph.has_node(node_name):
                self.remove_node_yt(node_name, self.current_graph)

            # check the isolation status of the nodes
            if (node1, node2) in self.current_graph.edges(node1) or (
                node2,
                node1,
            ) in self.current_graph.edges(node1):
                # neither are isolated: use the insert between method to insert the new node on the current graph
                self.insert_node_between(node_name, node1, node2, self.current_graph)
            elif self.current_network_variables[node1]["isolated"] is False:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(node_name)
                self.current_graph.add_edge(node1, node_name)
            elif self.current_network_variables[node2]["isolated"] is False:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(node_name)
                self.current_graph.add_edge(node2, node_name)
            else:
                # both nodes are isolated: add the node to the graph
                self.current_graph.add_node(node_name)

            # increase the pointer to point to the next element in the list (the next deceptive node to use)
            self.deceptive_node_pointer += 1
            if not self.reached_max_deceptive_nodes:
                # checks if all the deceptive nodes are in play
                self.current_deceptive_nodes += 1
            if self.deceptive_node_pointer == len(self.deceptive_nodes):
                self.deceptive_node_pointer = 0
            if self.current_deceptive_nodes == len(self.deceptive_nodes):
                self.reached_max_deceptive_nodes = True

            new_vulnerability = generate_vulnerability(
                self.gr_node_vuln_lower, self.gr_node_vuln_upper
            )

            if node_name not in self.current_network_variables:
                # sets the state of the node (only if it was not used before)
                self.current_network_variables[node_name] = {
                    "vulnerability_score": new_vulnerability,
                    "true_compromised_status": 0,
                    "blue_view_compromised_status": 0,
                    "node_position": self.get_midpoint(node1, node2),
                    "deceptive_node": True,
                    "blue_knows_intrusion": False,
                    "isolated": False,
                }
                self.initial_deceptive_vulnerabilities[node_name] = new_vulnerability
            # updates all of the nodes attributes if the setting is True
            if self.blue_deceptive_node_make_new:
                self.current_network_variables[node_name] = {
                    "vulnerability_score": new_vulnerability,
                    "true_compromised_status": 0,
                    "blue_view_compromised_status": 0,
                    "node_position": 0,
                    "deceptive_node": True,
                    "blue_knows_intrusion": False,
                    "isolated": False,
                }
                self.initial_deceptive_vulnerabilities[node_name] = new_vulnerability
            # updates the position of the node based on its new location
            self.current_network_variables[node_name][
                "node_position"
            ] = self.get_midpoint(node1, node2)
            # updates the current adjacency matrix
            self.adj_matrix = self.adj_matrix = nx.to_numpy_array(self.current_graph)
            return node_name
        else:
            # If no edge return false as the deceptive node cannot be put here
            return False

    def remove_node_yt(self, node_name: str, graph: nx.Graph) -> None:
        """
        Remove a node from a graph.

        Removing a node removes all connections to and from that node

        Args:
            node_name: the name of the node to remove
            graph: the networkx graph to remove the node from
        """
        # extracts the 0th element from a list where a variable "to_remove" has been removed
        extract_connections = lambda x, to_remove: list(  # noqa
            filter(lambda z: z != to_remove, x)  # noqa
        )[
            0
        ]  # noqa

        # gets all of the edges from a node
        links = graph.edges(node_name)
        # gets the connections to this node using the extract_connections lambda function
        connections = [extract_connections(x, node_name) for x in links]
        if len(connections) >= 2:
            # generates the new connections
            new_links = list(itertools.combinations(connections, 2))
            # adds the new edges
            graph.add_edges_from(new_links)
        # removes the old node
        graph.remove_node(node_name)

    def insert_node_between(
        self, new_node: str, node1: str, node2: str, graph: nx.Graph
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
        graph.remove_edge(node1, node2)
        graph.add_node(new_node)
        # adds the new node in and updates the edges
        graph.add_edge(node1, new_node)
        graph.add_edge(new_node, node2)

    def isolate_node(self, node: str):
        """
        Isolate a node (disable all of the nodes connections).

        Args:
            node: the node to disable the connections of

        """
        current_connections = self.get_current_connected_nodes(node)
        for i in current_connections:
            self.current_graph.remove_edge(node, i)
        self.current_network_variables[node]["isolated"] = True
        self.adj_matrix = self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def reconnect_node(self, node: str):
        """
        Re-enable any connections that may have previously been disabled.

        Args:
            node: the node to re-enable
        """
        base_connections = self.get_base_connected_nodes(node)
        for i in base_connections:
            if not self.current_network_variables[i]["isolated"]:
                self.current_graph.add_edge(node, i)
        self.current_network_variables[node]["isolated"] = False
        self.adj_matrix = self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def attack_node(
        self,
        node: str,
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
        if guarantee:
            # IF guaranteed then compromise the node
            self.current_network_variables[node]["true_compromised_status"] = 1
            self.immediate_attempt_view_update(node)
            return True

        # check if vulnerability and score are being used. If they are not then select a value
        if use_vulnerability:
            defence = 1 - self.current_network_variables[node]["vulnerability_score"]
        else:
            defence = 0
        if not use_skill:
            skill = 1

        # calculate the attack score, the higher the score the more likely the attack is to succeed
        attack_score = ((skill * skill) / (skill + defence)) * 100

        # check if the attack hits based on the attack score
        if attack_score > random.randint(0, 100):
            self.current_network_variables[node]["true_compromised_status"] = 1
            self.immediate_attempt_view_update(node)
            return True
        else:
            return False

    def make_node_safe(self, node: str):
        """
        Make the state for a given node safe.

        Args:
            node: the node to make safe
        """
        self.current_network_variables[node]["true_compromised_status"] = 0
        self.current_network_variables[node]["blue_view_compromised_status"] = 0
        if self.red_current_location == node:
            # If the red agent is in the node that just got made safe then the red agent needs to be pushed back
            self.push_red()
        self.current_network_variables[node]["blue_knows_intrusion"] = False

    def immediate_attempt_view_update(self, node: str):
        """
        Attempt to update the view of a specific node for the blue agent.

        There is a chance that intrusions will not be detected.

        Args:
            node: the node to try and update the view for
        """
        true_state = self.current_network_variables[node]["true_compromised_status"]
        if (
            self.current_network_variables[node]["blue_knows_intrusion"] is True
        ):  # if we have seen the intrusion before we don't want to forget about it
            self.current_network_variables[node][
                "blue_view_compromised_status"
            ] = true_state
        if true_state == 1:
            if (
                random.randint(0, 99)
                < self.settings["BLUE"]["chance_to_immediately_discover_intrusion"]
                * 100
                or node in self.deceptive_nodes
            ):
                self.current_network_variables[node][
                    "blue_view_compromised_status"
                ] = true_state
                # remember this intrusion so we don't forget about it
                self.current_network_variables[node]["blue_knows_intrusion"] = True

        else:
            self.current_network_variables[node][
                "blue_view_compromised_status"
            ] = true_state

    def immediate_attempt_view_update_with_specified_chance(
        self, node: str, chance: float
    ):
        """
        Update the blue view of a node but with a specified chance and not the chance used in the settings file.

        Args:
            node: The node to attempt to update
            chance: The chance blue has of updating the node and detecting a red intrusion
        """
        true_state = self.current_network_variables[node]["true_compromised_status"]
        if true_state == 1:
            if random.randint(0, 99) < chance * 100:
                self.current_network_variables[node][
                    "blue_view_compromised_status"
                ] = true_state
        else:
            self.current_network_variables[node][
                "blue_view_compromised_status"
            ] = true_state

    def scan_node(self, node: str) -> None:
        """
        Scan a target node to determine compromise based on the chance of discovery of compromise.

        Args:
            node: The node to be scanned
        """
        if self.current_network_variables[node]["blue_knows_intrusion"]:
            self.current_network_variables[node]["blue_view_compromised_status"] = 1
        else:
            true_state = self.current_network_variables[node]["true_compromised_status"]
            if true_state == 1:
                if (
                    random.randint(0, 99) < self.blue_scan_detection_chance * 100
                    or self.current_network_variables[node]["deceptive_node"]
                ):
                    self.current_network_variables[node]["blue_knows_intrusion"] = True
                    self.current_network_variables[node][
                        "blue_view_compromised_status"
                    ] = 1

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
