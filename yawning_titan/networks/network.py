from __future__ import annotations

import warnings
from logging import getLogger
from typing import Final, List, Optional
from uuid import uuid4

import networkx
import networkx as nx
from networkx import Graph
from networkx.classes.reportviews import EdgeView, NodeView

from yawning_titan.db.doc_metadata import DocMetadata

_LOGGER = getLogger(__name__)


class Node:
    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        high_value_node: bool = False,
        entry_node: bool = False,
        x_pos: float = 0.0,
        y_pos: float = 0.0,
    ):
        if uuid is None:
            uuid = str(uuid4())
        self._uuid: Final[str] = uuid
        self._name: str = name
        self._high_value_node: bool = high_value_node
        self._entry_node: bool = entry_node
        self._x_pos: float = x_pos
        self._y_pos: float = y_pos
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

    @x_pos.setter
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
    def __init__(self, doc_metadata: Optional[DocMetadata] = None, **attr):
        super().__init__(**attr)
        self._uuid_node_map: Dict[str, None] = {}
        self._doc_metadata = doc_metadata
        if self._doc_metadata is None:
            self._doc_metadata = DocMetadata()

    def add_node(self, node: Node):
        super().add_node(node.uuid, **node.to_dict())
        self._uuid_node_map[node.uuid] = node
        self._validate(node)

    def remove_node(self, node: Node):
        super().remove_node(node.uuid)
        self._uuid_node_map.pop(node.uuid)

    def add_edge(self, node_a: Node, node_b: Node):
        super().add_edge(node_a.uuid, node_b.uuid)

    def remove_edge(self, node_a: Node, node_b: Node):
        super().remove_edge(node_a.uuid, node_b.uuid)

    def _validate(self, node: Node):

        # check that no entry nodes and high value nodes intersect
        if self.entry_nodes and self.high_value_nodes:
            uuids_intersect = set(self.entry_nodes) & set(self.high_value_nodes)
            if uuids_intersect:
                if node.uuid in uuids_intersect:
                    node_str = str(self._uuid_node_map[node.uuid])
                    warnings.warn(
                        f"Entry nodes and high value nodes intersect at node {node_str} and may cause the training to prematurely end."
                    )

    @property
    def high_value_nodes(self) -> List[str]:
        uuids = []
        for uuid, node in super().__dict__["_node"].items():
            if node["high_value_node"]:
                uuids.append(uuid)
        return uuids

    @property
    def entry_nodes(self) -> List[str]:
        uuids = []
        for uuid, node in super().__dict__["_node"].items():
            if node["entry_node"]:
                uuids.append(uuid)
        return uuids

    def to_dict(self):
        d = {}
        d["nodes"] = super().__dict__["_node"]
        d["edges"] = super().__dict__["_adj"]
        d["_doc_metadata"] = self._doc_metadata.to_dict(True)
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


router_1 = Node(name="Router 1", high_value_node=False, entry_node=True)

switch_1 = Node(name="Switch 1", high_value_node=False, entry_node=False)
switch_2 = Node(name="Switch 2", high_value_node=True, entry_node=False)

pc_1 = Node(name="PC 1", high_value_node=False, entry_node=False)
pc_2 = Node(name="PC 2", high_value_node=True, entry_node=False)
pc_3 = Node(name="PC 3", high_value_node=True, entry_node=True)
pc_4 = Node(name="PC 4", high_value_node=True, entry_node=False)
pc_5 = Node(name="PC 5", high_value_node=True, entry_node=False)
pc_6 = Node(name="PC 6", high_value_node=True, entry_node=False)

server_1 = Node(name="Server 1", high_value_node=False, entry_node=False)
server_2 = Node(name="Server 2", high_value_node=True, entry_node=False)

graph = Network()

graph.add_node(router_1)
graph.add_node(switch_1)
graph.add_node(switch_2)

graph.add_node(pc_1)
graph.add_node(pc_2)
graph.add_node(pc_3)
graph.add_node(pc_4)
graph.add_node(pc_5)
graph.add_node(pc_6)
graph.add_node(server_1)
graph.add_node(server_2)

graph.add_edge(router_1, switch_1)
graph.add_edge(switch_1, server_1)
graph.add_edge(switch_1, pc_1)
graph.add_edge(switch_1, pc_2)
graph.add_edge(switch_1, pc_3)
graph.add_edge(router_1, switch_2)
graph.add_edge(switch_2, server_2)
graph.add_edge(switch_2, pc_4)
graph.add_edge(switch_2, pc_5)
graph.add_edge(switch_2, pc_6)

print(graph.nodes)
print(graph.edges)
print(graph.to_dict())
