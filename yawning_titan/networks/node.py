from __future__ import annotations

from typing import Final, Optional
from uuid import uuid4


class Node:
    def __init__(
            self,
            uuid: Optional[str] = None,
            name: Optional[str] = None,
            high_value_node: bool = False,
            entry_node: bool = False,
            vulnerability: int = 0,
            x_pos: float = 0.0,
            y_pos: float = 0.0,
            classes: Optional[str] = None
    ):
        if uuid is None:
            uuid = str(uuid4())
        self._uuid: Final[str] = uuid
        self.name: str = name
        self._high_value_node: bool = high_value_node
        self._entry_node: bool = entry_node
        self.vulnerability = vulnerability
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
