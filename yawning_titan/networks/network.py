from __future__ import annotations

import math
import random
import warnings
from collections import Counter
from enum import Enum
from logging import getLogger
from random import sample
from typing import Any, Dict, List, Optional, Tuple, Union

import networkx as nx
import numpy
from numpy.random import choice

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.networks.node import Node

_LOGGER = getLogger(__name__)

# --- Tier 0 groups


class RandomHighValueNodePreference(Enum):
    """Preference of how the random high value nodes are placed."""

    FURTHEST_AWAY_FROM_ENTRY = "FURTHEST_AWAY_FROM_ENTRY"
    """Prefer nodes furthest away from entry nodes."""
    NONE = "NONE"
    """No preference."""


class RandomEntryNodePreference(Enum):
    """Preference of hw the random entry nodes are placed."""

    CENTRAL = "CENTRAL"
    """Prefer central nodes."""
    EDGE = "EDGE"
    """Prefer edge nodes."""
    NONE = "NONE"
    """No preference."""


class Network(nx.Graph):
    """A representation of a network in YawningTitan."""

    def __init__(
        self,
        set_random_entry_nodes: bool = False,
        random_entry_node_preference: RandomEntryNodePreference = RandomEntryNodePreference.NONE,
        num_of_random_entry_nodes: int = 0,
        set_random_high_value_nodes: bool = False,
        random_high_value_node_preference: RandomHighValueNodePreference = RandomHighValueNodePreference.NONE,
        num_of_random_high_value_nodes: int = 0,
        set_random_vulnerabilities: bool = False,
        node_vulnerability_lower_bound: float = 0.01,
        node_vulnerability_upper_bound: float = 1,
        doc_metadata: Optional[DocMetadata] = None,
        **kwargs,
    ):
        """Extend networkx.Graph with a series of attributes required to represent a YawningTitan network using a series of :class: `~yawning_titan.networks.node.Node` objects."""
        super().__init__()
        self.set_random_entry_nodes = set_random_entry_nodes
        """If no entry nodes are added, set them at random. Default is ``False``."""
        self.random_entry_node_preference = random_entry_node_preference
        """The type of random entry node preference."""
        self.num_of_random_entry_nodes = num_of_random_entry_nodes
        """The number of random entry nodes to be generated."""
        self.set_random_high_value_nodes = set_random_high_value_nodes
        """If no high value nodes are added, set them at random. Default is ``False``."""
        self.random_high_value_node_preference = random_high_value_node_preference
        """The type of random high value node preference."""
        self.num_of_random_high_value_nodes = num_of_random_high_value_nodes
        """The number of random high_value nodes to be generated."""
        self.set_random_vulnerabilities = set_random_vulnerabilities
        """If True, random vulnerability is set for each node using the upper and lower bounds."""
        self.node_vulnerability_lower_bound = node_vulnerability_lower_bound
        """A lower vulnerability means that a node is less likely to be compromised. Default value is 0."""
        self.node_vulnerability_upper_bound = node_vulnerability_upper_bound
        """A higher vulnerability means that a node is more vulnerable. Default value is 1."""
        self._doc_metadata = doc_metadata

        self.nodes: List[Node]
        """Access the `nodes` property from the superclass which has `list` properties but is a `NodeView` instance"""

        if self._doc_metadata is None:
            self._doc_metadata = DocMetadata()

    @property
    def high_value_nodes(self) -> List[Node]:
        """A list of the high value nodes in the network."""
        return [n for n in self.nodes if n.high_value_node]

    @property
    def entry_nodes(self) -> List[Node]:
        """A list of the entry nodes in the network."""
        return [n for n in self.nodes if n.entry_node]

    @property
    def deceptive_nodes(self) -> List[Node]:
        """A list of the deceptive nodes in the network."""
        return [n for n in self.nodes if n.deceptive_node]

    @property
    def node_vulnerability_lower_bound(self) -> float:
        """The minimum value that a node within the networks vulnerability can take."""
        return self._node_vulnerability_lower_bound

    @property
    def doc_metadata(self) -> DocMetadata:
        """The configs document metadata."""
        return self._doc_metadata

    @node_vulnerability_lower_bound.setter
    def node_vulnerability_lower_bound(self, x: float):
        if x is None or x <= 0:
            msg = "Node vulnerability lower bound must be above 0."
            _LOGGER.error(msg, exc_info=True)
            raise ValueError(msg)
        self._node_vulnerability_lower_bound = x

    @doc_metadata.setter
    def doc_metadata(self, doc_metadata: DocMetadata):
        if self._doc_metadata is None:
            self._doc_metadata = doc_metadata
        else:
            msg = "Cannot set _doc_metadata as it has already been set."
            _LOGGER.error(msg)

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
        key_by_name: bool = False,
    ) -> Union[List[Node], Dict[str, Node]]:
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
        nodes = self.nodes
        if filter_true_compromised:
            # Return true if compromised status is 1
            nodes = [n for n in nodes if n.true_compromised_status == 1]
        if filter_blue_view_compromised:
            # Return True if blue view compromised status is 1
            nodes = [n for n in nodes if n.blue_view_compromised_status == 1]
        if filter_true_safe:
            # Return True if compromised status is 0
            nodes = [n for n in nodes if n.true_compromised_status == 0]
        if filter_blue_view_safe:
            # Return True if blue view compromised status is 0
            nodes = [n for n in nodes if n.blue_view_compromised_status == 0]
        if filter_isolated:
            # Return True if isolated is True
            nodes = [n for n in nodes if n.isolated]
        if filter_non_isolated:
            # Return True if isolated is False
            nodes = [n for n in nodes if not n.isolated]
        if filter_deceptive:
            # Return True if deceptive node is True
            nodes = [n for n in nodes if n.deceptive_node]
        if filter_non_deceptive:
            # Return True if deceptive node is False
            nodes = [n for n in nodes if not n.deceptive_node]

        if not key_by_name:
            return nodes

        return {n.name: n for n in nodes}

    def get_node_from_uuid(self, uuid: str) -> Union[Node, None]:
        """Return the first node that has a given uuid."""
        for node in self.nodes:
            if node.uuid == uuid:
                return node
        return None

    def get_node_from_name(self, name: str) -> Union[Node, None]:
        """Return the first node that has a given name."""
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def _generate_random_vulnerability(self) -> float:
        """
        Generate a single random vulnerability value from the lower and upper bounds.

        :returns: A single float representing a vulnerability.
        """
        return random.uniform(
            self.node_vulnerability_lower_bound, self.node_vulnerability_upper_bound
        )

    def _check_intersect(self, node: Node):
        """Check that high value nodes and entry nodes do not overlap."""
        if self.entry_nodes and self.high_value_nodes:
            uuids_intersect = [
                n.uuid for n in set(self.entry_nodes) & set(self.high_value_nodes)
            ]
            if uuids_intersect:
                if node.uuid in uuids_intersect:
                    node_str = str(node)
                    warnings.warn(
                        UserWarning(
                            f"Entry nodes and high value nodes intersect at node "
                            f"'{node_str}', and may cause the training to end "
                            f"prematurely."
                        )
                    )

    def add_node(self, node_for_adding: Node, **kwargs):
        """
        Add a node to the network.

        Extend the `add_node` method of the superclass.

        if the `node_for_adding` is a special node then check that there are no intersections between hvn and entry_node's.
        """
        if node_for_adding not in self.nodes:
            super().add_node(node_for_adding, **kwargs)
            if node_for_adding.entry_node or node_for_adding.high_value_node:
                self._check_intersect(node_for_adding)

    def remove_node(self, n: Node):
        """
        Remove a node from the network.

        Extend the `remove_node` method of the superclass.
        """
        super().remove_node(n)

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, **kwargs):
        """
        Add an edge between 2 nodes in the network.

        Extend the `add_edge` method of the superclass.
        """
        super().add_edge(u_of_edge, v_of_edge, **kwargs)

    def remove_edge(self, u: Node, v: Node):
        """
        Remove an edge between 2 nodes in the network.

        Extend the `remove_edge` method of the superclass.
        """
        super().remove_edge(u, v)

    def reset_random_entry_nodes(self):
        """
        Set the entry nodes.

        If no entry nodes supplied then the first node in the network is chosen as the initial node.
        """
        try:
            node_dict = nx.algorithms.centrality.eigenvector_centrality(
                self, max_iter=500
            )
        except nx.PowerIterationFailedConvergence as e:
            _LOGGER.debug(e)
            node_dict = {node: 0.5 for node in self.nodes()}
        weights = list(node_dict.values())
        all_nodes = list(node_dict.keys())

        if self.random_entry_node_preference == RandomEntryNodePreference.EDGE:
            weights = list(map(lambda x: (1 / x) ** 4, weights))
        elif self.random_entry_node_preference == RandomEntryNodePreference.CENTRAL:
            weights = list(map(lambda x: x**4, weights))
        elif self.random_entry_node_preference == RandomEntryNodePreference.NONE:
            weights = [1] * len(all_nodes)

        weights_normal = [float(i) / sum(weights) for i in weights]

        entry_nodes = choice(
            all_nodes,
            self.num_of_random_entry_nodes,
            replace=False,
            p=weights_normal,
        )

        for node in self.nodes:
            if node in entry_nodes:
                node.entry_node = True
            else:
                node.entry_node = False
            self._check_intersect(node)

    def reset_random_high_value_nodes(self):
        """
        Sets up the high value nodes (HVNs) to be used by the training environment.

        If HVNs are supplied in the `Network`, they are used. However, if they are not supplied, the following
        logic is applied:
            If game_mode.game_rules.lose_when_high_value_node_lost is True:
                An acceptable amount (math.ceil((len(current_graph.nodes) - len(entry_nodes) + 1) * 0.15) of
                HVNs are defined from a list of potential HVSn at random after steps are taken to ensure that HVNs are
                not entry nodes.
            Otherwise:
                HVNs are set to an empty list.
        """
        # if no high value nodes set, set up the possible high value node list

        # number of possible high value nodes calculated by seeing how many nodes there are minus the entry
        # nodes, then only having 15% of the nodes left over to be high value nodes.
        number_possible_high_value = math.ceil(
            (len(self.nodes) - len(self.entry_nodes) + 1) * 0.15
        )
        # print warning that the number of high value nodes exceed the above preferably this would be handled
        # elsewhere i.e. configuration.
        if self.num_of_random_high_value_nodes > number_possible_high_value:
            msg = (
                f"The configured number of high value nodes exceed the allowable number in the given "
                f"networks. {str(number_possible_high_value)} high value nodes will be created."
            )
            warnings.warn(UserWarning(msg))
            number_of_high_value_nodes = number_possible_high_value
        elif self.num_of_random_high_value_nodes <= 0:
            msg = (
                f"The configured number of high value nodes, {self.num_of_random_high_value_nodes}, "
                f"must be greater than 0. {str(number_possible_high_value)} high value nodes will be created."
            )
            warnings.warn(UserWarning(msg))
            number_of_high_value_nodes = number_possible_high_value
        else:
            number_of_high_value_nodes = self.num_of_random_high_value_nodes

        possible_high_value_nodes = []
        # chooses a random node to be the high value node
        if self.random_high_value_node_preference == RandomHighValueNodePreference.NONE:
            possible_high_value_nodes = list(
                set(self.nodes).difference(set(self.entry_nodes))
            )
        # Choose the node that is the furthest away from the entry points as the high value node
        elif (
            self.random_high_value_node_preference.FURTHEST_AWAY_FROM_ENTRY
            == RandomHighValueNodePreference.FURTHEST_AWAY_FROM_ENTRY
        ):
            # gets all the paths between nodes
            paths = []
            for n in self.entry_nodes:
                paths.append(dict(nx.all_pairs_shortest_path_length(self))[n])
            sums = Counter()
            counters = Counter()
            # gets the distances to the entry points
            for itemset in paths:
                sums.update(itemset)
                counters.update(itemset.keys())
            # averages the distances to find the node that is, on average, the furthest away
            result = {x: float(sums[x]) / counters[x] for x in sums.keys()}
            for _ in range(number_possible_high_value):
                current = max(result, key=result.get)
                possible_high_value_nodes.append(current)
                result.pop(current)

            # prevent high value nodes from becoming entry nodes
            possible_high_value_nodes = list(
                set(possible_high_value_nodes).difference(self.entry_nodes)
            )
        # randomly pick unique nodes from a list of possible high value nodes

        if (
            possible_high_value_nodes is None
        ):  # If there are none possible then try again
            self.reset_random_high_value_nodes()

        high_value_nodes = sample(
            set(possible_high_value_nodes),
            number_of_high_value_nodes,
        )
        for node in self.nodes:
            if node in high_value_nodes:
                node.high_value_node = True
            else:
                node.high_value_node = False
            self._check_intersect(node)

    def reset_random_vulnerabilities(self):
        """Regenerate random vulnerabilities for every node in the network."""
        if self.set_random_vulnerabilities:
            for node in self.nodes:
                node.vulnerability = self._generate_random_vulnerability()

    def to_dict(self, json_serializable: bool = False) -> Dict[str, Any]:
        """Represent the `Network` as a dictionary."""
        random_entry_node_preference = None
        if self.random_entry_node_preference:
            random_entry_node_preference = self.random_entry_node_preference.value

        random_high_value_node_preference = None
        if self.random_high_value_node_preference:
            random_high_value_node_preference = (
                self.random_high_value_node_preference.value
            )
        d = {
            "set_random_entry_nodes": self.set_random_entry_nodes,
            "random_entry_node_preference": random_entry_node_preference,
            "num_of_random_entry_nodes": self.num_of_random_entry_nodes,
            "set_random_high_value_nodes": self.set_random_high_value_nodes,
            "random_high_value_node_preference": random_high_value_node_preference,
            "num_of_random_high_value_nodes": self.num_of_random_high_value_nodes,
            "set_random_vulnerabilities": self.set_random_vulnerabilities,
            "node_vulnerability_lower_bound": self.node_vulnerability_lower_bound,
            "node_vulnerability_upper_bound": self.node_vulnerability_upper_bound,
            "nodes": self.__dict__["_node"],
            "edges": self.__dict__["_adj"],
            "_doc_metadata": self.doc_metadata,
        }
        if json_serializable:
            d["nodes"] = {k.uuid: k.to_dict() for k in d["nodes"].keys()}
            d["edges"] = {
                k.uuid: {node.uuid: attrs for node, attrs in v.items()}
                for k, v in d["edges"].items()
            }
            d["_doc_metadata"] = d["_doc_metadata"].to_dict()
        return d

    def to_adj_matrix_and_positions(self) -> Tuple[numpy.array, Dict[str, List[float]]]:
        """Represent the network by its adjacency matrix and a dictionary of node names to positions."""
        return nx.to_numpy_array(self), {n.name: n.node_position for n in self.nodes}

    @classmethod
    def create(cls, network_dict: dict) -> Network:
        """
        Create an instance on :class: `Network` from a dictionary.

        :param network_dict: a dictionary describing a :class:`Network`
        :return: An instance of :class: `Network`.
        """
        network_dict["doc_metadata"] = DocMetadata(**network_dict.pop("_doc_metadata"))
        network_dict["random_entry_node_preference"] = RandomEntryNodePreference[
            network_dict["random_entry_node_preference"]
        ]
        network_dict[
            "random_high_value_node_preference"
        ] = RandomHighValueNodePreference[
            network_dict["random_high_value_node_preference"]
        ]
        network = Network(**network_dict)
        for uuid, attrs in network_dict["nodes"].items():
            network.add_node(Node(**attrs))

        edge_tuples = []
        for uuid_u, edges in network_dict["edges"].items():
            for uuid_v in edges.keys():
                edge_tuple = tuple(sorted([uuid_u, uuid_v]))
                if edge_tuple not in edge_tuples:
                    edge_tuples.append(edge_tuple)
                    node_u = network.get_node_from_uuid(edge_tuple[0])
                    node_v = network.get_node_from_uuid(edge_tuple[1])
                    network.add_edge(node_u, node_v)

        return network
