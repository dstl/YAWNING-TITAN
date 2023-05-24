"""
The `yawning_titan` top-level __init__.

`gym.envs` registered:
    `five-node-def-v0`
        entry_point: `yawning_titan.envs.specific:FiveNodeDef`
    `four-node-def-v0`
        entry_point: `yawning_titan.envs.specific:FourNodeDef`
    `networks-graph-explore-v0`
        entry_point: `yawning_titan.envs.specific:GraphExplore`
    `18-node-env-v0`
        entry_point: `yawning_titan.envs.specific:NodeEnv`

App directories initialised:
    `LOG_DIR`:
        The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS.

Logging configured from the root:
    Logging is configured using the `yawning_titan.config._package_data.logging_config.yaml` config file.
"""
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
    id="networks-graph-explore-v0",
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


def _version() -> str:
    version_path = _YT_ROOT_DIR / "VERSION"
    with open(version_path, "r") as file:
        return file.readline().strip()


__version__ = _version()


def _log_dir() -> Union[Path, PosixPath]:
    if sys.platform == "win32":
        dir_path = _YT_PLATFORM_DIRS.user_data_path / "logs"
    else:
        dir_path = _YT_PLATFORM_DIRS.user_log_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


# Force all to be created if not already
DATA_DIR: Final[Union[Path, PosixPath]] = _YT_PLATFORM_DIRS.user_data_path
"""The path to the app data directory as an instance of `Path` or `PosixPath`, depending on the OS."""


LOG_DIR: Final[Union[Path, PosixPath]] = _log_dir()
"""The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS."""


DB_DIR: Final[Union[Path, PosixPath]] = _YT_PLATFORM_DIRS.user_data_path / "db"
"""The path to the app db directory as an instance of `Path` or `PosixPath`, depending on the OS."""

APP_IMAGES_DIR: Final[Union[Path, PosixPath]] = _YT_PLATFORM_DIRS.user_data_path / "app_images"
"""The path to the app images directory as an instance of `Path` or `PosixPath`, depending on the OS."""

NOTEBOOKS_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "notebooks"
"""
The path to the users notebooks directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users notebooks are stored at: ~/yawning_titan/notebooks.
"""

GAME_MODES_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "game_modes"
"""
The path to the users game modes directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users game modes are stored at: ~/yawning_titan/game_modes.
"""

IMAGES_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "images"
"""
The path to the users images directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users images are stored at: ~/yawning_titan/images.
"""

VIDEOS_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "videos"
"""
The path to the users videos directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users videos are stored at: ~/yawning_titan/videos.
"""

AGENTS_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "agents"
"""
The path to the users agents directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agents are stored at: ~/yawning_titan/agents.
"""

AGENTS_LOGS_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "agents" / "logs"
"""
The path to the users agents logs directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agent logs are stored at: ~/yawning_titan/agents/logs.
"""

PPO_TENSORBOARD_LOGS_DIR: Final[Union[Path, PosixPath]] = _YT_USER_DIRS / "agents" / "logs" / "tensorboard"
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
