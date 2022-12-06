"""Provides an implementation of a TinyDB class as an ABC."""
from __future__ import annotations

import os.path
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Final, List, Mapping, Union

from tinydb import TinyDB
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan import DB_DIR
from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.exceptions import YawningTitanDBError

_LOGGER = getLogger(__name__)


class YawningTitanDB(ABC):
    """An :py:class:`~abc.ABC` that implements the :class:`~tinydb.database.TinyDB` query functions.

    :param name: The name of the db, similar to a SQL table name.
    """

    @abstractmethod
    def __init__(self, name: str):
        self._name: Final[str] = name
        self._path = DB_DIR / f"{self._name}.json"

        if not self._db_file_exist():
            _LOGGER.info(f"New TinyDB .json file created: {self._path}")
        self._db = TinyDB(self._path)

    def _db_file_exist(self) -> bool:
        """
        Check whether the :class:`~tinydb.database.TinyDB` .json file exists.

        :return: ``True`` if it does exist, otherwise ``False``.
        """
        return os.path.isfile(self._path)

    @property
    def name(self) -> str:
        """The DB name."""
        return self._name

    @property
    def db(self) -> TinyDB:
        """The instance of :class:`~tinydb.database.TinyDB`."""
        return self._db

    @abstractmethod
    def insert(self, item: Mapping) -> int:
        """An abstract :func:`tinydb.table.Table.insert` method."""
        if "_doc_metadata" not in item:
            item["_doc_metadata"] = DocMetadata()
        return self.db.insert(item)

    @abstractmethod
    def all(self) -> List[Document]:
        """An abstract :func:`tinydb.table.Table.all` method."""
        return self.db.all()

    @abstractmethod
    def get(self, doc_id: int) -> Union[Document, None]:
        """An abstract :func:`tinydb.table.Table.get` method."""
        return self.db.get(doc_id=doc_id)

    @abstractmethod
    def get_with_uuid(self, uuid: int) -> Union[Document, None]:
        """An abstract get_with_uuid method that searches th _doc_metadata.uuid."""
        results = self.db.search(DocMetadataSchema.UUID == uuid)
        if results:
            if len(results) == 1:
                return results[0]
            else:
                msg = f"Get with uuid aborted as multiple entries in the {self._name} db with uuid='{uuid}' exist."
                try:
                    raise YawningTitanDBError(msg)
                except YawningTitanDBError as e:
                    _LOGGER.critical(msg, exc_info=True)
                    raise e

    @abstractmethod
    def search(self, query: QueryInstance) -> List[Document]:
        """An abstract :func:`tinydb.table.Table.search` method."""
        return self.db.search(query)

    @abstractmethod
    def update(self, doc: Mapping, uuid: str) -> List[int]:
        """An abstract :func:`tinydb.table.Table.update` method."""
        return self.db.update(doc, cond=DocMetadataSchema.UUID == uuid)

    @abstractmethod
    def upsert(self, doc: Mapping, uuid: str) -> List[int]:
        """An abstract :func:`tinydb.table.Table.upsert` method."""
        return self.db.upsert(doc, cond=DocMetadataSchema.UUID == uuid)

    @abstractmethod
    def remove(self, cond: QueryInstance) -> List[int]:
        """An abstract :func:`tinydb.table.Table.remove` method."""
        return self.db.remove(cond=cond)

    def remove_with_uuid(self, uuid: str) -> List[int]:
        """
        Remove a document with a given _doc_metadata.uuid.

        :param uuid: A documents _doc_metadata.uuid.
        :return: The doc_id of the removed document.
        """
        docs = self.db.search(DocMetadataSchema.UUID == uuid)
        if docs and len(docs) > 1:
            msg = f"Remove with uuid aborted from {self._name} db as multiple documents with uuid='{uuid}' exist."
            try:
                raise YawningTitanDBError(msg)
            except YawningTitanDBError as e:
                _LOGGER.critical(msg, exc_info=True)
                raise e
        else:
            doc_ids = self.remove(cond=DocMetadataSchema.UUID == uuid)

            return doc_ids
