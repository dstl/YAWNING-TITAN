import shutil
from pathlib import Path
from typing import Any, Dict, List

from yawning_titan import GAME_MODES_DIR
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema


class NetworkManager:
    """Handle all interfacing with Yawning Titan networks in :attribute: `network_db` and their info for the GUI session."""

    network_db: NetworkDB = NetworkDB()

    @classmethod
    def filter_entry_nodes(cls, min, max) -> List[str]:
        """
        Generate a list of ``uuids`` corresponding to networks that have a number of entry nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid
            for network in cls.network_db.search(
                NetworkSchema.ENTRY_NODES.len_bt(min, max)
            )
        ]

    @classmethod
    def filter_high_value_nodes(cls, min, max) -> List[str]:
        """
        Generate a list of ``uuids`` corresponding to networks that have a number of high value nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid
            for network in cls.network_db.search(
                NetworkSchema.HIGH_VALUE_NODES.len_bt(min, max)
            )
        ]

    @classmethod
    def filter_network_nodes(cls, min, max) -> List[str]:
        """
        Generate a list of ``uuids`` corresponding to networks that have a number of nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid
            for network in cls.network_db.search(NetworkSchema.MATRIX.len_bt(min, max))
        ]

    @classmethod
    def filter(cls, attribute: str, min, max) -> List[str]:
        """Call the filter method for the appropriate attribute.

        :param attribute: the string name of a network attribute to filter
        :param min: the minimum value of the attribute (inclusive)
        :param max: the maximum value of the attribute (inclusive)
        """
        attr = f"filter_{attribute}"
        if not hasattr(cls, attr):
            return None
        return getattr(cls, attr)(min, max)


class GameModeManager:
    """TBC."""

    db: GameModeDB = GameModeDB()

    @classmethod
    def get_game_mode_data(cls):
        """TBC."""
        return [
            {**g.doc_metadata.to_dict(), "complete": g.validation.passed}
            for g in cls.db.all()
        ]


class gg:
    """Handle all interfacing with Yawning Titan game modes in :attribute: `root_dir` and their info for the GUI session."""

    game_modes: Dict[str, Dict[str, Any]] = {}
    protected_game_mode_filenames: List[str] = ["base_config.yaml"]
    root_dir: Path = GAME_MODES_DIR

    # Getters

    @classmethod
    def get_game_mode_path(cls, game_mode_filename: str) -> Path:
        """
        Generate path for game mode file.

        :param game_mode_filename: A string filename (including extension) of a game mode file in the :attribute: `root_dir`

        :return: a string representation of the full path to the `game_mode_filename`
        """
        path = cls.root_dir / game_mode_filename
        if path.exists():
            return path
        else:
            raise FileNotFoundError(
                f"Game mode {game_mode_filename} does not exist in {cls.root_dir}"
            )

    @classmethod
    def load_game_mode(
        cls, game_mode_path: Path, info_only: bool = False, valid_only: bool = False
    ) -> None:
        """Create a summary of information related to each game mode available in :attribute: `root_dir`."""
        game_mode = GameMode()
        game_mode.set_from_yaml(game_mode_path, infer_legacy=True)
        if valid_only and not cls.check_game_mode(game_mode):
            return
        cls.game_modes[game_mode_path.name] = {
            "name": game_mode_path.stem,
            "description": "description",  # TODO: allow the description to be set on point of creation or got from tinydb.
            "protected": game_mode_path.stem in cls.protected_game_mode_filenames,
            "complete": cls.check_game_mode(game_mode),
        }
        if info_only:
            cls.game_modes[game_mode_path.name]["config_class"] = None
        else:
            cls.game_modes[game_mode_path.name]["config_class"] = game_mode

    @classmethod
    def load_game_modes(cls, info_only: bool = False, valid_only: bool = False) -> None:
        """Create a summary of information related to each game mode available in :attribute: `root_dir`."""
        cls.game_modes = {}
        game_mode_paths = cls.root_dir.iterdir()
        for path in game_mode_paths:
            cls.load_game_mode(path, info_only, valid_only)

    @classmethod
    def get_game_mode(cls, game_mode_filename: str) -> GameMode:
        """
        Get an instance of :class: `~yawning_titan.game_modes.game_mode _config.GameModeConfig` corresponding to the :param: `game_mode_filename`.

        :param game_mode_filename: a file name and extension of a `~yawning_titan.game_modes.game_mode _config.GameModeConfig`
        :return: the instance of `~yawning_titan.game_modes.game_mode _config.GameModeConfig` populated with the data from :param: `game_mode_filename`
        """
        if game_mode_filename not in cls.game_modes:
            cls.load_game_mode(
                game_mode_path=cls.get_game_mode_path(game_mode_filename)
            )
        if cls.game_modes[game_mode_filename]["config_class"] is None:
            game_mode = GameMode()
            game_mode.set_from_yaml(
                cls.get_game_mode_path(game_mode_filename), infer_legacy=True
            )
            cls.game_modes[game_mode_filename]["config_class"] = game_mode
        return cls.game_modes[game_mode_filename]["config_class"]

    # Checkers

    @classmethod
    def check_game_mode(cls, game_mode: GameMode) -> bool:
        """
        Check that a game mode path can construct a valid GameModeConfig object.

        :return: a boolean True/False value indicating whether the game mode passes the validation checks in `GameModeConfig`
        """
        return game_mode.validation.passed

    # Setters

    @classmethod
    def create_game_mode(cls, game_mode_filename: str) -> None:
        """
        Create a new entry in :attr: `GameModeManager.game_modes` to represent a potential new new Yawning Titan game mode config file.

        :param game_mode_filename: a file name and extension for a new Yawning Titan game mode config file
        """
        new_game_mode_path = uniquify(cls.root_dir / game_mode_filename)
        cls.game_modes[game_mode_filename] = {
            "name": new_game_mode_path.stem,
            "description": None,
            "protected": False,
            "config_class": True,
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
        source_game_mode_path = cls.root_dir / source_game_mode_filename
        new_game_mode_path = uniquify(cls.root_dir / new_game_mode_filename)
        shutil.copy(source_game_mode_path, new_game_mode_path)
        cls.game_modes[new_game_mode_filename] = cls.game_modes[
            source_game_mode_filename
        ]
        cls.game_modes[new_game_mode_filename].update({"name": new_game_mode_path.stem})

    @classmethod
    def delete_game_mode(cls, game_mode_filename: str) -> None:
        """
        Delete a unprotected Yawning Titan game mode. If the game mode is in the list of protected game modes; do nothing.

        :param game_mode_filename: a file name and extension for a new Yawning Titan game mode config file
        """
        path = cls.root_dir / game_mode_filename
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
