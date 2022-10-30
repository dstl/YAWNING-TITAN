import logging
import os
from pathlib import Path
from typing import Final

from gym.envs.registration import register
from platformdirs import PlatformDirs

# TODO: Set root level logging with defined format with RotatingFileHandler
logger = logging.getLogger("yawning_titan")

register(
    id="five-node-def-v0",
    entry_point="yawning_titan.envs.specific:FiveNodeDef"
)

register(
    id="four-node-def-v0",
    entry_point="yawning_titan.envs.specific:FourNodeDef"
)

register(
    id="network-graph-explore-v0",
    entry_point="yawning_titan.envs.specific:GraphExplore",
)

register(
    id="18-node-env-v0", entry_point="yawning_titan.envs.specific:NodeEnv"
)

_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs("yawning_titan", "DSTL")

CONFIG_DIR: Final[Path] = _PLATFORM_DIRS.user_config_path
"""
The path to the app config directory as an instance of pathlib.Path.
"""

LOG_DIR: Final[Path] = _PLATFORM_DIRS.user_log_path
"""
The path to the app log directory as an instance of pathlib.Path.
"""

DATA_DIR: Final[Path] = _PLATFORM_DIRS.user_data_path
"""
The path to the app data directory as an instance of pathlib.Path.
"""

GAME_MODES_DIR: Final[Path] = Path(os.path.join(CONFIG_DIR, "game_modes"))
"""
The path to the app game modes directory as an instance of pathlib.Path.
"""

NOTEBOOKS_DIR: Final[Path] = Path(os.path.join(DATA_DIR, "notebooks"))
"""
The path to the app notebooks directory as an instance of pathlib.Path.
"""

DOCS_DIR: Final[Path] = Path(os.path.join(DATA_DIR, "docs"))
"""
The path to the app docs directory as an instance of pathlib.Path.
"""

IMAGES_DIR: Final[Path] = Path(os.path.join(DATA_DIR, "images"))
"""
The path to the app images directory as an instance of pathlib.Path.
"""
