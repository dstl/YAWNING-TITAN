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
from networkx.drawing.layout import (
    bipartite_layout,
    circular_layout,
    fruchterman_reingold_layout,
    kamada_kawai_layout,
    multipartite_layout,
    planar_layout,
    random_layout,
    rescale_layout,
    shell_layout,
    spectral_layout,
    spiral_layout,
    spring_layout,
)
from numpy.random import choice
from tabulate import tabulate

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.exceptions import NetworkError
from yawning_titan.networks.node import Node

_LOGGER = getLogger(__name__)


class NetworkLayout(Enum):
    """
    An enum class that maps to layout functions in networkx.drawing.layout.

    See: https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout
    """

    BIPARTITE = "bipartite"
    CIRCULAR = "circular"
    FRUCHTERMAN_REINGOLD = "fruchterman_reingold"
    KAMADA_KAWAI = "kamada_kawai"
    MULTIPARTITE = "multipartite"
    PLANAR = "planar"
    RANDOM = "random"
    RESCALE = "rescale"
    SHELL = "shell"
    SPECTRAL = "spectral"
    SPIRAL = "spiral"
    SPRING = "spring"

    def as_layout_func(self):
        """Maps the NetworkLayout to a function in networkx.drawing.layout."""
        layout_dict = {
            NetworkLayout.BIPARTITE: bipartite_layout,
            NetworkLayout.CIRCULAR: circular_layout,
            NetworkLayout.FRUCHTERMAN_REINGOLD: fruchterman_reingold_layout,
            NetworkLayout.KAMADA_KAWAI: kamada_kawai_layout,
            NetworkLayout.MULTIPARTITE: multipartite_layout,
            NetworkLayout.PLANAR: planar_layout,
            NetworkLayout.RANDOM: random_layout,
            NetworkLayout.RESCALE: rescale_layout,
            NetworkLayout.SHELL: shell_layout,
            NetworkLayout.SPECTRAL: spectral_layout,
            NetworkLayout.SPIRAL: spiral_layout,
            NetworkLayout.SPRING: spring_layout,
        }
        return layout_dict[self]


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
    """
    A Network that the NetworkInterface interacts with.

    Network extends networkx.Graph.

    Example:
        .. code::python


    """

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
        """
        The Network constructor.

        :param set_random_entry_nodes: Whether entry nodes are set at random
            if not set in nodes. Default value of False.
        :param random_entry_node_preference: The random entry node placement
            preference as an instance of
            yawning_titan.networks.network.RandomEntryNodePreference.
            Default value of RandomEntryNodePreference.NONE.
        :param num_of_random_entry_nodes: The number of random entry nodes
            that will be attempted to be set.
        :param set_random_high_value_nodes: Whether high value nodes are set
            at random if not set in nodes. Default value of False.
        :param random_high_value_node_preference: The random high value node
            placement preference as an instance of
            yawning_titan.networks.network.RandomHighValueNodePreference.
            Default value of RandomHighValueNodePreference.NONE.
        :param num_of_random_high_value_nodes: The number of random high value
            nodes that will be attempted to be set.
        :param set_random_vulnerabilities: Whether node vulnerability scores
            are set at random.
        :param node_vulnerability_lower_bound: The lower-bound of a nodes
            vulnerability score. Default value of 0.01.
        :param node_vulnerability_upper_bound: The upper-bound of a nodes
            vulnerability score. Default value of 0.01.
        """
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
    def num_possible_high_value_nodes(self) -> int:
        """Maximum number of allowed high value nodes in the network.

        Number of possible high value nodes calculated by seeing how many nodes there are minus the entry
        nodes, then only having 15% of the nodes left over to be high value nodes.
        """
        return math.ceil((len(self.nodes) - len(self.entry_nodes) + 1) * 0.15)

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
            # self.set_node_positions()

    def remove_node(self, n: Node):
        """
        Remove a node from the network.

        Extend the `remove_node` method of the superclass.
        """
        super().remove_node(n)
        # self.set_node_positions()

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, **kwargs):
        """
        Add an edge between 2 nodes in the network.

        Extend the `add_edge` method of the superclass.
        """
        super().add_edge(u_of_edge, v_of_edge, **kwargs)
        # self.set_node_positions()

    def remove_edge(self, u: Node, v: Node):
        """
        Remove an edge between 2 nodes in the network.

        Extend the `remove_edge` method of the superclass.
        """
        super().remove_edge(u, v)

    def reset(self):
        """
        Resets the network.

        This is done by calling:

        - reset_random_entry_nodes()
        - reset_random_high_value_nodes
        - reset_random_vulnerabilities()
        """
        if self.set_random_entry_nodes:
            self.reset_random_entry_nodes()
        if self.set_random_high_value_nodes:
            self.reset_random_high_value_nodes()
        if self.set_random_vulnerabilities:
            self.reset_random_vulnerabilities()

    def show(self, verbose=False):
        """
        Show details of all Nodes in the Network.

        :param verbose: If True, all Node attributes are shown, otherwise
            just the uuid is shown.
        """
        rows = []
        headers = [
            "UUID",
            "Name",
            "High Value Node",
            "Entry Node",
            "Vulnerability",
            "Position (x,y)",
        ]
        keys = [
            "uuid",
            "name",
            "high_value_node",
            "entry_node",
            "vulnerability",
            "position",
        ]

        for node in self.nodes:
            node_dict = node.to_dict()
            node_dict["position"] = f"{node.x_pos:.2f}, {node.y_pos:.2f}"
            d = {key: node_dict[key] for key in keys}
            row = list(d.values())
            if not verbose:
                row = [row[0]]
            rows.append(row)

        print(tabulate([headers] + rows, headers="firstrow"))

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
        as_list: bool = False,
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

        if key_by_name:
            return {n.name: n for n in nodes}

        if as_list:
            return list(nodes)

        return nodes

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

    def set_from_dict(
        self,
        config_dict: dict,
        remove_existing_edges: bool = False,
        remove_existing_nodes: bool = False,
        clear_special_nodes: bool = True,
    ):
        """Set the values of existing network attributes from those contained in a dictionary.

        :param config_dict: A dictionary of network attribute name value pairs
        :param remove_existing_edges: Whether to remove existing edges
        :param remove_existing_nodes: Whether to remove existing nodes
        """
        if clear_special_nodes:
            self.clear_special_nodes()

        if "_doc_metadata" in config_dict:
            config_dict["_doc_metadata"] = DocMetadata(
                **config_dict.pop("_doc_metadata")
            )
        if "random_entry_node_preference" in config_dict:
            config_dict["random_entry_node_preference"] = RandomEntryNodePreference[
                config_dict["random_entry_node_preference"]
            ]
        if "random_high_value_node_preference" in config_dict:
            config_dict[
                "random_high_value_node_preference"
            ] = RandomHighValueNodePreference[
                config_dict["random_high_value_node_preference"]
            ]
        if "nodes" in config_dict:
            self.add_nodes_from_dict(
                nodes_dict=config_dict.pop("nodes"),
                remove_existing=remove_existing_nodes,
            )
        if "edges" in config_dict:
            self.add_edges_from_dict(
                edges_dict=config_dict.pop("edges"),
                remove_existing=remove_existing_edges,
            )

        # self.set_node_positions()

        for k, v in config_dict.items():
            if hasattr(self, k):
                setattr(self, k, v)

        if self.set_random_entry_nodes:
            self.reset_random_entry_nodes()

        if self.set_random_high_value_nodes:
            self.reset_random_high_value_nodes()

        if self.set_random_vulnerabilities:
            self.reset_random_vulnerabilities()

    def clear_special_nodes(self):
        """Remove all special node designations."""
        for node in self.entry_nodes:
            node.entry_node = False
        for node in self.high_value_nodes:
            node.high_value_node = False

    def set_node_positions(self, network_layout: NetworkLayout = NetworkLayout.SPRING):
        """
        Sets the Node positions of the current Network.

        :param network_layout: A member of NetworkLayout. Default is
            NetworkLayout.SPRING.
        """
        pos_dict = network_layout.as_layout_func()(self)
        for node in self.nodes:
            node.node_position = pos_dict[node]

    def add_nodes_from_dict(self, nodes_dict: Dict[str, dict], remove_existing=False):
        """Add nodes to the graph with properties defined from a dictionary.

        :param nodes_dict: a dictionary of node uuids to properties
        :param remove_existing: a boolean to indicate whether to remove existing nodes
        """
        if remove_existing:
            for n in self.nodes:
                self.remove_node(n)
        for uuid, attrs in nodes_dict.items():
            self.add_node(Node.create_from_db(**attrs))

    def add_edges_from_dict(self, edges_dict: Dict[str, dict], remove_existing=False):
        """Add edges to the graph with properties defined from a dictionary.

        :param edges_dict: a dictionary of edge uuids to properties
        :param remove_existing: a boolean to indicate whether to remove existing edges
        """
        edge_tuples = []
        if remove_existing:
            for e in self.edges:
                self.remove_edge(e)
        for uuid_u, edges in edges_dict.items():
            for uuid_v in edges.keys():
                edge_tuple = tuple(sorted([uuid_u, uuid_v]))
                if edge_tuple not in edge_tuples:
                    edge_tuples.append(edge_tuple)
                    node_u = self.get_node_from_uuid(edge_tuple[0])
                    node_v = self.get_node_from_uuid(edge_tuple[1])
                    self.add_edge(node_u, node_v)

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
        if not self.entry_nodes:
            msg = "Cannot set random high value nodes before setting entry nodes."
            _LOGGER.error(msg, exc_info=True)
            raise NetworkError(msg)

        # print warning that the number of high value nodes exceed the above preferably this would be handled
        # elsewhere i.e. configuration.
        if self.num_of_random_high_value_nodes > self.num_possible_high_value_nodes:
            msg = (
                f"The configured number of high value nodes exceed the allowable number in the given "
                f"networks. {str(self.num_possible_high_value_nodes)} high value nodes will be created."
            )
            warnings.warn(UserWarning(msg))
            number_of_high_value_nodes = self.num_possible_high_value_nodes
        elif self.num_of_random_high_value_nodes <= 0:
            msg = (
                f"The configured number of high value nodes, {self.num_of_random_high_value_nodes}, "
                f"must be greater than 0. {str(self.num_possible_high_value_nodes)} high value nodes will be created."
            )
            warnings.warn(UserWarning(msg))
            number_of_high_value_nodes = self.num_possible_high_value_nodes
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
            for _ in range(self.num_possible_high_value_nodes):
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

        if len(possible_high_value_nodes) < number_of_high_value_nodes:
            number_of_high_value_nodes = len(possible_high_value_nodes)
            msg = (
                f"The configured number of high value nodes, {self.num_of_random_high_value_nodes}, "
                f"cannot be created with the chosen method. Instead {str(self.num_possible_high_value_nodes)} high value nodes will be created."
            )
            warnings.warn(UserWarning(msg))

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
        network = Network()
        network.set_from_dict(network_dict)
        return network

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.doc_metadata.uuid == other.doc_metadata.uuid
        return False

    def __hash__(self):
        return hash(self.doc_metadata.uuid)

    def __repr__(self):
        net_str = (
            f"{self.__class__.__name__}("
            f"uuid='{self.doc_metadata.uuid}', "
            f"nodes={len(self.nodes)}, "
        )

        if self.doc_metadata.name:
            net_str += f"name='{self.doc_metadata.name}', "
        if self.doc_metadata.author:
            net_str += f"author='{self.doc_metadata.author}', "
        net_str += f"locked={self.doc_metadata.locked})"

        return net_str

    def __str__(self):
        return repr(self)
