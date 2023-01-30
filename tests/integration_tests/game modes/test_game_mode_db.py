"""Test the main :class:`` class."""
import os
from unittest.mock import patch

import pytest

from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.exceptions import YawningTitanDBError
from yawning_titan.game_modes.game_mode_db import GameModeDB


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
