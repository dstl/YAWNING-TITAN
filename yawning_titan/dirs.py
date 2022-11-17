"""
The `dirs.py` module handles application directories and user directories.

Uses `platformdirs.PlatformDirs` and `pathlib.Path` to create the required app directories in the correct locations
based on the users OS.
"""
import sys
from pathlib import Path, PosixPath
from typing import Final, Union

from platformdirs import PlatformDirs

_YT_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(
    appname="yawning_titan", appauthor="DSTL"
)

if sys.platform == "win32":
    _YT_USER_DIRS: Final[Union[Path, PosixPath]] = (
        Path.home() / "DSTL" / "yawning_titan"
    )
else:
    _YT_USER_DIRS: Final[Union[Path, PosixPath]] = Path.home() / "yawning_titan"


def data_dir() -> Path:
    """The path to the app data directory as an instance of pathlib.Path."""
    dir_path = _YT_PLATFORM_DIRS.user_data_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def config_dir() -> Path:
    """The path to the app config directory as an instance of pathlib.Path."""
    if sys.platform == "win32":
        dir_path = _YT_PLATFORM_DIRS.user_data_path / "config"
    else:
        dir_path = _YT_PLATFORM_DIRS.user_config_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def log_dir() -> Path:
    """The path to the app log directory as an instance of pathlib.Path."""
    if sys.platform == "win32":
        dir_path = _YT_PLATFORM_DIRS.user_data_path / "logs"
    else:
        dir_path = _YT_PLATFORM_DIRS.user_log_path
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def docs_dir() -> Path:
    """The path to the app docs directory as an instance of pathlib.Path."""
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "docs"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def db_dir() -> Path:
    """The path to the app db directory as an instance of pathlib.Path."""
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "db"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def app_images_dir() -> Path:
    """The path to the app images directory as an instance of pathlib.Path."""
    dir_path = _YT_PLATFORM_DIRS.user_data_path / "app_images"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def notebooks_dir() -> Path:
    """
    The path to the users notebooks directory as an instance of pathlib.Path.

    Users notebooks are stored at: ~/DSTL/yawning_titan/notebooks.
    """
    dir_path = _YT_USER_DIRS / "notebooks"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def game_modes_dir() -> Path:
    """
    The path to the users game modes directory as an instance of pathlib.Path.

    Users game modes are stored at: ~/DSTL/yawning_titan/game_modes.
    """
    dir_path = _YT_USER_DIRS / "game_modes"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def images_dir() -> Path:
    """
    The path to the users images directory as an instance of pathlib.Path.

    Users images are stored at: ~/DSTL/yawning_titan/images.
    """
    dir_path = _YT_USER_DIRS / "images"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def agents_dir() -> Path:
    """
    The path to the users agents directory as an instance of pathlib.Path.

    Users images are stored at: ~/DSTL/yawning_titan/agents.
    """
    dir_path = _YT_USER_DIRS / "agents"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path