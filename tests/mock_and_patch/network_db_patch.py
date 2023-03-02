from unittest.mock import patch

from tests.mock_and_patch.yawning_titan_db_patch import (
    yawning_titan_db_test_defaults_patch,
)
from yawning_titan.db.yawning_titan_db import YawningTitanDB


def network_db_init_patch(self):
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_test_defaults_patch):
        self._db = YawningTitanDB("networks")
