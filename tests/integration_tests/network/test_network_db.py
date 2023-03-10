"""Test the main :class: `yawning_titan.networks.network_db.NetworkDB`."""
import os
from copy import copy
from unittest.mock import patch

import pytest

from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBError
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema


@pytest.mark.integration_test
def test_db_file_exists():
    """Test the creation of the network db."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        assert os.path.isfile(db._db._path)
        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_delete_default_network_delete_fails():
    """Test attempted deletion of locked network fails."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        db.rebuild_db()
        config = db.search(DocMetadataSchema.LOCKED == True)[0]
        with pytest.raises(YawningTitanDBError):
            db.remove(config)

        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_reset_default_networks():
    """Test resetting network to default removes modifications."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        db.rebuild_db()
        networks_copy = copy.deepcopy(db.all())

        network_copy = networks_copy[0]

        # Update the object locally
        network_copy.set_random_entry_nodes = False

        # Hack an update to the locked network in the db
        db._db.db.update(
            network_copy.to_dict(json_serializable=True),
            DocMetadataSchema.UUID == network_copy.doc_metadata.uuid,
        )

        # Perform the default network reset
        db.reset_default_networks_in_db()

        assert db.all() == networks_copy

        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_network_schema():
    """Test querying the network DB using NetworkSchema."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        db.rebuild_db()
        results = db.search(NetworkSchema.SET_RANDOM_ENTRY_NODES == True)
        assert len(results) == 1
        assert results[0].doc_metadata.uuid == "b3cd9dfd-b178-415d-93f0-c9e279b3c511"
        db._db.close_and_delete_temp_db()
