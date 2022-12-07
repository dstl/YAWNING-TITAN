"""Fixtures and classes for testing the YawningTitanDB and YawningTitanQuery classes."""
from typing import Dict, Final, List, Mapping, Optional, Union

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
        {
            "forename": "John",
            "surname": "Smith",
            "age": 264,
            "hobbies": ["Barley", "Hops", "Water"],
            "_doc_metadata": DocMetadata(locked=True).to_dict(),
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

    def insert(
        self,
        doc: Mapping,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """Insert a doc and return the inserted doc."""
        return super().insert(doc, name, description, author)

    def all(self) -> List[Document]:
        """Get all docs."""
        return super().all()

    def get_uuid(self, uuid: str) -> Union[Document, None]:
        """Get a dog from its uuid."""
        return super().get_uuid(uuid)

    def search(self, query: QueryInstance) -> List[Document]:
        """Search for docs using Query."""
        return super().search(query)

    def update(
        self,
        doc: Mapping,
        uuid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """Update a doc by uuid."""
        return super().update(doc, uuid, name, description, author)

    def upsert(
        self,
        doc: Mapping,
        uuid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """Upsert a doc by uuid."""
        return super().upsert(doc, uuid, name, description, author)

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """Remove documents matching a query."""
        return super().remove_by_cond(cond)

    def remove(self, uuid: str) -> str:
        """Remove a document with a given uuid."""
        return super().remove(uuid)
