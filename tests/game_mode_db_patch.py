from unittest.mock import patch

from tests.yawning_titan_db_patch import yawning_titan_db_test_defaults_patch
from yawning_titan.db.yawning_titan_db import YawningTitanDB


def game_mode_db_init_patch(self):
    """Patch GameModeDB to use the tests/_package_data/game_modes.json db file."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_test_defaults_patch):
        self._db = YawningTitanDB("game_modes")
