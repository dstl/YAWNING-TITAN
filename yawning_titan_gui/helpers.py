import glob
import logging
import os
import sys
from pathlib import Path
from typing import Any, List

from django.http import HttpRequest, JsonResponse

from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
from yawning_titan.yawning_titan_run import YawningTitanRun
from yawning_titan_gui import STATIC_DIR, YT_RUN_TEMP_DIR
from yawning_titan_server.settings import STATIC_URL


class RunManager:
    gif = None

    @classmethod
    def run_yt(cls, *args, **kwargs):  # TODO: Move
        Path("spam.log").unlink()
        logger = logging.getLogger("yr_run")
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler("spam.log")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        kwargs["logger"] = logger
        with open("stdout.txt", "w+") as sys.stdout:
            run = YawningTitanRun(**kwargs)
        if kwargs["render"]:
            loop = ActionLoop(
                run.env,
                run.agent,
                episode_count=kwargs.get("num_episodes", run.total_timesteps),
            )
            loop.gif_action_loop(
                output_directory=YT_RUN_TEMP_DIR, save_gif=True, render_network=False
            )

    @classmethod
    def get_output(cls):
        output = {"stderr": "", "stdout": ""}
        with open("spam.log", "r") as f:
            try:
                lines = f.readlines()
                text = "<br>".join(lines)
                output["stderr"] = text
            except Exception as e:
                pass
        with open("stdout.txt", "r") as f:
            try:
                lines = f.readlines()
                text = "<br>".join(lines)
                output["stdout"] = text
            except Exception as e:
                pass
        dir = glob.glob(YT_RUN_TEMP_DIR.as_posix())
        gif_path = max(dir, key=os.path.getctime)
        output["gif"] = f"/{STATIC_URL}{Path(gif_path).name}"
        return output


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


def static_path_to_url(path: str):
    """"""
    print("PATH", path, STATIC_DIR.as_posix())
    return path
    # print("TESTxxxx",path.split(STATIC_DIR.as_posix())[1])
    # return path.split(STATIC_DIR.as_posix())[1]
