"""Test the main :class:`` class."""
import os
from unittest.mock import patch

from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.config.network_config import NetworkConfig
from yawning_titan.db.network import NetworkDB
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.envs.generic.helpers.network_creator import create_18_node_network


def test_db_file_exists():
    """Test the creation of the network db."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        assert os.path.isfile(db._path)
        db.close_and_delete_temp_db()


def test_insert_and_read():
    """Test insertion and retrieval from the network db."""
    matrix, positions = create_18_node_network()
    network_config = NetworkConfig.create_from_args(matrix=matrix, positions=positions)

    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = NetworkDB()
        db.insert(network_config)

        assert db.all()[0].to_dict(json_serializable=True) == network_config.to_dict(
            json_serializable=True
        )
        db.close_and_delete_temp_db()
