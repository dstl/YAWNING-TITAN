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
from yawning_titan.networks.network import Network

__all__ = ["NetworkDB", "NetworkSchema"]

_LOGGER = getLogger(__name__)


class NetworkSchema:
    """
    A schema-like class that defines the network DB fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:`~yawning_titan.networks.network.Network` class.

    :Example:

    >>> from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
    >>> db = NetworkDB()
    >>> network_configs = db.search(NetworkSchema.MATRIX.len_le(18))
    """

    MATRIX: Final[YawningTitanQuery] = YawningTitanQuery().matrix
    """Mapped to :attr:`yawning_titan.networks.network.Network.matrix`."""
    POSITIONS: Final[YawningTitanQuery] = YawningTitanQuery().positions
    """Mapped to :attr:`yawning_titan.networks.network.Network.positions`."""
    ENTRY_NODES: Final[YawningTitanQuery] = YawningTitanQuery().entry_nodes
    """Mapped to :attr:`yawning_titan.networks.network.Network.entry_nodes`."""
    VULNERABILITIES: Final[YawningTitanQuery] = YawningTitanQuery().vulnerabilities
    """Mapped to :attr:`yawning_titan.networks.network.Network.vulnerabilities`."""
    HIGH_VALUE_NODES: Final[YawningTitanQuery] = YawningTitanQuery().high_value_nodes
    """Mapped to :attr:`yawning_titan.networks.network.Network.high_value_nodes`."""


class NetworkDB:
    """
    The :class:`~yawning_titan.db.networks.NetworkDB` class extends :class:`~yawning_titan.db.YawningTitanDB`.

    The below code blocks demonstrate how to use the :class:`~yawning_titan.db.networks.NetworkDB` class.

    - Instantiate the Network DB:

        .. code:: python

            >>> from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
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
        self._db = YawningTitanDB("networks")
        self.reset_default_networks_in_db()

    def __enter__(self) -> NetworkDB:
        return NetworkDB()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def _doc_to_network_config(cls, doc: Document):
        """Convert the document.

        Converts a :class:`tinydb.table.Document` from the :class:`~yawning_titan.db.networks.NetworkDB` to an instance
        of :class:`~yawning_titan.networks.network.Network`.

        :param doc: A :class:`tinydb.table.Document`.
        :return: The doc as a :class:`~yawning_titan.networks.network.Network`.
        """
        doc["matrix"] = np.array(doc["matrix"])
        doc["_doc_metadata"] = DocMetadata(**doc["_doc_metadata"])
        return Network(**doc)

    def insert(
        self,
        network: Network,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Network:
        """
        Insert a :class:`~yawning_titan.networks.network.Network` into the DB as ``.json``.

        :param network: An instance of :class:`~yawning_titan.networks.network.Network`
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db.doc_metadata.DocMetadata`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The inserted :class:`~yawning_titan.networks.network.Network`.
        """
        print(network.doc_metadata)
        network.doc_metadata.update(name, description, author)
        self._db.insert(network.to_dict(json_serializable=True, include_none=False))

        return network

    def all(self) -> List[Network]:
        """
        Get all :class:`~yawning_titan.networks.network.Network` from the network DB.

        :return: A :py:classs:`list` of :class:`~yawning_titan.networks.network.Network`.
        """
        return [self._doc_to_network_config(doc) for doc in self._db.all()]

    def get(self, uuid: str) -> Union[Network, None]:
        """
        Get a network config document from its uuid.

        :param uuid: A target document uuid.
        :return: The network config document as an instance of
            :class:`~yawning_titan.networks.network.Network` if the uuid exists,
            otherwise :py:class:`None`.
        """
        # self._db.db.clear_cache()
        doc = self._db.get(uuid)
        if doc:
            return self._doc_to_network_config(doc)

    def search(self, query: YawningTitanQuery) -> List[Network]:
        """
        Searches the :class:`~yawning_titan.networks.network.Network` with a :class:`NetworkSchema` query.

        :param query: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: A :py:class:`list` of :class:`~yawning_titan.networks.network.Network`.
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
        network: Network,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Network:
        """
        Update a :class:`~yawning_titan.networks.network.Network`. in the db.

        :param network: An instance of :class:`~yawning_titan.networks.network.Network`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The updated :class:`~yawning_titan.networks.network.Network`.
        """
        # Update the configs metadata
        network.doc_metadata.update(name, description, author)
        # Perform the update and retrieve the returned doc
        doc = self._db.update(
            network.to_dict(json_serializable=True),
            network.doc_metadata.uuid,
            name,
            description,
            author,
        )
        if doc:
            # Update the configs metadata created at
            network.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return network

    def upsert(
        self,
        network: Network,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Network:
        """
        Upsert a :class:`~yawning_titan.networks.network.Network`. in the db.

        :param network: An instance of :class:`~yawning_titan.networks.network.Network`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The upserted :class:`~yawning_titan.networks.network.Network`.
        """
        network.doc_metadata.update(name, description, author)
        doc = self._db.upsert(
            network.to_dict(json_serializable=True),
            network.doc_metadata.uuid,
            name,
            description,
            author,
        )

        # Update the configs metadata created at
        if doc and "updated_at" in doc["_doc_metadata"]:
            network.doc_metadata.updated_at = doc["_doc_metadata"]["updated_at"]

        return network

    def remove(self, network: Network) -> List[str]:
        """
        Remove a :class:`~yawning_titan.networks.network.Network`. from the db.

        :param network: An instance of :class:`~yawning_titan.networks.network.Network`.
        :return: The uuid of the removed :class:`~yawning_titan.networks.network.Network`.
        """
        self._db.remove(network.doc_metadata.uuid)

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """
        Remove :class:`~yawning_titan.networks.network.Network`. from the db that match the query.

        :param cond: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: The list of uuids of the removed :class:`~yawning_titan.networks.network.Network`.
        """
        return self._db.remove_by_cond(cond)

    def reset_default_networks_in_db(self):
        """
        Reset the default network in the db.

        Achieves this by loading the default
        `yawning_titan/networks/_package_data/network.json` db file into TinyDB,
        then iterating over all docs and forcing an update of each one in the main
        networks db from its uuid if they do not match.
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

            # Get the matching network from the networks db
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
            - call :func:`~yawning_titan.networks.network_db.NetworkDB.reset_default_networks_in_db`

        .. warning::

                This function completely rebuilds the database. Any custom networks
                saved in the db will be lost. The default networks can be reset
                using the :func:`~yawning_titan.networks.network_db.NetworkDB.reset_default_networks_in_db`
                function.
        """
        _LOGGER.info(f"Rebuilding the {self._db.name} db.")
        self._db.db.clear_cache()
        self._db.db.truncate()
        self.reset_default_networks_in_db()


def default_18_node_network() -> Network:
    """
    The standard 18-node network found in the Ridley, A. (2017) research paper.

    .. seealso:: https://www.nsa.gov/portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    with NetworkDB() as db:
        return db.get("b3cd9dfd-b178-415d-93f0-c9e279b3c511")
