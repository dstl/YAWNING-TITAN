from pathlib import Path
from typing import Any, List

from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema


class NetworkManager:
    """Handle all interfacing with Yawning Titan networks in :attribute: `network_db` and their info for the GUI session."""

    db: NetworkDB = NetworkDB()
    current_network: Network = None

    @classmethod
    def filter_entry_nodes(cls, min, max) -> List[str]:
        """
        Generate a list of ``uuids`` corresponding to networks that have a number of entry nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid
            for network in cls.db.search(NetworkSchema.ENTRY_NODES.len_bt(min, max))
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
            for network in cls.db.search(
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
            for network in cls.db.search(NetworkSchema.MATRIX.len_bt(min, max))
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
            print("OOPS")
            return None
        return getattr(cls, attr)(min, max)

    @classmethod
    def get_network_data(cls) -> List[dict]:
        """Gather the doc metadata of all network objects."""
        return [network.doc_metadata for network in cls.db.all()]


class GameModeManager:
    """Wrapper over an instance of `~yawning_titan.game_modes.game_mode_db.GameModeDB` to provide helper functions to the GUI."""

    db: GameModeDB = GameModeDB()

    @classmethod
    def get_game_mode_data(cls, valid_only: bool = False) -> List[dict]:
        """Gather the doc metadata of all game mode objects adding a field `valid` to denote that a game mode is fully valid.

        :param valid_only: return only valid game modes.
        """
        game_modes = [
            {**g.doc_metadata.to_dict(), "valid": g.validation.passed}
            for g in cls.db.all()
        ]
        if not valid_only:
            return game_modes
        return [g for g in game_modes if g["valid"]]


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
