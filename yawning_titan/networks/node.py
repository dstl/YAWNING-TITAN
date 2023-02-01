from __future__ import annotations

from typing import Final, Optional
from uuid import uuid4


class Node:
    """A Node class that is used by the Network subclass of networkx.Graph."""

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        high_value_node: bool = False,
        entry_node: bool = False,
        vulnerability: float = 0.0,
        x_pos: float = 0.0,
        y_pos: float = 0.0,
        classes: Optional[str] = None,
    ):
        if uuid is None:
            uuid = str(uuid4())
        self._uuid: Final[str] = uuid
        self.name: str = name
        self._high_value_node: bool = high_value_node
        self._entry_node: bool = entry_node
        self._vulnerability = vulnerability
        self._x_pos: float = x_pos
        self._y_pos: float = y_pos
        self._classes = classes
        self._set_classes()

        # Default node attributes
        self.vulnerability_score = vulnerability
        self.true_compromised_status = 0
        self.blue_view_compromised_status = 0
        self.node_position = 0
        self.deceptive_node = False
        self.blue_knows_intrusion = False
        self.isolated = False

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

    def set_vulnerability(self, x):
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
        self._set_classes()

    @property
    def entry_node(self) -> bool:
        """True if the Node is an entry node, otherwise False."""
        return self._entry_node

    @entry_node.setter
    def entry_node(self, entry_node: bool):
        self._entry_node = entry_node
        self._set_classes()

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
            f"name='{self.name}', "
            f"high_value_node={self._high_value_node}, "
            f"entry_node={self._entry_node}, "
            f"vulnerability={self.vulnerability}, "
            f"x_pos={self._x_pos}, "
            f"y_pos={self._y_pos}"
            f")"
        )

    def __hash__(self):
        return hash((self._uuid, self.name, self._high_value_node, self._entry_node))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False
