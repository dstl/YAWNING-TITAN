from pathlib import Path
from typing import Any, Dict, List

from django.urls import reverse

from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
from yawning_titan_server.settings import DOCS_ROOT

# from setup import version


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
            for network in cls.db.search(
                NetworkQuery.num_of_entry_nodes_between(min, max)
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
            for network in cls.db.search(
                NetworkQuery.num_of_high_value_nodes_between(min, max)
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
            for network in cls.db.search(NetworkQuery.num_of_nodes_between(min, max))
        ]

    @classmethod
    def filter(cls, filters: Dict[str, dict]) -> List[str]:
        """Call the filter method for the appropriate attribute.

        :param attribute: the string name of a network attribute to filter
        :param min: the minimum value of the attribute (inclusive)
        :param max: the maximum value of the attribute (inclusive)
        """
        networks: List[set] = []
        for k, v in filters.items():
            attr = f"filter_{k}"
            print("ATTR = ", attr)
            if hasattr(cls, attr):
                networks.append(set(getattr(cls, attr)(v["min"], v["max"])))
        if len(networks) == 1:
            return list(networks[0])
        return list(networks[0].intersection(*[networks][1:]))


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

    # @classmethod
    # def filter(cls, filters: dict):
    #     """Filter a game mode using a dictionary of ranges or values."""
    #     item_dict = GameMode().to_legacy_dict()
    #     queries = []
    #     for name, filter in filters.items():
    #         if isinstance(item_dict[name], (FloatItem, IntItem)):
    #             queries.append(item_dict[name].query.bt(filter["min"], filter["max"]))
    #         else:
    #             queries.append((item_dict[name].query == filter))
    #     _filter = reduce(and_, queries)
    #     return cls.db.search(_filter)


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
    """Return names of each section of the sphinx documentation."""
    docs_dir = DOCS_ROOT / "source"
    if docs_dir.exists():
        return [p.stem for p in docs_dir.iterdir() if p.suffix == ".html"]
    return []


def get_url(url_name: str, *args, **kwargs):
    """
    Wrapped implementation of Django's reverse url.

    A lookup that returns the url by name
    or empty string when the url does not exist.

    :param url_name: The name of the url string as defined in `urls.py`.

    :return: The full url string as defined in `urls.py`
    """
    try:
        return reverse(url_name, args=args, kwargs=kwargs)
    except Exception:
        return None


def get_url_dict(name: str, href: str, new_tab: bool = False):
    """Return a dictionary with keys `name` and `href` to describe a url link element."""
    return {"name": name, "href": href, "new_tab": new_tab}


def get_toolbar(current_page_title: str = None):
    """Get toolbar information for the current page title."""
    default_toolbar = {
        "home": {"icon": "bi-house-door", "title": "Home"},
        "doc": {
            "icon": "bi-file-earmark",
            "title": "Documentation",
            "links": [
                get_url_dict(n, get_url("Documentation", section=n))
                for n in get_docs_sections()
            ],
        },
        "manage-game_modes": {"icon": "bi-gear", "title": "Manage game modes"},
        "manage-networks": {"icon": "bi-diagram-2", "title": "Manage networks"},
        "run-view": {"icon": "bi-play", "title": "Run session"},
        "about": {
            "icon": "bi-question-lg",
            "title": "About",
            "links": [
                get_url_dict(n, href, True)
                for n, href in zip(
                    ["Contributors", "Discussions", "Report bug", "Feature request"],
                    [
                        "https://github.com/dstl/YAWNING-TITAN/graphs/contributors",
                        "https://github.com/dstl/YAWNING-TITAN/discussions",
                        "https://github.com/dstl/YAWNING-TITAN/issues/new?assignees=&labels=bug&template=bug_report.md&title=[BUG]",
                        "https://github.com/dstl/YAWNING-TITAN/issues/new?assignees=&labels=feature_request&template=feature_request.md&title=[REQUEST]",
                    ],
                )
            ],
            "info": [f"Version: {version()}"],
        },
    }
    for id, info in default_toolbar.items():
        default_toolbar[id]["active"] = info["title"] == current_page_title
    return default_toolbar


def version() -> str:
    """
    Gets the version from the `VERSION` file.

    :return: The version string.
    """
    with open("VERSION", "r") as file:
        return file.readline()
