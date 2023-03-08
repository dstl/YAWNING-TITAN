"""This test module tests the YawningTitanDB class using the DemoDB subclass."""
from copy import deepcopy
from typing import Dict, Final, List, Mapping, Optional, Union
from unittest.mock import patch

import pytest
from tinydb.queries import QueryInstance
from tinydb.table import Document

from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBCriticalError, YawningTitanDBError


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
            "hobbies": [
                "Water",
                "Malted Barley",
                "Glucose Syrup",
                "Barley",
                "Hops",
                "Hop Extract",
                "Nitrogen",
            ],
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

    def get(self, uuid: str) -> Union[Document, None]:
        """Get a dog from its uuid."""
        return super().get(uuid)

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


@pytest.mark.unit_test
def test_all(demo_db_docs):
    """Test the YawningTitanDB.insert and YawningTitanDB.all functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.all()

        db.close_and_delete_temp_db()

        assert results == demo_db_docs


@pytest.mark.unit_test
def test_get(demo_db_docs):
    """Test the awningTitanDB.get function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        doc = db.insert(item)
        results = db.get(doc["_doc_metadata"]["uuid"])

        db.close_and_delete_temp_db()

        assert results == item


@pytest.mark.unit_test
def test_search(demo_db_docs):
    """Test the YawningTitanDB.search function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        uuid = item["_doc_metadata"]["uuid"]
        db.insert(item)
        results = db.search(DocMetadataSchema.UUID == uuid)

        db.close_and_delete_temp_db()

        assert results == [item]


@pytest.mark.unit_test
def test_count(demo_db_docs):
    """Test the YawningTitanDB.count function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        count = db.count()

        db.close_and_delete_temp_db()

        assert count == len(demo_db_docs)


@pytest.mark.unit_test
def test_insert_existing_uuid_fails(demo_db_docs):
    """Test YawningTitanDB.insert function fails with duplicate uuid's."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        uuid = "Ignore me I'm from a unit test!"
        item["_doc_metadata"]["uuid"] = uuid
        db.insert(item)

        with pytest.raises(YawningTitanDBCriticalError):
            db.insert(item)

        db.close_and_delete_temp_db()


@pytest.mark.unit_test
def test_get_with_uuid_multiple_fails(demo_db_docs):
    """Test YawningTitanDB.get_with_uuid function fails with duplicate uuid's."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item_1 = demo_db_docs[0]
        item_2 = demo_db_docs[1]
        uuid = "Ignore me I'm from a unit test!"
        item_1["_doc_metadata"]["uuid"] = uuid
        db.insert(item_1)

        # Have to go this way around as inserting both with same uuid won't work.
        db.insert(item_2)
        item_2_original_uuid = item_2["_doc_metadata"]["uuid"]
        item_2["_doc_metadata"]["uuid"] = uuid
        db.update(item_2, item_2_original_uuid)
        with pytest.raises(YawningTitanDBCriticalError):
            db.get(uuid)

    db.close_and_delete_temp_db()


@pytest.mark.unit_test
def test_update(demo_db_docs):
    """Test the YawningTitanDB.insert and YawningTitanDB.update functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        db.insert(item)
        updated_item = deepcopy(item)
        updated_item["age"] = 30
        db.update(doc=updated_item, uuid=updated_item["_doc_metadata"]["uuid"])
        result = db.get(updated_item["_doc_metadata"]["uuid"])
        db.close_and_delete_temp_db()

        assert result["_doc_metadata"]["uuid"] == item["_doc_metadata"]["uuid"]
        assert result["age"] == 30
        assert (
            result["_doc_metadata"]["created_at"]
            < result["_doc_metadata"]["updated_at"]
        )


@pytest.mark.unit_test
def test_update_metadata(demo_db_docs):
    """Test the YawningTitanDB.update function with new metadata."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        db.insert(item)
        db.update(
            doc=item,
            uuid=item["_doc_metadata"]["uuid"],
            name="Johns file",
            description="A description of Johns file",
            author="Jane Doe",
        )
        result = db.get(item["_doc_metadata"]["uuid"])

        db.close_and_delete_temp_db()

        assert result["_doc_metadata"]["uuid"] == item["_doc_metadata"]["uuid"]
        assert result["_doc_metadata"]["name"] == "Johns file"
        assert result["_doc_metadata"]["description"] == "A description of Johns file"
        assert result["_doc_metadata"]["author"] == "Jane Doe"
        assert (
            result["_doc_metadata"]["created_at"]
            < result["_doc_metadata"]["updated_at"]
        )


