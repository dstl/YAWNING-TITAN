from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Final, List, Mapping, Union

from tinydb import TinyDB
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan import DB_DIR


class YawningTitanDB(ABC):
    """An :py:class:`~abc.ABC` that implements the :class:`~tinydb.database.TinyDB` query functions."""

    @abstractmethod
    def __init__(self, name: str):
        self._name: Final[str] = name
        self._db = TinyDB(DB_DIR / f"{self._name}.json")

    @property
    def name(self) -> str:
        """The DB name."""
        return self._name

    @property
    def db(self) -> TinyDB:
        """The instance of :class:`~tinydb.database.TinyDB`."""
        return self._db

    @abstractmethod
    def insert(self, item: Mapping) -> int:
        """An abstract :func:`tinydb.table.Table.insert` method."""
        return self.db.insert(item)

    @abstractmethod
    def all(self) -> List[Document]:
        """An abstract :func:`tinydb.table.Table.all` method."""
        return self.db.all()

    @abstractmethod
    def get(self, doc_id: int) -> Union[Document, None]:
        """An abstract :func:`tinydb.table.Table.get` method."""
        return self.db.get(doc_id=doc_id)

    @abstractmethod
    def search(self, query: QueryInstance) -> List[Document]:
        """An abstract :func:`tinydb.table.Table.search` method."""
        return self.db.search(query)
