"""Provides an API for the ``network.json`` TinyDB file, and a Schema class that defines the network DB fields."""
from __future__ import annotations

import os
from logging import getLogger
from pathlib import Path
from typing import Final, List, Optional, Union

import numpy as np
from tinydb import TinyDB
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.network.network_config import NetworkConfig

__all__ = ["NetworkDB", "NetworkSchema"]

_LOGGER = getLogger(__name__)


class NetworkSchema:
    """
    A schema-like class that defines the network DB fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:`~yawning_titan.network.network_config.NetworkConfig` class.

    :Example:

    >>> from yawning_titan.network.network_db import NetworkDB, NetworkSchema
    >>> db = NetworkDB()
    >>> network_configs = db.search(NetworkSchema.MATRIX.len_le(18))
    """

    MATRIX: Final[YawningTitanQuery] = YawningTitanQuery().matrix
    """Mapped to :attr:`yawning_titan.network.network_config.NetworkConfig.matrix`."""
    POSITIONS: Final[YawningTitanQuery] = YawningTitanQuery().positions
    """Mapped to :attr:`yawning_titan.network.network_config.NetworkConfig.positions`."""
    ENTRY_NODES: Final[YawningTitanQuery] = YawningTitanQuery().entry_nodes
    """Mapped to :attr:`yawning_titan.network.network_config.NetworkConfig.entry_nodes`."""
    VULNERABILITIES: Final[YawningTitanQuery] = YawningTitanQuery().vulnerabilities
    """Mapped to :attr:`yawning_titan.network.network_config.NetworkConfig.vulnerabilities`."""
    HIGH_VALUE_NODES: Final[YawningTitanQuery] = YawningTitanQuery().high_value_nodes
    """Mapped to :attr:`yawning_titan.network.network_config.NetworkConfig.high_value_nodes`."""


