from pathlib import Path
from typing import Any, List

from django.urls import reverse
from yawning_titan import _YT_ROOT_DIR

from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
from yawning_titan_server.settings import DOCS_ROOT


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
            return None
        return getattr(cls, attr)(min, max)


class GameModeManager:
    """Wrapper over an instance of `~yawning_titan.game_modes.game_mode_db.GameModeDB` to provide helper functions to the GUI."""

    db: GameModeDB = GameModeDB()

    @classmethod
    def get_game_mode_data(cls):
        """Gather the doc metadata of all game mode objects adding a field `complete` to denote that a game mode is fully valid."""
        return [
            {**g.doc_metadata.to_dict(), "complete": g.validation.passed}
            for g in cls.db.all()
        ]


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

def get_docs_sections():
    return [p.stem for p in DOCS_ROOT.iterdir() if p.suffix == ".html"]

def get_url(url_name: str,*args,**kwargs):
    """
    Wrapped implementation of Django's reverse url.

    A lookup that returns the url by name
    or empty string when the url does not exist.

    :param url_name: The name of the url string as defined in `urls.py`.

    :return: The full url string as defined in `urls.py`
    """
    try:
        return reverse(url_name,args=args,kwargs=kwargs)
    except Exception:
        return None
    
def get_url_dict(name:str,href:str):
    """return a dictionary with keys `name` and `href` to describe a url link element."""
    return {"name":name,"href":href}

def get_sidebar():
    default_sidebar = {
        "Documentation": [
            get_url_dict(n,get_url('docs',section=n)) for n in get_docs_sections()
        ],
        "Configuration": [
            get_url_dict(n,get_url(n)) for n in ["Manage game modes","Manage networks"] if get_url(n)
        ],
        "Training runs": [
            get_url_dict(n,get_url(n))for n in  ["Setup a training run", "View completed runs"] if get_url(n)
        ],
        "About": [
            get_url_dict(n,get_url(n)) for n in ["Contributors", "Report bug", "FAQ"] if get_url(n)
        ],
    }
    return default_sidebar