"""Provides an API for the ``game_mode.json`` TinyDB file, and a Schema class that defines the game_mode DB fields."""
from __future__ import annotations

import os
from logging import getLogger
from pathlib import Path
from typing import Final, List, Optional, Union

from tinydb import TinyDB
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.config import _LIB_CONFIG_ROOT_PATH
from yawning_titan.db.compatibility_query import (
    EntryNodeCompatibilityQuery,
    HighValueNodeCompatibilityQuery,
    NetworkCompatibilityQuery,
    NetworkNodeCompatibilityQuery,
)
from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.game_modes.game_mode import GameMode

__all__ = ["GameModeDB", "GameModeSchema"]

_LOGGER = getLogger(__name__)


class GameModeSchema:
    """
    A schema-like class that defines the game_mode DB fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:~`yawning_titan.game_modes.game_mode.GameMode` class.

    :Example:

    >>> from yawning_titan.game_modes.game_mode_db import GameModeDB, GameModeSchema
    >>> db = GameModeDB()
    >>> game_modes = db.search(GameModeSchema.NODE_COUNT.min(18))
    """

    NETWORK_NODES: Final[
        NetworkNodeCompatibilityQuery
    ] = NetworkNodeCompatibilityQuery().game_rules.network_compatibility.node_count
    """Mapped to :attr:`~yawning_titan.game_modes.game_mode.GameMode.game_rules.network_compatibility.node_count`."""

    ENTRY_NODES: Final[
        EntryNodeCompatibilityQuery
    ] = EntryNodeCompatibilityQuery().game_rules.network_compatibility.entry_node_count
    """Mapped to :attr:`~yawning_titan.game_modes.game_mode.GameMode.game_rules.network_compatibility.entry_node_count``."""

    HIGH_VALUE_NODES: Final[
        HighValueNodeCompatibilityQuery
    ] = (
        HighValueNodeCompatibilityQuery().game_rules.network_compatibility.high_value_node_count
    )
    """Mapped to :attr:`~yawning_titan.game_modes.game_mode.GameMode.game_rules.network_compatibility.high_value_node_count`."""

    NETWORK_COMPATIBILITY: Final[
        NetworkCompatibilityQuery
    ] = NetworkCompatibilityQuery().game_rules.network_compatibility
    """Mapped to :attr:`~yawning_titan.game_modes.game_mode.GameMode.game_rules.network_compatibility`."""

    CONFIGURATION: Final[YawningTitanQuery] = YawningTitanQuery()
    """Use this to access the full schema of the database structured in the same nested format as :class:~`yawning_titan.game_modes.game_mode.GameMode`."""


