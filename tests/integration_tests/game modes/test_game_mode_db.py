"""Test the main :class: `~yawning_titan.game_modes.game_mode_db.GameModeDB` class."""
import os
from unittest.mock import patch

import pytest

from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBError
from yawning_titan.game_modes.game_mode_db import GameModeDB, GameModeSchema
from yawning_titan.networks.network_db import default_18_node_network


@pytest.mark.integration_test
def test_db_file_exists():
    """Test the creation of the game mode db."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = GameModeDB()
        assert os.path.isfile(db._db._path)
        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_delete_default_game_mode_delete_fails():
    """Test attempted deletion of locked game mode fails."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = GameModeDB()
        config = db.search(DocMetadataSchema.LOCKED == True)[0]

        with pytest.raises(YawningTitanDBError):
            db.remove(config)

        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_game_mode_configuration_query():
    """Test searching by game mode property returns appropriate result."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = GameModeDB()
        found = db.search(
            GameModeSchema.CONFIGURATION.RED.AGENT_ATTACK.IGNORES_DEFENCES == False
        )
        not_found = db.search(
            GameModeSchema.CONFIGURATION.RED.AGENT_ATTACK.IGNORES_DEFENCES == "1"
        )
        GameModeSchema.CONFIGURATION.BLUE.ACTION_SET.deceptive_nodes.MAX_NUMBER

        assert len(not_found) == 0
        assert len(found) == len(db.all())
        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_game_mode_compatibility_query_network():
    """Test searching by network element compatibility returns appropriate result."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = GameModeDB()

        network = default_18_node_network()

        # default network is restricted to have between 2-5 entry nodes so this network will not be found
        found = db.search(GameModeSchema.ENTRY_NODES.works_with(network))
        assert len(found) == len(db.all()) - 1

        # default network is restricted to have between 2-5 high value nodes so this network will not be found
        found = db.search(GameModeSchema.HIGH_VALUE_NODES.works_with(network))
        assert len(found) == len(db.all()) - 1

        # default network is restricted to have between 2-18 network nodes so this network will not be found
        found = db.search(GameModeSchema.NETWORK_NODES.works_with(network))
        assert len(found) == len(db.all()) - 1

        # default game mode incompatible with network as high value nodes and network nodes have incompatible counts
        found = db.search(GameModeSchema.NETWORK_COMPATIBILITY.compatible_with(network))
        assert len(found) == len(db.all()) - 1

        db._db.close_and_delete_temp_db()


@pytest.mark.integration_test
def test_game_mode_compatibility_query_integer():
    """Test searching by network element compatibility expressed as an integer returns appropriate result."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        db = GameModeDB()

        # all are compatible as they are either unrestricted or sufficiently sized.
        found = db.search(GameModeSchema.ENTRY_NODES.works_with(3))
        assert len(found) == len(db.all())

        # default network is restricted to have between 2-5 high value nodes so this network will not be found
        found = db.search(GameModeSchema.HIGH_VALUE_NODES.works_with(0))
        assert len(found) == len(db.all()) - 1

        # all are compatible as they are either unrestricted or sufficiently sized.
        found = db.search(GameModeSchema.NETWORK_NODES.works_with(18))
        assert len(found) == len(db.all()) - 1

        db._db.close_and_delete_temp_db()
