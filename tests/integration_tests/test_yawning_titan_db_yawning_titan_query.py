"""This test modules tests the integration between YawningTitanDB and YawningTitanQuery."""
from unittest.mock import patch

import pytest

from tests.fixtures.yawning_titan_demo_db_fixtures import (
    DemoDB,
    DemoSchema,
    demo_db_docs,
)
from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.yawning_titan_db import YawningTitanDB

docs = demo_db_docs  # Dummy line to 'use' demo_db_docs so flake8 doesn't throw F401 or F811


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
        assert results == demo_db_docs
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_gt(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_gt` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_gt(3))
        assert len(results) == 1
        assert results == [demo_db_docs[1]]
        db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_yt_query_len_ge(demo_db_docs):
    """Test the custom :func:`yawning_titan.db.query.YawningTitanQuery.len_ge` function."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = DemoDB("test")
        for item in demo_db_docs:
            db.insert(item)
        results = db.search(DemoSchema.HOBBIES.len_ge(3))
        assert len(results) == 2
        assert results == demo_db_docs
        db.close_and_delete_temp_db()
