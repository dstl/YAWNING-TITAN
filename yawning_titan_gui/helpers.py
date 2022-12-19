import shutil
from pathlib import Path
from typing import Any, Dict, List

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig


class GameModeManager:
    """Handle all interfacing with Yawning Titan game modes in :var: `GAME_MODES_DIR` and their info for the GUI session."""

    game_modes: Dict[str, Dict[str, Any]] = {}
    protected_game_mode_filenames = ["base_config.yaml"]

    # Getters

    @staticmethod
    def get_game_mode_path(game_mode_filename: str) -> Path:
        """
        Generate path for game mode file.

        :param game_mode_filename: A string filename (including extension) of a game mode file in the `GAME_MODES_DIR`

        :return: a string representation of the full path to the `game_mode_filename`
        """
        return GAME_MODES_DIR / game_mode_filename

    @classmethod
    def load_game_mode_info(cls) -> None:
        """Create a summary of information related to each game mode available in :var: `GAME_MODES_DIR`."""
        cls.game_modes = {
            path.name: {
                "name": path.stem,
                "description": "description",  # TODO: allow the description to be set on point of creation or got from tinydb.
                "protected": path.stem in cls.protected_game_mode_filenames,
                "complete": cls.check_game_mode(path),
            }
            for path in cls.get_game_mode_file_paths(valid_only=False)
        }

    @classmethod
    def get_game_mode(cls, game_mode_filename: str) -> GameModeConfig:
        """
        Get an instance of :class: `~yawning_titan.config.game_config.game_mode_config.GameModeConfig` corresponding to the :param: `game_mode_filename`.

        :param game_mode_filename: a file name and extension of a `~yawning_titan.config.game_config.game_mode_config.GameModeConfig`
        :return: the instance of `~yawning_titan.config.game_config.game_mode_config.GameModeConfig` populated with the data from :param: `game_mode_filename`
        """
        return GameModeConfig.create_from_yaml(
            cls.get_game_mode_path(game_mode_filename)
        )

    @classmethod
    def get_game_mode_file_paths(cls, valid_only=False) -> List[Path]:
        """
        Select all game modes in the `GAME_MODES_DIR` matching criteria.

        :param: valid_only: whether to return only those game modes that pass the :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>` validation check

        :return: a list of file Path objects representing game modes.
        """
        game_modes = [
            g for g in GAME_MODES_DIR.iterdir() if g.stem != "everything_off_config"
        ]
        if not valid_only:
            return game_modes
        return [g for g in game_modes if cls.check_game_mode(g)]

    # Checkers

    @classmethod
    def check_game_mode(cls, game_mode_path: Path) -> bool:
        """
        Check that a game mode path can construct a valid GameModeConfig object.

        :param: game_mode_path: A pathlib `Path` object representing a Yawning Titan game mode

        :return: a boolean True/False value indicating whether the game mode passes the validation checks in `GameModeConfig`
        """
        try:
            GameModeConfig.create_from_yaml(game_mode_path)
            return True
        except Exception:
            return False

    # Setters

    @classmethod
    def create_game_mode(cls, game_mode_filename: str) -> None:
        """
        Create a new entry in :attr: `GameModeManager.game_modes` to represent a potential new new Yawning Titan game mode config file.

        :param game_mode_filename: a file name and extension for a new Yawning Titan game mode config file
        """
        new_game_mode_path = uniquify(GAME_MODES_DIR / game_mode_filename)
        cls.game_modes[game_mode_filename] = {
            "name": new_game_mode_path.stem,
            "description": None,
            "protected": False,
            "complete": False,
        }

    @classmethod
    def create_game_mode_from(
        cls, source_game_mode_filename: str, new_game_mode_filename: str
    ) -> None:
        """
        Create a duplicate of a Yawning Titan game mode config file and save it under a new name.

        :param source_game_mode_filename: a file name and extension for an existing Yawning Titan game mode config file
        :param new_game_mode_filename: a file name and extension for a new Yawning Titan game mode config file
        """
        source_game_mode_path = GAME_MODES_DIR / source_game_mode_filename
        new_game_mode_path = uniquify(GAME_MODES_DIR / new_game_mode_filename)
        shutil.copy(source_game_mode_path, new_game_mode_path)

    @classmethod
    def delete_game_mode(cls, game_mode_filename: str) -> None:
        """
        Delete a unprotected Yawning Titan game mode. If the game mode is in the list of protected game modes; do nothing.

        :param game_mode_filename: a file name and extension for a new Yawning Titan game mode config file
        """
        path = GAME_MODES_DIR / game_mode_filename
        if (
            path.exists()
            and game_mode_filename not in cls.protected_game_mode_filenames
        ):
            path.unlink()


def next_key(_dict: dict, key: int) -> Any:
    """
    Get the next key in a dictionary.

    Use key_index + 1 if there is a subsequent key
    otherwise return first key.

    :param: _dict: a dictionary object
    :param: key: the current key

    :return: the subsequent key in the dictionary after `key`
    """
    keys = list(_dict.keys())
    key_index = keys.index(key)
    if key_index < (len(keys) - 1):
        return keys[key_index + 1]
    return keys[0]


def uniquify(path: Path) -> Path:
    """
    Create a unique file path from a proposed path by adding a numeral to the filename.

    Transforms the input `Path` object by iteratively adding numerals to the end
    of the filename until the proposed path does not exist.

    :param path: a `pathlib.Path` object to convert to a unique path

    :return: The transformed path object.

    :Example:

    >>> test.txt -> exists
    >>> test(1).txt -> exists
    >>> test(2).txt -> new path
    """
    filename = path.stem
    extension = path.suffix
    parent = path.parent
    counter = 1

    while path.exists():
        path = parent / f"{filename}({counter}){extension}"
        counter += 1
    return path
