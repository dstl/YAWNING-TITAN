from pathlib import Path
from typing import Any, List

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig


def game_mode_path(game_mode_filename: str) -> str:
    """
    Generate path for game mode file.

    :param game_mode_filename: A string filename (including extension) of a game mode file in the `GAME_MODES_DIR`

    :return: a string representation of the full path to the `game_mode_filename`
    """
    return (GAME_MODES_DIR / game_mode_filename).as_posix()


def check_game_mode(game_mode_path: Path) -> bool:
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


def get_game_mode_file_paths(valid_only=False) -> List[Path]:
    """
    Select all game modes in the `GAME_MODES_DIR` matching criteria.

    :param: valid_only: whether to return only those game modes that pass the `GameModeConfig` validation check

    :return: a list of file Path objects representing game modes.
    """
    game_modes = [
        g for g in GAME_MODES_DIR.iterdir() if g.stem != "everything_off_config"
    ]
    if not valid_only:
        return game_modes
    return [g for g in game_modes if check_game_mode(g)]


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

    >>>test.txt -> exists
    >>>test(1).txt -> exists
    >>>test(2).txt -> new path
    """
    filename = path.stem
    extension = path.suffix
    parent = path.parent
    counter = 1

    while path.exists():
        path = parent / f"{filename}({counter}){extension}"
        counter += 1
    return path