class NetworkDB:
    """
    The :class:`~yawning_titan.db.network.NetworkDB` class extends :class:`~yawning_titan.db.YawningTitanDB`.

    The below code blocks demonstrate how to use the :class:`~yawning_titan.db.network.NetworkDB` class.

    - Instantiate the Network DB:

        .. code:: python

            >>> from yawning_titan.network.network_db import NetworkDB, NetworkSchema
            >>> db = NetworkDB()

    - Search for all network configs that have "1" as an entry node:

        .. code:: python

            >>> db.search(NetworkSchema.ENTRY_NODES.all(["1"]))

    - Search for all network configs that have "1" as both an entry node and a high value node:

        .. code:: python

            >>> query = (NetworkSchema.ENTRY_NODES.all(["1"])) and (NetworkSchema.HIGH_VALUE_NODES.all(["1"]))
            >>> db.search(query)

    - Search for all network configs that have at least 3 high value nodes

            .. code:: python

            >>> db.search(NetworkSchema.ENTRY_NODES.len_ge(3))

    """

    def __init__(self):
        self._db = YawningTitanDB("network")
        self.reset_default_networks_in_db()

    @classmethod
    def _doc_to_network_config(cls, doc: Document):
        """Convert the document.

        Converts a :class:`tinydb.table.Document` from the :class:`~yawning_titan.db.network.NetworkDB` to an instance
        of :class:`~yawning_titan.network.network_config.NetworkConfig`.

        :param doc: A :class:`tinydb.table.Document`.
        :return: The doc as a :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        doc["matrix"] = np.array(doc["matrix"])
        doc["_doc_metadata"] = DocMetadata(**doc["_doc_metadata"])
        return NetworkConfig(**doc)

    def insert(
        self,
        network_config: NetworkConfig,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> NetworkConfig:
        """
        Insert a :class:`~yawning_titan.network.network_config.NetworkConfig` into the DB as ``.json``.

        :param network_config: An instance of :class:`~yawning_titan.network.network_config.NetworkConfig`
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The inserted :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        network_config.doc_metadata.update(name, description, author)
        self._db.insert(
            network_config.to_dict(json_serializable=True, include_none=False)
        )

        return network_config

    def all(self) -> List[NetworkConfig]:
        """
        Get all :class:`~yawning_titan.network.network_config.NetworkConfig` from the network DB.

        :return: A :py:classs:`list` of :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        return [self._doc_to_network_config(doc) for doc in self._db.all()]

    def get(self, uuid: str) -> Union[NetworkConfig, None]:
        """
        Get a network config document from its uuid.

        :param uuid: A target document uuid.
        :return: The network config document as an instance of
            :class:`~yawning_titan.network.network_config.NetworkConfig` if the uuid exists,
            otherwise :py:class:`None`.
        """
        doc = self._db.get(uuid)
        if doc:
            return self._doc_to_network_config(doc)

    def search(self, query: YawningTitanQuery) -> List[NetworkConfig]:
        """
        Searches the :class:`~yawning_titan.network.network_config.NetworkConfig` with a :class:`NetworkSchema` query.

        :param query: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: A :py:class:`list` of :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        network_configs = []
        for doc in self._db.search(query):
            network_configs.append(self._doc_to_network_config(doc))
        return network_configs

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
        network_config: NetworkConfig,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> NetworkConfig:
        """
        Update a :class:`~yawning_titan.network.network_config.NetworkConfig`. in the db.

        :param network_config: An instance of :class:`~yawning_titan.network.network_config.NetworkConfig`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The updated :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        # Update the configs metadata
        network_config.doc_metadata.update(name, description, author)
        # Perform the update and retrieve the returned doc
        doc = self._db.update(
            network_config.to_dict(json_serializable=True),
            network_config.doc_metadata.uuid,
            name,
            description,
            author,
        )
        if doc:
            # Update the configs metadata created at
            network_config.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return network_config

    def upsert(
        self,
        network_config: NetworkConfig,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> NetworkConfig:
        """
        Upsert a :class:`~yawning_titan.network.network_config.NetworkConfig`. in the db.

        :param network_config: An instance of :class:`~yawning_titan.network.network_config.NetworkConfig`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The upserted :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        network_config.doc_metadata.update(name, description, author)
        doc = self._db.upsert(
            network_config.to_dict(json_serializable=True),
            network_config.doc_metadata.uuid,
            name,
            description,
            author,
        )

        # Update the configs metadata created at
        if doc and "updated_at" in doc["_doc_metadata"]:
            network_config.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return network_config

    def remove(self, network_config: NetworkConfig) -> List[str]:
        """
        Remove a :class:`~yawning_titan.network.network_config.NetworkConfig`. from the db.

        :param network_config: An instance of :class:`~yawning_titan.network.network_config.NetworkConfig`.
        :return: The uuid of the removed :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        self._db.remove(network_config.doc_metadata.uuid)

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """
        Remove :class:`~yawning_titan.network.network_config.NetworkConfig`. from the db that match the query.

        :param cond: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: The list of uuids of the removed :class:`~yawning_titan.network.network_config.NetworkConfig`.
        """
        return self._db.remove_by_cond(cond)

    def reset_default_networks_in_db(self):
        """
        Reset the default networks in the db.

        Achieves this by loading the default
        `yawning_titan/network/_package_data/network.json` db file into TinyDB,
        then iterating over all docs and forcing an update of each one in the main
        network db from its uuid if they do not match.
        """
        # Obtain the path to the default db file in package data
        self._db.db.clear_cache()
        network_root = Path(__file__).parent.resolve()
        default_network_path = os.path.join(
            network_root, "_package_data", "network.json"
        )

        # Load the default db file into TinyDB
        default_db = TinyDB(default_network_path)

        # Iterate over all default networks, and force an update in the
        # main NetworkDB by uuid.
        for network in default_db.all():
            uuid = network["_doc_metadata"]["uuid"]
            name = network["_doc_metadata"]["name"]

            # Get the matching network from the  network db
            db_network = self.get(uuid)

            # If the network doesn't match the default, or it doesn't exist,
            # perform an upsert.
            if db_network:
                reset = (
                    db_network.to_dict(json_serializable=True, include_none=False)
                    != network
                )
            else:
                reset = True

            if reset:
                self._db.db.upsert(network, DocMetadataSchema.UUID == uuid)
                _LOGGER.info(
                    f"Reset default network '{name}' in the "
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
            - call :func:`~yawning_titan.network.network_db.NetworkDB.reset_default_networks_in_db`
        """
        _LOGGER.info(f"Rebuilding the {self._db.name} db.")
        self._db.db.clear_cache()
        self._db.db.truncate()
        self.reset_default_networks_in_db()
