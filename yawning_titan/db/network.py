from typing import Final, List, Union

import numpy as np
from tinydb import Query
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.db import YawningTitanQuery, YawningTitanTinyDB

__all__ = ["NetworkDB"]


class NetworkDB(YawningTitanTinyDB):
    """
    The :class:`yawning_titan.db.network.NetworkDB` class.

    The below code blocks demonstrate how to use the :class:`yawning_titan.db.network.NetworkDB` class.

    - Instantiate the Network DB:

        .. code:: python

            >>> from yawning_titan.db.network import NetworkDB
            >>> db = NetworkDB()

    - Search for all network configs that have "1" as an entry node:

        .. code:: python

            >>> db.search(db.ENTRY_NODES.all(["1"]))

    - Search for all network configs that have "1" as both an entry node and a high value node:

        .. code:: python

            >>> query = (db.ENTRY_NODES.all(["1"])) and (db.HIGH_VALUE_NODES.all(["1"]))
            >>> db.search(query)

    """
    MATRIX: Final[Query] = YawningTitanQuery().matrix
    POSITIONS: Final[Query] = YawningTitanQuery().positions
    ENTRY_NODES: Final[Query] = YawningTitanQuery().entry_nodes
    VULNERABILITIES: Final[Query] = YawningTitanQuery().vulnerabilities
    HIGH_VALUE_NODES: Final[Query] = YawningTitanQuery().high_value_nodes

    def __init__(self):
        super().__init__("network")

    @classmethod
    def _doc_to_network_config(cls, doc: Document):
        """
        Converts a :class:`tinydb.table.Document` from the :class:`yawning_titan.db.network.NetworkDB` to an instance
        of :class:`yawning_titan.config.network_config.network_config.NetworkConfig`.

        :param doc: A :class:`tinydb.table.Document`.
        :return: The doc as a :class:`yawning_titan.config.network_config.network_config.NetworkConfig`.
        """
        doc["matrix"] = np.array(doc["matrix"])
        return NetworkConfig.create(doc)

    def insert(self, item: NetworkConfig) -> int:
        return super().insert(item.to_dict(json_serializable=True))

    def all(self) -> List[NetworkConfig]:
        network_configs = []
        for doc in super(NetworkDB, self).all():
            network_configs.append(self._doc_to_network_config(doc))
        return network_configs

    def get(self, doc_id: int) -> Union[Document, None]:
        doc = super().get(doc_id)
        if doc:
            return self._doc_to_network_config(super().get(doc_id))

    def search(self, query: QueryInstance) -> List[NetworkConfig]:
        """
        Searches the network db.

        :param query: A :class:`tinydb.queries.QueryInstance`.
        :return: A :py:class:`list` of :class:`yawning_titan.config.network_config.network_config.NetworkConfig`.
        """
        network_configs = []
        for doc in super(NetworkDB, self).search(query):
            network_configs.append(self._doc_to_network_config(doc))
        return network_configs
