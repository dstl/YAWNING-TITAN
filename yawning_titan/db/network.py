"""Provides an API for the ``network.json`` TinyDB file, and a Schema class that defines the network DB fields."""
from __future__ import annotations

from typing import Final, List, Mapping, Optional, Union

import numpy as np
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.config.network_config import NetworkConfig
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.yawning_titan_db import YawningTitanDB

__all__ = ["NetworkDB", "NetworkSchema"]

from yawning_titan.db.query import YawningTitanQuery


class NetworkSchema:
    """
    A schema-like class that defines the network DB fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:`~yawning_titan.config.network_config.NetworkConfig` class.

    :Example:

    >>> from yawning_titan.db.network import NetworkDB, NetworkSchema
    >>> db = NetworkDB()
    >>> network_configs = db.search(NetworkSchema.MATRIX.len_le(18))
    """

    MATRIX: Final[YawningTitanQuery] = YawningTitanQuery().matrix
    """Mapped to :attr:`yawning_titan.config.network_config.NetworkConfig.matrix`."""
    POSITIONS: Final[YawningTitanQuery] = YawningTitanQuery().positions
    """Mapped to :attr:`yawning_titan.config.network_config.NetworkConfig.positions`."""
    ENTRY_NODES: Final[YawningTitanQuery] = YawningTitanQuery().entry_nodes
    """Mapped to :attr:`yawning_titan.config.network_config.NetworkConfig.entry_nodes`."""
    VULNERABILITIES: Final[YawningTitanQuery] = YawningTitanQuery().vulnerabilities
    """Mapped to :attr:`yawning_titan.config.network_config.NetworkConfig.vulnerabilities`."""
    HIGH_VALUE_NODES: Final[YawningTitanQuery] = YawningTitanQuery().high_value_nodes
    """Mapped to :attr:`yawning_titan.config.network_config.NetworkConfig.high_value_nodes`."""


class NetworkDB(YawningTitanDB):
    """
    The :class:`~yawning_titan.db.network.NetworkDB` class extends :class:`~yawning_titan.db.YawningTitanDB`.

    The below code blocks demonstrate how to use the :class:`~yawning_titan.db.network.NetworkDB` class.

    - Instantiate the Network DB:

        .. code:: python

            >>> from yawning_titan.db.network import NetworkDB, NetworkSchema
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
        super().__init__("network")

    @classmethod
    def _doc_to_network_config(cls, doc: Document):
        """Convert the document.

        Converts a :class:`tinydb.table.Document` from the :class:`~yawning_titan.db.network.NetworkDB` to an instance
        of :class:`~yawning_titan.config.network_config.NetworkConfig`.

        :param doc: A :class:`tinydb.table.Document`.
        :return: The doc as a :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        doc["matrix"] = np.array(doc["matrix"])
        doc["_doc_metadata"] = DocMetadata(**doc["_doc_metadata"])
        return NetworkConfig.create_from_args(**doc)

    def insert(
        self,
        network_config: NetworkConfig,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> NetworkConfig:
        """
        Insert a :class:`~yawning_titan.config.network_config.NetworkConfig` into the DB as ``.json``.

        :param network_config: An instance of :class:`~yawning_titan.config.network_config.NetworkConfig`
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The inserted :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        network_config.doc_metadata.update(name, description, author)
        super().insert(network_config.to_dict(json_serializable=True))

        return network_config

    def all(self) -> List[NetworkConfig]:
        """
        Get all :class:`~yawning_titan.config.network_config.NetworkConfig` from the network DB.

        :return: A :py:classs:`list` of :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        return [
            self._doc_to_network_config(doc) for doc in super().all()
        ]

    def get(self, uuid: str) -> Union[NetworkConfig, None]:
        """
        Get a network config document from its uuid.

        :param uuid: A target document uuid.
        :return: The network config document as an instance of
            :class:`~yawning_titan.config.network_config.NetworkConfig` if the uuid exists,
            otherwise :py:class:`None`.
        """
        doc = super().get_uuid(uuid)
        if doc:
            return self._doc_to_network_config(doc)

    def search(self, query: QueryInstance) -> List[NetworkConfig]:
        """
        Searches the network db with a given :class:`NetworkSchema` query.

        :param query: A :class:`tinydb.queries.QueryInstance`.
        :return: A :py:class:`list` of :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        network_configs = []
        for doc in super(NetworkDB, self).search(query):
            network_configs.append(self._doc_to_network_config(doc))
        return network_configs

    def update(
        self,
        network_config: NetworkConfig,
        uuid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> NetworkConfig:
        """Stub."""
        # Update the configs metadata
        network_config.doc_metadata.update(name, description, author)
        # Perform the update and retrieve the returned doc
        doc = super().update(
            network_config.to_dict(json_serializable=True),
            network_config.doc_metadata.uuid,
            name,
            description,
            author,
        )

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
        """Stub."""
        network_config.doc_metadata.update(name, description, author)
        super().upsert(
            network_config.to_dict(json_serializable=True),
            network_config.doc_metadata.uuid,
            name,
            description,
            author,
        )

        # Update the configs metadata created at
        network_config.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return network_config

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """Stub."""
        pass
