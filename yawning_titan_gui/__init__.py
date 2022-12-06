from pathlib import Path, PosixPath
from typing import Final, Union
from platformdirs import PlatformDirs


_YT_GUI_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(appname="yawning_titan_gui")
"""An instance of `PlatformDirs` set with appname='yawning_titan_gui'."""

def _static_dir() -> Union[Path, PosixPath]:
    dir_path = _YT_GUI_PLATFORM_DIRS.user_data_path / "static"
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

_YT_GUI_ROOT_DIR: Final[Path] = Path(__file__).parent.resolve()
DEFAULT_GAME_MODE: Final[Path] = "everything_off_config.yaml"

STATIC_DIR: Final[Union[Path, PosixPath]] = _static_dir()
"""The path to the app static directory as an instance of `Path` or `PosixPath`, depending on the OS."""

print("S",STATIC_DIR)