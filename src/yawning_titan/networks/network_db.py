"""Provides an API for the ``network.json`` TinyDB file, and a Schema class that defines the network DB fields."""
from __future__ import annotations

import os
from logging import getLogger
from pathlib import Path
from typing import Final, List, Optional, Union

from tinydb import TinyDB
from tinydb.queries import QueryInstance

from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.db.yawning_titan_db import YawningTitanDB, YawningTitanDBSchema
from yawning_titan.networks.network import Network

__all__ = ["NetworkDB", "NetworkSchema", "default_18_node_network"]

_LOGGER = getLogger(__name__)


class NetworkQuery(YawningTitanQuery):
    def __int__(self):
        super().__init__()

    @staticmethod
    def num_of_nodes(n: int) -> YawningTitanQuery:
        """Returns all Networks with n number of nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_nodes(18))

        :param n: The target number of nodes in a Network.
        :return: A list of Networks.
        """
        return YawningTitanQuery()["nodes"].len_eq(n)

    @staticmethod
    def num_of_nodes_between(min: int, max: int) -> YawningTitanQuery:
        """Returns all Networks with between `min` and `max` number of nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_nodes(18))

        :param min: The minimum number of nodes in a Network.
        :param max: The maximum number of nodes in a Network.
        :return: A list of Networks.
        """
        return YawningTitanQuery()["nodes"].len_bt(min, max)

    def _num_nodes_of_type(self, n, type):
        """Helper function for num_of_entry_nodes."""

        def test_len(val, i):
            try:
                nodes = [n for n in val.values() if val[type]]
                return len(nodes) == i
            except TypeError:
                return False

        return self.test(test_len, n)

    def _num_nodes_of_type_between(self, min, max, type):
        """Helper function for num_of_entry_nodes."""

        def test_len(val, min, max, type):
            try:
                nodes = [n for n in val.values() if n[type]]
                return min <= len(nodes) <= max
            except TypeError:
                return False

        return self.test(test_len, min, max, type)

    @staticmethod
    def num_of_entry_nodes(n: int) -> YawningTitanQuery:
        """
        Returns all Networks with n number of entry nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_entry_nodes(3))

        :param n: The target number of entry nodes.
        :return: A List of Nodes.
        """
        return NetworkQuery().nodes._num_nodes_of_type(n, "entry_node")

    @staticmethod
    def num_of_entry_nodes_between(min: int, max: int) -> YawningTitanQuery:
        """
        Returns all Networks with between `min` and `max` number of entry nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_entry_nodes_between(3,6))

        :param n: The target number of entry nodes.
        :return: A List of Nodes.
        """
        return NetworkQuery().nodes._num_nodes_of_type_between(min, max, "entry_node")

    @staticmethod
    def num_of_high_value_nodes(n: int) -> YawningTitanQuery:
        """
        Returns all Networks with n number of high_value nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_high_value_nodes(3))

        :param min: The minimum number of high_value nodes.
        :param max: The maximum number of high_value nodes.
        :return: A List of Nodes.
        """
        return NetworkQuery().nodes._num_nodes_of_type(n, "high_value_node")

    @staticmethod
    def num_of_high_value_nodes_between(min: int, max: int) -> YawningTitanQuery:
        """
        Returns all Networks with between `min` and `max` number of high value nodes.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB, NetworkQuery
        >>> db = NetworkDB()
        >>> networks = db.search(NetworkQuery.num_of_high_value_nodes_between(3,6))

        :param min: The minimum number of high_value nodes.
        :param max: The minimum number of high_value nodes.
        :return: A List of Nodes.
        """
        return NetworkQuery().nodes._num_nodes_of_type_between(
            min, max, "high_value_node"
        )


class NetworkSchema(YawningTitanDBSchema):
    """
    A schema-like class that defines the network DB fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:`~yawning_titan.networks.network.Network` class.

    :Example:

    >>> from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
    >>> db = NetworkDB()
    >>> network_configs = db.search(NetworkSchema.SET_RANDOM_ENTRY_NODES == True)
    """

    SET_RANDOM_ENTRY_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().set_random_entry_nodes
    RANDOM_ENTRY_NODE_PREFERENCE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().random_entry_node_preference
    NUM_OF_RANDOM_ENTRY_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().num_of_random_entry_nodes
    SET_RANDOM_HIGH_VALUE_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().set_random_high_value_nodes
    RANDOM_HIGH_VALUE_NODE_PREFERENCE: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().random_high_value_node_preference
    NUM_OF_RANDOM_HIGH_VALUE_NODES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().num_of_random_high_value_nodes
    SET_RANDOM_VULNERABILITIES: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().set_random_vulnerabilities
    NODE_VULNERABILITY_LOWER_BOUND: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().node_vulnerability_lower_bound
    NODE_VULNERABILITY_UPPER_BOUND: Final[
        YawningTitanQuery
    ] = YawningTitanQuery().node_vulnerability_upper_bound


