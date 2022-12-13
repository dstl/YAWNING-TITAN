"""
The `yawning_titan` top-level __init__.

`gym.envs` registered:
    `five-node-def-v0`
        entry_point: `yawning_titan.envs.specific:FiveNodeDef`
    `four-node-def-v0`
        entry_point: `yawning_titan.envs.specific:FourNodeDef`
    `network-graph-explore-v0`
        entry_point: `yawning_titan.envs.specific:GraphExplore`
    `18-node-env-v0`
        entry_point: `yawning_titan.envs.specific:NodeEnv`
App directories initialised:
    `DATA_DIR`:
        The path to the app data directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `CONFIG_DIR`:
        The path to the app config directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `LOG_DIR`:
        The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `DOCS_DIR`:
        The path to the app docs directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `DB_DIR`:
        The path to the app db directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `APP_IMAGES_DIR`:
        The path to the app images directory as an instance of `Path` or `PosixPath`, depending on the OS.

User directories initialised:
    `NOTEBOOKS_DIR`:
        The path to the users notebooks directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `GAME_MODES_DIR`:
        The path to the users game modes directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `IMAGES_DIR`:
        The path to the users images directory as an instance of `Path` or `PosixPath`, depending on the OS.
    `AGENTS_DIR`:
        The path to the users agents directory as an instance of `Path` or `PosixPath`, depending on the OS.

Logging configured from the root:
    Logging is configured using the `yawning_titan.config._package_data.logging_config.yaml` config file.
"""
__version__ = "1.0.1"

import logging.config
import os
import sys
from pathlib import Path, PosixPath
from typing import Final, Union

import yaml
from gym.envs.registration import register
from platformdirs import PlatformDirs

register(id="five-node-def-v0", entry_point="yawning_titan.envs.specific:FiveNodeDef")

register(id="four-node-def-v0", entry_point="yawning_titan.envs.specific:FourNodeDef")

register(
    id="network-graph-explore-v0",
    entry_point="yawning_titan.envs.specific:GraphExplore",
)

register(id="18-node-env-v0", entry_point="yawning_titan.envs.specific:NodeEnv")

# Below handles application directories and user directories.
# Uses `platformdirs.PlatformDirs` and `pathlib.Path` to create the required app directories in the correct locations
# based on the users OS.

_YT_ROOT_DIR: Final[Union[Path, PosixPath]] = Path(__file__).parent.resolve()

_YT_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(appname="yawning_titan")
"""An instance of `PlatformDirs` set with appname='yawning_titan'."""

_YT_USER_DIRS: Final[Union[Path, PosixPath]] = Path.home() / "yawning_titan"
"""The users home space for YT which is located at: ~/yawning_titan."""


def _data_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_PLATFORM_DIRS.user_data_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _config_dir() -> Union[Path, PosixPath]:
    if sys.platform == "win32":
        dir_path = _YT_PLATFORM_DIRS.user_data_path / "config"
    else:
        dir_path = _YT_PLATFORM_DIRS.user_config_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _log_dir() -> Union[Path, PosixPath]:
    if sys.platform == "win32":
        dir_path = _YT_PLATFORM_DIRS.user_data_path / "logs"
    else:
        dir_path = _YT_PLATFORM_DIRS.user_log_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _docs_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "docs"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _db_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "db"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _app_images_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "app_images"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _notebooks_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "notebooks"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _game_modes_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "game_modes"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _images_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "images"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _agents_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "agents"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _agents_logs_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "agents" / "logs"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _ppo_tensorboard_logs_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_USER_DIRS / "agents" / "logs" / "tensorboard"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


# Force all to be created if not already
DATA_DIR: Final[Union[Path, PosixPath]] = _data_dir()
"""The path to the app data directory as an instance of `Path` or `PosixPath`, depending on the OS."""

CONFIG_DIR: Final[Union[Path, PosixPath]] = _config_dir()
"""The path to the app config directory as an instance of `Path` or `PosixPath`, depending on the OS."""

LOG_DIR: Final[Union[Path, PosixPath]] = _log_dir()
"""The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS."""

DOCS_DIR: Final[Union[Path, PosixPath]] = _docs_dir()
"""The path to the app docs directory as an instance of `Path` or `PosixPath`, depending on the OS."""

DB_DIR: Final[Union[Path, PosixPath]] = _db_dir()
"""The path to the app db directory as an instance of `Path` or `PosixPath`, depending on the OS."""

APP_IMAGES_DIR: Final[Union[Path, PosixPath]] = _app_images_dir()
"""The path to the app images directory as an instance of `Path` or `PosixPath`, depending on the OS."""

NOTEBOOKS_DIR: Final[Union[Path, PosixPath]] = _notebooks_dir()
"""
The path to the users notebooks directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users notebooks are stored at: ~/yawning_titan/notebooks.
"""

GAME_MODES_DIR: Final[Union[Path, PosixPath]] = _game_modes_dir()
"""
The path to the users game modes directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users game modes are stored at: ~/yawning_titan/game_modes.
"""

IMAGES_DIR: Final[Union[Path, PosixPath]] = _images_dir()
"""
The path to the users images directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users images are stored at: ~/yawning_titan/images.
"""

AGENTS_DIR: Final[Union[Path, PosixPath]] = _agents_dir()
"""
The path to the users agents directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agents are stored at: ~/yawning_titan/agents.
"""

AGENTS_LOGS_DIR: Final[Union[Path, PosixPath]] = _agents_logs_dir()
"""
The path to the users agents logs directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agent logs are stored at: ~/yawning_titan/agents/logs.
"""

PPO_TENSORBOARD_LOGS_DIR: Final[Union[Path, PosixPath]] = _ppo_tensorboard_logs_dir()
"""
The path to the PPO algorithm tensorboard logs directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agent PPO algorithm tensorboard logs are stored at: ~/yawning_titan/agents/logs/ppo_tensorboard.
"""

# Setup root logger format
with open(
    _YT_ROOT_DIR / "config" / "_package_data" / "logging_config.yaml", "r"
) as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

LOG_FILE_PATH: Final[str] = os.path.join(
    LOG_DIR, config["handlers"]["info_rotating_file_handler"]["filename"]
)
config["handlers"]["info_rotating_file_handler"]["filename"] = LOG_FILE_PATH

try:
    logging.config.dictConfig(config)
except Exception as e:
    print(e)
