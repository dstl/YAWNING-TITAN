"""Fixtures and classes for testing the YawningTitanDB and YawningTitanQuery classes."""
from typing import Dict, Final, List, Mapping, Union

import pytest
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.db.yawning_titan_db import YawningTitanDB


@pytest.fixture
def demo_db_docs() -> List[Dict[str, Union[str, int, List[str]]]]:
    """
    A basic list of docs with the structure.

    - forename: str
    - surname: str
    - age: int
    - hobbies: List[str]
    """
    return [
        {
            "forename": "John",
            "surname": "Doe",
            "age": 25,
            "hobbies": ["Cats", "Books", "Food"],
            "_doc_metadata": DocMetadata().to_dict(),
        },
        {
            "forename": "Jane",
            "surname": "Doe",
            "age": 26,
            "hobbies": ["Cats", "Books", "Food", "Walks"],
            "_doc_metadata": DocMetadata().to_dict(),
        },
    ]


class DemoSchema:
    """A schema-like class that defines the DB fields in ``demo_db_docs()``."""

    FORENAME: Final[YawningTitanQuery] = YawningTitanQuery().forename
    """Mapped to ``demo_db_docs()["forename"]``."""
    SURNAME: Final[YawningTitanQuery] = YawningTitanQuery().surname
    """Mapped to ``demo_db_docs()["surname"]``."""
    AGE: Final[YawningTitanQuery] = YawningTitanQuery().age
    """Mapped to ``demo_db_docs()["age"]``."""
    HOBBIES: Final[YawningTitanQuery] = YawningTitanQuery().hobbies
    """Mapped to ``demo_db_docs()["hobbies"]``."""


class DemoDB(YawningTitanDB):
    """An implementation of :class:`~yawning_titan.db.yawning_titan_db.YawningTitanDB`."""

    def __init__(self, name: str):
        super().__init__(name)

    def insert(self, item: Mapping) -> int:
        """Insert a doc and return the inserted doc_id."""
        return super().insert(item)

    def all(self) -> List[Document]:
        """Get all docs."""
        return super().all()

    def get(self, doc_id: int) -> Union[Document, None]:
        """Get a dog from its doc_id."""
        return super().get(doc_id)

    def get_with_uuid(self, uuid: int) -> Union[Document, None]:
        """Get a dog from its uuid."""
        return super().get_with_uuid(uuid)

    def search(self, query: QueryInstance) -> List[Document]:
        """Search for docs using Query."""
        return super().search(query)

    def update(self, doc: Mapping, uuid: str) -> List[int]:
        """Update a doc by uuid."""
        return super().update(doc, uuid)

    def upsert(self, doc: Mapping, uuid: str) -> List[int]:
        """Upsert a doc by uuid."""
        return super().upsert(doc, uuid)

    def remove(self, cond: QueryInstance) -> List[int]:
        """Remove documents matching a query."""
        return super().remove(cond)

    def remove_with_uuid(self, uuid: str) -> List[int]:
        """Remove a document with a given uuid."""
        return super().remove_with_uuid(uuid)