class NetworkDB:
    """
    The :class:`~yawning_titan.db.networks.NetworkDB` class extends :class:`~yawning_titan.db.YawningTitanDB`.

    The below code blocks demonstrate how to use the :class:`~yawning_titan.db.networks.NetworkDB` class.

    - Instantiate the Network DB:

        .. code:: python

            >>> from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
            >>> db = NetworkDB()

    - Search for all network that have set_random_entry_nodes == True.

        .. code:: python

            >>> db.search(NetworkSchema.SET_RANDOM_ENTRY_NODES == True)

    """

    def __init__(self):
        self._db = YawningTitanDB("networks")

    def __enter__(self) -> NetworkDB:
        return NetworkDB()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.__exit__(exc_type, exc_val, exc_tb)

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
            :class:`~yawning_titan.db._doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db._doc_metadata.DocMetadata`.
            :class:`~yawning_titan.db._doc_metadata.DocMetadata`.
        :param name: The config name.
        :param description: The config description.
        :param author: The config author.
        :return: The inserted :class:`~yawning_titan.networks.network.Network`.
        """
        network.doc_metadata.update(name, description, author)
        self._db.insert(network.to_dict(json_serializable=True))

        return network

    def all(self) -> List[Network]:
        """
        Get all :class:`~yawning_titan.networks.network.Network` from the network DB.

        :return: A :class:`list` of :class:`~yawning_titan.networks.network.Network`.
        """
        return [Network.create(doc) for doc in self._db.all()]

    def show(self, verbose=False):
        """
        Show details of all entries in the db.

        :param verbose: If True, all doc metadata details are shown,
            otherwise just the name is shown.
        """
        self._db.show(verbose)

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
            return Network.create(doc)

    def search(self, query: YawningTitanQuery) -> List[Network]:
        """
        Searches the :class:`~yawning_titan.networks.network.Network` with a :class:`NetworkSchema` query.

        :param query: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: A :class:`list` of :class:`~yawning_titan.networks.network.Network`.
        """
        network_configs = []
        for doc in self._db.search(query):
            network_configs.append(Network.create(doc))
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

    def remove(self, network: Network) -> Union[str, None]:
        """
        Remove a :class:`~yawning_titan.networks.network.Network`. from the db.

        :param network: An instance of :class:`~yawning_titan.networks.network.Network`.
        :return: The uuid of the removed :class:`~yawning_titan.networks.network.Network`.
        """
        return self._db.remove(network.doc_metadata.uuid)

    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """
        Remove :class:`~yawning_titan.networks.network.Network`. from the db that match the query.

        :param cond: A :class:`~yawning_titan.db.query.YawningTitanQuery`.
        :return: The list of uuids of the removed :class:`~yawning_titan.networks.network.Network`.
        """
        return self._db.remove_by_cond(cond)

    def reset_default_networks_in_db(self, force=False):
        """
        Reset the default network in the db.

        Achieves this by loading the default
        `yawning_titan/networks/_package_data/network.json` db file into TinyDB,
        then iterating over all docs and forcing an update of each one in the main
        networks db from its uuid if they do not match.

        :param force: Forces a reset without checking for equality when
            True. Has a default value of False.
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
        for package_data_network in default_db.all():
            uuid = package_data_network["_doc_metadata"]["uuid"]
            name = package_data_network["_doc_metadata"]["name"]

            # Get the matching network from the networks db
            try:
                db_network = self.get(uuid)
            except KeyError:
                db_network = None

            # If the network doesn't match the default, or it doesn't exist,
            # perform an upsert.
            if not force and db_network:
                reset = False
            else:
                reset = True
            if reset:
                self._db.db.upsert(package_data_network, DocMetadataSchema.UUID == uuid)
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

    .. see also:: https://www.nsa.gov/portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    with NetworkDB() as db:
        return db.get("b3cd9dfd-b178-415d-93f0-c9e279b3c511")


def dcbo_base_network() -> Network:
    """
    Creates the same network used to generated DCBO data.

    .. node::
        This function replaces the network that was defined in
        `yawning_titan/integrations/dcbo/base_net.txt`.

    :return: An instance of :class:`~yawning_titan.networks.network.Network`.
    """
    with NetworkDB() as db:
        return db.get("47cb9f49-b53d-44f8-9a7b-3d74cf2ec1b0")