class GameModeDB:
    """
    The :class:`~yawning_titan.config.game_modes.GameModeDB` class extends :class:`~yawning_titan.db.YawningTitanDB`.

    The below code blocks demonstrate how to use the :class:`~yawning_titan.config.game_modes.GameModeDB` class.

    - Instantiate the GameMode DB:

        .. code:: python

            >>> from yawning_titan.game_modes.game_mode_db import GameModeDB, GameModeSchema
            >>> db = GameModeDB()

    - Search for all game modes that work with a minimum of 18 nodes in the game_mode:

        .. code:: python

            >>> db.search(GameModeSchema.NODE_COUNT.min(18))
    """

    def __init__(self):
        self._db = YawningTitanDB("game_modes")
        self.reset_default_game_modes_in_db()

    def __enter__(self) -> GameModeDB:
        return GameModeDB()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def _doc_to_game_mode(cls, doc: Document):
        """Convert the document.

        Converts a :class:`tinydb.table.Document` from the :class:`~yawning_titan.config.game_modes.GameModeDB` to an instance
        of :class:~yawning_titan.game_modes.game_mode.GameMode`.

        :param doc: A :class:`tinydb.table.Document`.
        :return: The doc as a :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        doc["_doc_metadata"] = DocMetadata(**doc["_doc_metadata"])
        game_mode: GameMode = GameMode()
        game_mode.set_from_dict(doc)
        return game_mode

    def insert(
        self,
        game_mode: GameMode,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> GameMode:
        """
        Insert a :class:`~yawning_titan.game_modes.game_mode.GameMode` into the DB as ``.json``.

        :param game_mode: An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The inserted :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        game_mode.doc_metadata.update(name, description, author)
        self._db.insert(
            game_mode.to_dict(
                json_serializable=True, include_none=True, values_only=True
            )
        )

        return game_mode

    def all(self) -> List[GameMode]:
        """
        Get all :class:`~yawning_titan.game_modes.game_mode.GameMode` from the game mode DB.

        :return: A :class:`list` of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        return [self._doc_to_game_mode(doc) for doc in self._db.all()]

    def get(self, uuid: str) -> Union[GameMode, None]:
        """
        Get a game_mode config document from its uuid.

        :param uuid: A target document uuid.
        :return: The game_mode config document as an instance of
            :class:~yawning_titan.game_modes.game_mode.GameMode` if the uuid exists,
            otherwise :class:`None`.
        """
        # self._db.db.clear_cache()
        doc = self._db.get(uuid)
        if doc:
            return self._doc_to_game_mode(doc)

    def search(self, query: YawningTitanQuery) -> List[GameMode]:
        """
        Searches the :class:`~yawning_titan.game_modes.game_mode.GameMode` with a :class:`GameModeSchema` query.

        :param query: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: A :class:`list` of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        game_mode_configs = []
        for doc in self._db.search(query):
            game_mode_configs.append(self._doc_to_game_mode(doc))
        return game_mode_configs

    def count(self, cond: Optional[QueryInstance] = None) -> int:
        """
        Count how many docs are in the db. Extends :class:`tinydb.table.Table.count`.

        A :class:`~yawning_titan.db.query.YawningTitanQuery` can be used to
        filter the count.

        :param cond: An optional :class:`~yawning_titan.db.query.YawningTitanQuery`.
            Has a default value of ``None``.
        :return: The number of docs counted.
        """
        if cond:
            return self._db.count(cond)
        return len(self._db.all())

    def update(
        self,
        game_mode: GameMode,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> GameMode:
        """
        Update a :class:`~yawning_titan.game_modes.game_mode.GameMode`. in the db.

        :param game_mode: An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The updated :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        # Update the configs metadata
        game_mode.doc_metadata.update(name, description, author)
        # Perform the update and retrieve the returned doc
        doc = self._db.update(
            game_mode.to_dict(json_serializable=True),
            game_mode.doc_metadata.uuid,
            name,
            description,
            author,
        )
        if doc:
            # Update the configs metadata created at
            game_mode.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return game_mode

    def upsert(
        self,
        game_mode: GameMode,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> GameMode:
        """
        Upsert a :class:`~yawning_titan.game_modes.game_mode.GameMode`. in the db.

        :param game_mode: An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The upserted :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        game_mode.doc_metadata.update(name, description, author)
        doc = self._db.upsert(
            game_mode.to_dict(json_serializable=True),
            game_mode.doc_metadata.uuid,
            name,
            description,
            author,
        )

        # Update the configs metadata created at
        if doc and "updated_at" in doc["_doc_metadata"]:
            game_mode.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return game_mode

    def remove(self, game_mode: GameMode) -> List[str]:
        """
        Remove a :class:`~yawning_titan.game_modes.game_mode.GameMode`. from the db.

        :param game_mode: An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        :return: The uuid of the removed :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        self._db.remove(game_mode.doc_metadata.uuid)

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """
        Remove :class:`~yawning_titan.game_modes.game_mode.GameMode`. from the db that match the query.

        :param cond: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: The list of uuids of the removed :class:`~yawning_titan.game_modes.game_mode.GameMode`.
        """
        return self._db.remove_by_cond(cond)

    def reset_default_game_modes_in_db(self):
        """
        Reset the default game_mode in the db.

        Achieves this by loading the default
        `yawning_titan/game_modes/_package_data/game_mode.json` db file into TinyDB,
        then iterating over all docs and forcing an update of each one in the main
        game_modes db from its uuid if they do not match.
        """
        # Obtain the path to the default db file in package data
        self._db.db.clear_cache()
        game_mode_root = Path(__file__).parent.resolve()
        default_game_mode_path = os.path.join(
            game_mode_root, "_package_data", "game_modes.json"
        )

        # Load the default db file into TinyDB
        default_db = TinyDB(default_game_mode_path)

        # Iterate over all default game_modes, and force an update in the
        # main GameModeDB by uuid.
        for game_mode in default_db.all():
            uuid = game_mode["_doc_metadata"]["uuid"]
            name = game_mode["_doc_metadata"]["name"]

            # Get the matching game_mode from the game_modes db
            db_game_mode = self.get(uuid)

            # If the game_mode doesn't match the default, or it doesn't exist,
            # perform an upsert.
            if db_game_mode:
                reset = (
                    db_game_mode.to_dict(
                        json_serializable=True, include_none=True, values_only=True
                    )
                    != game_mode
                )
            else:
                reset = True
            if reset:
                self._db.db.upsert(game_mode, DocMetadataSchema.UUID == uuid)
                _LOGGER.info(
                    f"Reset default game_mode '{name}' in the "
                    f"{self._db.name} db with uuid='{uuid}'."
                )

        # Clear the default db cache and close the file.
        default_db.clear_cache()
        default_db.close()

    def rebuild_db(self):
        """
        Rebuild the db.

        Actions taken:
            - clear the query cache
            - truncate the db
            - call :func:`~yawning_titan.game_modes.game_mode_db.GameModeDB.reset_default_game_modes_in_db`

        .. warning::

                This function completely rebuilds the database. Any custom game_modes
                saved in the db will be lost. The default game_modes can be reset
                using the :func:`~yawning_titan.game_modes.game_mode_db.GameModeDB.reset_default_game_modes_in_db`
                function.
        """
        _LOGGER.info(f"Rebuilding the {self._db.name} db.")
        self._db.db.clear_cache()
        self._db.db.truncate()
        self.reset_default_game_modes_in_db()

    def add_yaml_game_modes_to_db(self, directory: Path = None):
        """Add all yaml game modes in a given directory to the database.

        :param directory: The directory containing the files to add as a Path.
        """
        if directory is None:
            directory = _LIB_CONFIG_ROOT_PATH / "_package_data" / "game_modes"
        for game_mode_path in directory.iterdir():
            game_mode = GameMode()
            game_mode.set_from_yaml(game_mode_path, infer_legacy=True)
            self.insert(game_mode, name=game_mode_path.stem)


def default_game_mode() -> GameMode:
    """
    The default Yawning Titan game mode.

    :return: An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`.
    """
    with GameModeDB() as db:
        return db.get("900a704f-6271-4994-ade7-40b74d3199b1")
