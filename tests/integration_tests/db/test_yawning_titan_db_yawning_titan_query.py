"""This test modules tests the integration between YawningTitanDB and YawningTitanQuery."""
from unittest.mock import patch

import pytest

from tests.unit_tests.db.test_yawning_titan_db import DemoDB, DemoSchema, demo_db_docs
from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.yawning_titan_db import YawningTitanDB

docs = demo_db_docs  # noqa


@pytest.mark.integration_test
def test_count_with_condition(demo_db_docs):
    """Test the YawningTitanDB.count function with a condition."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        count = db.count(DemoSchema.AGE == 25)

        db.close_and_delete_temp_db()

        assert count == 1


@pytest.mark.integration_test
def test_yt_query_len_eq(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_eq` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_eq(3))
        assert len(results) == 1
        assert results == [demo_db_docs[0]]
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_lt(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_lt` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_lt(4))
        assert len(results) == 1
        assert results == [demo_db_docs[0]]
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_le(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_le` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_le(4))
        assert len(results) == 2
        assert results == demo_db_docs[:2]
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_gt(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_gt` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_gt(3))
        assert len(results) == 2
        assert results == demo_db_docs[1:]
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_ge(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_ge` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_ge(3))
        assert len(results) == 3
        assert results == demo_db_docs
        db.close_and_delete_temp_db()
