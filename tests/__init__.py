import os
from pathlib import Path
from typing import Final

from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.game_modes.game_mode_db import GameModeDB

TEST_CONFIG_PATH_OLD: Final[Path] = Path(
    os.path.join(Path(__file__).parent.resolve(), "test_configs", "game_mode", "old")
)

TEST_CONFIG_PATH_NEW: Final[Path] = Path(
    os.path.join(Path(__file__).parent.resolve(), "test_configs", "game_mode", "new")
)

TEST_BASE_CONFIG_PATH = Path(
    os.path.join(
        Path(__file__).parent.resolve(),
        "test_configs",
        "game_mode",
        "old",
        "base_config.yaml",
    )
)

TEST_BASE_NEW_CONFIG_PATH = Path(
    os.path.join(
        Path(__file__).parent.resolve(),
        "test_configs",
        "game_mode",
        "new",
        "base_new_config.yaml",
    )
)


class TestGameModeDB(GameModeDB):
    """An subclass of :class: `~yawning_titan.game_modes.game_mode_db.GameModeDB` to point to the test GameMode data."""

    def __init__(self):
        self._db = YawningTitanDB("test_game_modes", root=TEST_CONFIG_PATH_OLD.parent)
