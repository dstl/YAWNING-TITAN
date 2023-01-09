from __future__ import annotations

import math
import random
import warnings
from collections import Counter
from enum import Enum
from logging import getLogger
from random import randint, sample
from typing import Counter, List, Optional, Union

import networkx as nx
from numpy.random import choice

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.networks.node import Node

_LOGGER = getLogger(__name__)


class RandomHighValueNodePreference(Enum):
    """Preference of how the random high value nodes are placed."""

    FURTHEST_AWAY_FROM_ENTRY = "furthest_away_from_entry"
    """Prefer nodes furthest away from entry nodes."""
    NONE = "none"
    """No preference."""


class RandomEntryNodePreference(Enum):
    """Preference of hw the random entry nodes are placed."""

    CENTRAL = "central"
    """Prefer central nodes."""
    EDGE = "edge"
    """Prefer edge nodes."""
    NONE = "none"
    """No preference."""


class Network(nx.Graph):
    def __init__(
        self,
        set_random_entry_nodes: bool = False,
        random_entry_node_preference: RandomEntryNodePreference = RandomEntryNodePreference.NONE,
        num_of_random_entry_nodes: int = 0,
        set_random_high_value_nodes: bool = False,
        random_high_value_node_preference: RandomHighValueNodePreference = RandomHighValueNodePreference.NONE,
        num_of_random_high_value_nodes: int = 0,
        set_random_vulnerabilities: bool = False,
        node_vulnerability_lower_bound: int = 0,
        node_vulnerability_upper_bound: int = 1,
        doc_metadata: Optional[DocMetadata] = None,
    ):
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

        if self._doc_metadata is None:
            self._doc_metadata = DocMetadata()

    def add_node(self, node_for_adding: Node, **kwargs):
        if node_for_adding not in self.nodes:
            super().add_node(node_for_adding, **kwargs)
            self._check_intersect(node_for_adding)

    def remove_node(self, n: Node):
        super().remove_node(n)

    def get_node_from_uuid(self, uuid: str) -> Union[Node, None]:
        for node in self.nodes:
            if node.uuid == uuid:
                return node
        return None

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, **kwargs):
        super().add_edge(u_of_edge, v_of_edge, **kwargs)

    def remove_edge(self, u: Node, v: Node):
        super().remove_edge(u, v)

    def _check_intersect(self, node: Node):
        if self.entry_nodes and self.high_value_nodes:
            uuids_intersect = set(self.entry_nodes) & set(self.high_value_nodes)
            if uuids_intersect:
                if node.uuid in uuids_intersect:
                    node_str = str(node)
                    warnings.warn(
                        f"Entry nodes and high value nodes intersect at node "
                        f"'{node_str}', and may cause the training to end "
                        f"prematurely."
                    )

    @property
    def high_value_nodes(self) -> List[Node]:
        nodes = []
        for node in self.nodes:
            if node.high_value_node:
                nodes.append(node)
        return nodes

    @property
    def entry_nodes(self) -> List[Node]:
        nodes = []
        for node in self.nodes:
            if node.entry_node:
                nodes.append(node)
        return nodes

    def reset_random_entry_nodes(self):
        """
        Set the entry nodes.

        If no entry nodes supplied then the first node in the network is chosen as the initial node.
        """
        entry_node_weights = [
            1 / self.number_of_nodes() for _ in range(self.number_of_nodes())
        ]  # TODO: Is this needed anywhere?
        if not self.entry_nodes:
            if self.set_random_entry_nodes:
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
                elif (
                    self.random_entry_node_preference
                    == RandomEntryNodePreference.CENTRAL
                ):
                    weights = list(map(lambda x: x**4, weights))
                elif (
                    self.random_entry_node_preference == RandomEntryNodePreference.NONE
                ):
                    weights = [1] * len(all_nodes)

                weights_normal = [float(i) / sum(weights) for i in weights]

                entry_nodes = choice(
                    all_nodes,
                    self.num_of_random_entry_nodes,
                    replace=False,
                    p=weights_normal,
                )

                for node in entry_nodes:
                    node.entry_node = True

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
        if not self.high_value_nodes:

            # if no high value nodes set, set up the possible high value node list
            if self.set_random_high_value_nodes:
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
                    warnings.warn(msg)
                    number_of_high_value_nodes = number_possible_high_value
                elif self.num_of_random_high_value_nodes <= 0:
                    msg = (
                        f"The configured number of high value nodes, {self.num_of_random_high_value_nodes}, "
                        f"must be greater than 0. {str(number_possible_high_value)} high value nodes will be created."
                    )
                    warnings.warn(msg)
                    number_of_high_value_nodes = number_possible_high_value
                possible_high_value_nodes = []
                # chooses a random node to be the high value node
                if (
                    self.random_high_value_node_preference
                    == RandomHighValueNodePreference.NONE
                ):
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
                    for i in self.entry_nodes:
                        paths.append(
                            dict(nx.all_pairs_shortest_path_length(self.graph))[i]
                        )
                    print(paths)
                    sums = Counter()
                    counters = Counter()
                    # gets the distances to the entry points
                    for itemset in paths:
                        sums.update(itemset)
                        counters.update(itemset.keys())
                    # averages the distances to find the node that is, on average, the furthest away
                    result = {x: float(sums[x]) / counters[x] for x in sums.keys()}
                    print(result)
                    for i in range(number_possible_high_value):
                        current = max(result, key=result.get)
                        possible_high_value_nodes.append(current)
                        result.pop(current)

                    # prevent high value nodes from becoming entry nodes
                    possible_high_value_nodes = list(
                        set(possible_high_value_nodes).difference(self.entry_nodes)
                    )
                # randomly pick unique nodes from a list of possible high value nodes
                high_value_nodes = sample(
                    set(possible_high_value_nodes),
                    number_of_high_value_nodes,
                )
                for node in high_value_nodes:
                    node.high_value_node = True

    def _generate_random_vulnerability(self) -> float:
        """
        Generate a single random vulnerability value from the lower and upper bounds.

        :returns: A single float representing a vulnerability.
        """
        return random.uniform(
            self.node_vulnerability_lower_bound, self.node_vulnerability_upper_bound
        )

    def reset_random_vulnerabilities(self):
        if self.set_random_vulnerabilities:
            for node in self.nodes:
                node.vulnerability = self._generate_random_vulnerability()

    def to_dict(self):
        random_entry_node_preference = None
        if self.random_entry_node_preference:
            random_entry_node_preference = self.random_entry_node_preference.value

        random_high_value_node_preference = None
        if self.random_high_value_node_preference:
            random_high_value_node_preference = (
                self.random_high_value_node_preference.value
            )
        return {
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
            "_doc_metadata": self._doc_metadata,
        }

    def to_json(self):
        d = self.to_dict()
        d["nodes"] = {k.uuid: k.to_dict() for k, v in d["nodes"].items()}
        d["edges"] = {
            k.uuid: {node.uuid: attrs for node, attrs in v.items()}
            for k, v in d["edges"].items()
        }
        d["_doc_metadata"] = d["_doc_metadata"].to_dict()
        return d

    @property
    def doc_metadata(self) -> DocMetadata:
        """The configs document metadata."""
        return self._doc_metadata

    @doc_metadata.setter
    def doc_metadata(self, doc_metadata: DocMetadata):
        if self._doc_metadata is None:
            self._doc_metadata = doc_metadata
        else:
            msg = "Cannot set _doc_metadata as it has already been set."
            _LOGGER.error(msg)

    @classmethod
    def create(cls, network_dict) -> Network:
        network = Network()
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
