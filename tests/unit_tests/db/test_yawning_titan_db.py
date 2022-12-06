"""This test module tests the YawningTitanDB class using the DemoDB subclass."""
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
from yawning_titan.exceptions import YawningTitanDBError

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
        doc_id = db.insert(item)
        results = db.get(doc_id)

        db.close_and_delete_temp_db()

        assert results == item


@pytest.mark.unit_test
def test_get_with_uuid(demo_db_docs):
    """Test the YawningTitanDB.insert and YawningTitanDB.get functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        uuid = item["_doc_metadata"]["uuid"]
        db.insert(item)
        results = db.search(DocMetadataSchema.UUID == uuid)

        db.close_and_delete_temp_db()

        assert results == [item]


def test_get_with_uuid_multiple_fails(demo_db_docs):
    """Test YawningTitanDB.get_with_uuid function fails with duplicate uuid's."""
    with pytest.raises(YawningTitanDBError):

        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            db = DemoDB("test")
            item = demo_db_docs[0]
            uuid = "Ignore me I'm from a unit test!"
            item["_doc_metadata"]["uuid"] = uuid
            db.insert(item)
            db.insert(item)
            db.get_with_uuid(uuid)

        db.close_and_delete_temp_db()


@pytest.mark.unit_test
def test_update(demo_db_docs):
    """Test the YawningTitanDB.insert and YawningTitanDB.update functions."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        doc_id = db.insert(item)
        item["age"] = 30
        db.update(doc=item, uuid=item["_doc_metadata"]["uuid"])
        results = db.get(doc_id)

        db.close_and_delete_temp_db()

        assert results == item


@pytest.mark.unit_test
def test_upsert(demo_db_docs):
    """Test the YawningTitanDB.upsert function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        item = demo_db_docs[0]
        db.upsert(doc=item, uuid=item["_doc_metadata"]["uuid"])
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 1
        assert results[0] == item


def test_remove(demo_db_docs):
    """Test the YawningTitanDB.remove function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        db.remove(DemoSchema.AGE == demo_db_docs[1]["age"])
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 1
        assert results == [demo_db_docs[0]]


def test_remove_with_uuid(demo_db_docs):
    """Test the YawningTitanDB.remove_with_uuid function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        db.remove_with_uuid(demo_db_docs[1]["_doc_metadata"]["uuid"])
        results = db.all()

        db.close_and_delete_temp_db()

        assert len(results) == 1
        assert results == [demo_db_docs[0]]


def test_remove_with_uuid_multiple_fails(demo_db_docs):
    """Test YawningTitanDB.remove_with_uuid function fails with duplicate uuid's."""
    with pytest.raises(YawningTitanDBError):

        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            db = DemoDB("test")
            item = demo_db_docs[0]
            uuid = "Ignore me I'm from a unit test!"
            item["_doc_metadata"]["uuid"] = uuid
            db.insert(item)
            db.insert(item)
            db.remove_with_uuid(uuid)

        db.close_and_delete_temp_db()
