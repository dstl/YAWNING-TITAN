from __future__ import annotations

from typing import List, Optional
from uuid import uuid4


class Node:
    """A Node for building networks with yawning_titan.networks.network.Network."""

    def __init__(
        self,
        name: Optional[str] = None,
        high_value_node: bool = False,
        entry_node: bool = False,
        vulnerability: float = 0.01,
        classes: str = None,
    ):
        """
        The Node constructor.

        :param name: An optional name for the Node.
        :param high_value_node: Whether the Node is a high value node.
            Default value of False.
        :param entry_node: Whether the Node is an entry node. Default value
            of False.
        :param vulnerability: The vulnerability score of the Node. Has a
            default value of 0.1.
        """
        self._uuid: str = str(uuid4())
        self.name: str = name
        self._high_value_node: bool = high_value_node
        self._entry_node: bool = entry_node
        self._vulnerability = vulnerability
        self.classes = classes

        # Default node attributes
        self._x_pos: float = 0.0
        self._y_pos: float = 0.0
        self.vulnerability_score = vulnerability
        self.true_compromised_status = 0
        self.blue_view_compromised_status = 0
        self.deceptive_node = False
        self.blue_knows_intrusion = False
        self.isolated = False

    @classmethod
    def create_from_db(
        cls,
        uuid: str,
        high_value_node: bool,
        entry_node: bool,
        vulnerability: float,
        x_pos: float,
        y_pos: float,
        classes: str = None,
        name: Optional[str] = None,
    ) -> Node:
        """
        Used to create an instance of Node from the NetworkDB.

        :param uuid: the UUID given to a Node when it was first created.
        :param high_value_node: Whether the Node is a high value node.
        :param entry_node: Whether the Node is an entry node.
        :param vulnerability: The vulnerability score of the Node.
        :param x_pos: The x-position when displayed on a network graph.
        :param y_pos: The y-position when displayed on a network graph.
        :param name: An optional name for the Node.

        :return: The instance of Node.
        """
        node = Node(
            name=name,
            high_value_node=high_value_node,
            entry_node=entry_node,
            vulnerability=vulnerability,
            classes=classes,
        )
        node._uuid = uuid
        node.x_pos = x_pos
        node.y_pos = y_pos
        return node

    def reset_vulnerability(self):
        """Resets the nodes current `vulnerability_score` to the original `vulnerability`."""
        self.vulnerability_score = self.vulnerability

    @property
    def node_position(self) -> List[float]:
        """The nodes position as a list [x,y]."""
        return [self.x_pos, self.y_pos]

    @node_position.setter
    def node_position(self, pos: List[float]):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

    @property
    def vulnerability(self) -> float:
        """The nodes initial vulnerability."""
        return self._vulnerability

    @vulnerability.setter
    def vulnerability(self, x):
        self._vulnerability = x
        self.vulnerability_score = x

    @property
    def uuid(self) -> str:
        """The node UUID."""
        return self._uuid

    @property
    def high_value_node(self) -> bool:
        """True if the Node is high value, otherwise False."""
        return self._high_value_node

    @high_value_node.setter
    def high_value_node(self, high_value_node: bool):
        self._high_value_node = high_value_node

    @property
    def entry_node(self) -> bool:
        """True if the Node is an entry node, otherwise False."""
        return self._entry_node

    @entry_node.setter
    def entry_node(self, entry_node: bool):
        self._entry_node = entry_node

    @property
    def x_pos(self) -> float:
        """The x-position of the node."""
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos: float):
        self._x_pos = x_pos

    @property
    def y_pos(self) -> float:
        """The y-position of the node."""
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos: float):
        self._y_pos = y_pos

    def to_dict(self):
        """The Node as a dict."""
        return {
            "uuid": self._uuid,
            "name": self.name,
            "high_value_node": self._high_value_node,
            "entry_node": self._entry_node,
            "vulnerability": self.vulnerability,
            "x_pos": self._x_pos,
            "y_pos": self._y_pos,
        }

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.uuid

    def __repr__(self):
        node_str = f"{self.__class__.__name__}(" f"uuid='{self._uuid}', "
        if self.name:
            node_str += f"name='{self.name}', "
        node_str += (
            f"high_value_node={self._high_value_node}, "
            f"entry_node={self._entry_node}, "
            f"vulnerability={self.vulnerability}, "
            f"x_pos={self._x_pos}, "
            f"y_pos={self._y_pos}"
            f")"
        )
        return node_str

    def __hash__(self):
        return hash((self._uuid))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

    def __lt__(self, other: Node):
        if isinstance(other, Node):
            return self.uuid < other.uuid
        return self.uuid < other
