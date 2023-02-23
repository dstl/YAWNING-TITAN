"""Test the main :class: `yawning_titan.networks.network_db.NetworkDB`."""
import copy
import os
from unittest.mock import patch

import pytest

from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBError
from yawning_titan.networks.network_db import NetworkDB


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
        configs = db.all()

        config = configs[0]
        config_copy = copy.deepcopy(config)

        # Update the object locally
        config.set_random_entry_nodes = False

        # Hack an update to the locked network in the db
        db._db.db.update(
            config.to_dict(json_serializable=True),
            DocMetadataSchema.UUID == config.doc_metadata.uuid,
        )

        # Perform the default network reset
        db.reset_default_networks_in_db()

        assert db.all()[0].set_random_entry_nodes == config_copy.set_random_entry_nodes

        db._db.close_and_delete_temp_db()
