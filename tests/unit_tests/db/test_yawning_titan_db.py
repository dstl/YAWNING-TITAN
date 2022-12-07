"""This test module tests the YawningTitanDB class using the DemoDB subclass."""
from copy import deepcopy
from unittest.mock import patch

import pytest

from tests.fixtures.yawning_titan_demo_db_fixtures import (
    DemoDB,
    DemoSchema,
    demo_db_docs,
)
from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBCriticalError, YawningTitanDBError

docs = demo_db_docs  # Dummy line to 'use' demo_db_docs so flake8 doesn't throw F401 or F811


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
    """Test the YawningTitanDB.insert and YawningTitanDB.get functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        doc = db.insert(item)
        results = db.get_uuid(doc["_doc_metadata"]["uuid"])

        db.close_and_delete_temp_db()

        assert results == item


@pytest.mark.unit_test
def test_search(demo_db_docs):
    """Test the YawningTitanDB.insert and YawningTitanDB.get functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        uuid = item["_doc_metadata"]["uuid"]
        db.insert(item)
        results = db.search(DocMetadataSchema.UUID == uuid)

        db.close_and_delete_temp_db()

        assert results == [item]


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
            db.get_uuid(uuid)

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
        result = db.get_uuid(updated_item["_doc_metadata"]["uuid"])
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
        result = db.get_uuid(item["_doc_metadata"]["uuid"])

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
        result = db.get_uuid(updated_item["_doc_metadata"]["uuid"])

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
