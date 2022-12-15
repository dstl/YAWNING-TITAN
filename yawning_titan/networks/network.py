from __future__ import annotations

import warnings
from enum import Enum
from logging import getLogger
from typing import Dict, Final, List, Optional, Union
from uuid import uuid4

import networkx

from yawning_titan.db.doc_metadata import DocMetadata

_LOGGER = getLogger(__name__)


class RandomHighValueNodePlacement(Enum):
    """How the random high value nodes are placed."""
    FURTHEST_AWAY_FROM_ENTRY = "furthest_away_from_entry"
    RANDOM = "random"


class RandomEntryNodePlacement(Enum):
    """How the random entry nodes are placed."""
    CENTRAL = "central"
    EDGE = "edge"


class Node:
    def __init__(
            self,
            uuid: Optional[str] = None,
            name: Optional[str] = None,
            high_value_node: bool = False,
            entry_node: bool = False,
            x_pos: float = 0.0,
            y_pos: float = 0.0,
            classes: Optional[str] = None
    ):
        if uuid is None:
            uuid = str(uuid4())
        self._uuid: Final[str] = uuid
        self._name: str = name
        self._high_value_node: bool = high_value_node
        self._entry_node: bool = entry_node
        self._x_pos: float = x_pos
        self._y_pos: float = y_pos
        self._classes = classes
        self._set_classes()

    def _set_classes(self):
        if self.high_value_node and self._entry_node:
            self._classes = "high_value_entry_node"
        else:
            if self.high_value_node:
                self._classes = "high_value_node"
            elif self.entry_node:
                self._classes = "entry_node"
            else:
                self._classes = "standard_node"

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def high_value_node(self) -> bool:
        return self._high_value_node

    @high_value_node.setter
    def high_value_node(self, high_value_node: bool):
        self._high_value_node = high_value_node
        self._set_classes()

    @property
    def entry_node(self) -> bool:
        return self._entry_node

    @entry_node.setter
    def entry_node(self, entry_node: bool):
        self._entry_node = entry_node
        self._set_classes()

    @property
    def x_pos(self) -> float:
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos: float):
        self._x_pos = x_pos

    @property
    def y_pos(self) -> float:
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos: float):
        self._y_pos = y_pos

    def to_dict(self):
        return {
            "uuid": self._uuid,
            "name": self._name,
            "high_value_node": self._high_value_node,
            "entry_node": self._entry_node,
            "classes": self._classes,
            "x_pos": self._x_pos,
            "y_pos": self._y_pos,
        }

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.uuid

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"uuid='{self._uuid}', "
            f"name='{self._name}', "
            f"high_value_node={self._high_value_node}, "
            f"entry_node={self._entry_node}, "
            f"x_pos={self._x_pos}, "
            f"y_pos={self._y_pos}"
            f")"
        )

    def __hash__(self):
        return hash((self._uuid, self._name, self._high_value_node, self._entry_node))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False


class Network(networkx.Graph):

    def __init__(
            self,
            set_random_entry_nodes: bool = False,
            random_entry_node_placement: RandomEntryNodePlacement = None,
            set_random_high_value_nodes: bool = False,
            random_high_value_node_placement: RandomHighValueNodePlacement = None,
            node_vulnerability_lower_bound: int = 0,
            node_vulnerability_upper_bound: int = 1,
            doc_metadata: Optional[DocMetadata] = None,
    ):
        super().__init__()
        self.set_random_entry_nodes = set_random_entry_nodes
        """If no entry nodes are added, set them at random. Default is ``False``."""
        self.random_entry_node_placement = random_entry_node_placement
        """The type of random entry node placement."""
        self.set_random_high_value_nodes = set_random_high_value_nodes
        """If no high value nodes are added, set them at random. Default is ``False``."""
        self.random_high_value_node_placement = random_high_value_node_placement
        """The type of random high value node placement."""
        self.node_vulnerability_lower_bound = node_vulnerability_lower_bound
        """A lower vulnerability means that a node is less likely to be compromised. Default value is 0."""
        self.node_vulnerability_upper_bound = node_vulnerability_upper_bound
        """A higher vulnerability means that a node is more vulnerable. Default value is 1."""
        self._uuid_node_map: Dict[str, Node] = {}
        self._doc_metadata = doc_metadata
        if self._doc_metadata is None:
            self._doc_metadata = DocMetadata()

    def add_node(self, node_for_adding: Node, **attr):
        super().add_node(node_for_adding.uuid, **node_for_adding.to_dict())
        self._uuid_node_map[node_for_adding.uuid] = node_for_adding
        self._check_intersect(node_for_adding)

    def remove_node(self, n: Node):
        super().remove_node(n.uuid)
        self._uuid_node_map.pop(n.uuid)
        self._uuid_node_map.pop(n.uuid)

    def get_node_from_uuid(self, uuid: str) -> Union[Node, None]:
        return self._uuid_node_map.get(uuid)

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, **kwargs):
        super().add_edge(u_of_edge.uuid, v_of_edge.uuid)

    def remove_edge(self, u: Node, v: Node):
        super().remove_edge(u.uuid, v.uuid)

    def _check_intersect(self, node: Node):
        if self.entry_nodes and self.high_value_nodes:
            uuids_intersect = set(self.entry_nodes) & set(self.high_value_nodes)
            if uuids_intersect:
                if node.uuid in uuids_intersect:
                    node_str = str(self._uuid_node_map[node.uuid])
                    warnings.warn(
                        f"Entry nodes and high value nodes intersect at node "
                        f"'{node_str}', and may cause the training to end "
                        f"prematurely."
                    )

    @property
    def high_value_nodes(self) -> List[str]:
        uuids = []
        for uuid, node in self._uuid_node_map.items():
            if node.high_value_node:
                uuids.append(uuid)
        return uuids

    @property
    def entry_nodes(self) -> List[str]:
        uuids = []
        for uuid, node in self._uuid_node_map.items():
            if node.entry_node:
                uuids.append(uuid)
        return uuids

    def to_dict(self):
        random_entry_node_placement = None
        if self.random_entry_node_placement:
            random_entry_node_placement = self.random_entry_node_placement.value

        random_high_value_node_placement = None
        if self.random_high_value_node_placement:
            random_high_value_node_placement = self.random_high_value_node_placement.value
        return {
            "set_random_entry_nodes": self.set_random_entry_nodes,
            "random_entry_node_placement": random_entry_node_placement,
            "set_random_high_value_nodes": self.set_random_high_value_nodes,
            "random_high_value_node_placement": random_high_value_node_placement,
            "node_vulnerability_lower_bound": self.node_vulnerability_lower_bound,
            "node_vulnerability_upper_bound": self.node_vulnerability_upper_bound,
            "nodes": super().__dict__["_node"],
            "edges": super().__dict__["_adj"],
            "_doc_metadata": self._doc_metadata.to_dict(include_none=False)
        }

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
        doc_metadata = DocMetadata(**network_dict["_doc_metadata"])
        network = Network(
            network_dict["set_random_entry_nodes"],
            network_dict["random_entry_node_placement"],
            network_dict["set_random_high_value_nodes"],
            network_dict["random_high_value_node_placement"],
            network_dict["node_vulnerability_lower_bound"],
            network_dict["node_vulnerability_upper_bound"],
            doc_metadata
        )
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
