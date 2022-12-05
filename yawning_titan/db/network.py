"""
The :mod:`yawning_titan.db.network` module.

Provides an API for the ``network.json`` :class:`~tinydb.database.TinyDB` file,
and a Schema-like class that defines the network DB fields.
"""
from __future__ import annotations

from typing import Final, List, Union

import numpy as np
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.config.network_config import NetworkConfig
from yawning_titan.db import YawningTitanDB

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

    - Search for all network configs that have at-least 3 high value nodes

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
        return NetworkConfig.create(doc)

    def insert(self, item: NetworkConfig) -> int:
        """
        Insert a :class:`~yawning_titan.config.network_config.NetworkConfig` into the DB as ``.json``.

        :param item: An instance of :class:`~yawning_titan.config.network_config.NetworkConfig`
        :return: The inserted document ID.
        """
        return super().insert(item.to_dict(json_serializable=True))

    def all(self) -> List[NetworkConfig]:
        """
        Get all :class:`~yawning_titan.config.network_config.NetworkConfig` from the network DB.

        :return: A :py:classs:`list` of :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        network_configs = []
        for doc in super(NetworkDB, self).all():
            network_configs.append(self._doc_to_network_config(doc))
        return network_configs

    def get(self, doc_id: int) -> Union[NetworkConfig, None]:
        """
        Get a network config document from its document ID.

        :param doc_id: A target document ID.
        :return: The network config document as an instance of
            :class:`~yawning_titan.config.network_config.NetworkConfig` if the document id exists,
            otherwise :py:class:`None`.
        """
        doc = super().get(doc_id)
        if doc:
            return self._doc_to_network_config(super().get(doc_id))

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
