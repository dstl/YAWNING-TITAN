from pathlib import Path, PosixPath
from typing import Final, Union

from platformdirs import PlatformDirs

from yawning_titan import LOG_DIR

_YT_GUI_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(appname="yawning_titan_gui")
"""An instance of `PlatformDirs` set with appname='yawning_titan_gui'."""


def _static_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_GUI_PLATFORM_DIRS.user_data_path / "static"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _yt_run_temp_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_GUI_PLATFORM_DIRS.user_data_path / "static" / "yt_run"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _yt_gui_run_log() -> Union[Path, PosixPath]:
    dir_path = LOG_DIR / "yt_gui_run.log"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


_YT_GUI_ROOT_DIR: Final[Path] = Path(__file__).parent.resolve()

DEFAULT_GAME_MODE: Final[str] = "everything_off_config.yaml"
"""The filename of the game mode file to act as the base for all game modes """

STATIC_DIR: Final[Union[Path, PosixPath]] = _static_dir()
"""The path to the app static directory as an instance of `Path` or `PosixPath`, depending on the OS."""

# YT_RUN_TEMP_DIR: Final[Union[Path, PosixPath]] = _yt_run_temp_dir()
# """The path to the app temp directory for :class: `~yawning_titan.yawning_titan_run.YawningTitanRun` as an instance of `Path` or `PosixPath`, depending on the OS."""

YT_RUN_TEMP_DIR = _YT_GUI_ROOT_DIR / "static" / "gifs"

YT_GUI_RUN_LOG = LOG_DIR / "yt_gui_run.log"

YT_GUI_STDOUT = LOG_DIR / "stdout.txt"
