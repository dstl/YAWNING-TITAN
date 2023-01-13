from pathlib import Path
from typing import Final

_YT_GUI_ROOT_DIR: Final[Path] = Path(__file__).parent.resolve()
DEFAULT_GAME_MODE: Final[str] = "everything_off_config.yaml"
"""The filename of the game mode file to act as the base for all game modes """