@pytest.mark.unit_test
def test_update_locked_fails(demo_db_docs):
    """Test the YawningTitanDB.update function fails when updating a locked entry."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[2]
        db.insert(item)

        with pytest.raises(YawningTitanDBError):
            db.update(
                doc=item,
                uuid=item["_doc_metadata"]["uuid"],
                name="Johns file",
                description="A description of Johns file",
                author="Jane Doe",
            )

        db.close_and_delete_temp_db()


@pytest.mark.unit_test
def test_upsert_insert(demo_db_docs):
    """Test the YawningTitanDB.upsert function with a new insert."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        db.upsert(doc=item, uuid=item["_doc_metadata"]["uuid"])
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 1
        assert results[0] == item


@pytest.mark.unit_test
def test_upsert_update(demo_db_docs):
    """Test the YawningTitanDB.upsert function with an update."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        db.insert(item)
        updated_item = deepcopy(item)
        updated_item["age"] = 30
        db.upsert(doc=updated_item, uuid=updated_item["_doc_metadata"]["uuid"])
        result = db.get(updated_item["_doc_metadata"]["uuid"])

        db.close_and_delete_temp_db()

        assert result["_doc_metadata"]["uuid"] == item["_doc_metadata"]["uuid"]
        assert result["age"] == 30
        assert (
            result["_doc_metadata"]["created_at"]
            < result["_doc_metadata"]["updated_at"]
        )


@pytest.mark.unit_test
def test_remove(demo_db_docs):
    """Test the YawningTitanDB.remove function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        uuid = demo_db_docs[1]["_doc_metadata"]["uuid"]
        removed_uuids = db.remove_by_cond(DemoSchema.AGE == demo_db_docs[1]["age"])
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 2
        assert results == [demo_db_docs[0], demo_db_docs[2]]
        assert removed_uuids == [uuid]


@pytest.mark.unit_test
def test_remove_with_uuid(demo_db_docs):
    """Test the YawningTitanDB.remove_with_uuid function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        uuid = demo_db_docs[1]["_doc_metadata"]["uuid"]
        removed_uuid = db.remove(uuid)
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 2
        assert results == [demo_db_docs[0], demo_db_docs[2]]
        assert removed_uuid == uuid


@pytest.mark.unit_test
def test_remove_with_uuid_multiple_fails(demo_db_docs):
    """Test YawningTitanDB.remove_with_uuid function fails with duplicate uuid's."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item_1 = demo_db_docs[0]
        item_1_original_uuid = item_1["_doc_metadata"]["uuid"]
        db.insert(item_1)

        # Have to go this way around as inserting both with same uuid won't work.
        uuid = "Ignore me I'm from a unit test!"
        item_1["_doc_metadata"]["uuid"] = uuid
        db.insert(item_1)

        db.update(item_1, item_1_original_uuid)

        with pytest.raises(YawningTitanDBCriticalError):
            db.remove(uuid)

    db.close_and_delete_temp_db()


@pytest.mark.unit_test
def test_remove_locked_fails(demo_db_docs):
    """Test the YawningTitanDB.remove function fails when removing a locked entry."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[2]
        db.insert(item)

        with pytest.raises(YawningTitanDBError):
            db.remove(item["_doc_metadata"]["uuid"])

        db.close_and_delete_temp_db()
