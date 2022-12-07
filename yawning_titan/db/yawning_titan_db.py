"""
Provides an extended implementation of a TinyDB class as an ABC.

Makes use of uuid and locked values to ensure duplicates are not possible, and
locked files (system defaults) cannot be updated or removed.

.. todo:: Ensure the below versionadded is correct at the time of release.

.. versionadded:: 1.1.0
"""
from __future__ import annotations

import os.path
from abc import ABC, abstractmethod
from datetime import datetime
from logging import getLogger
from typing import Final, List, Mapping, Optional, Union

from tinydb import TinyDB
from tinydb.queries import QueryInstance
from tinydb.table import Document

from yawning_titan import DB_DIR
from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.exceptions import YawningTitanDBCriticalError, YawningTitanDBError

_LOGGER = getLogger(__name__)


class YawningTitanDB(ABC):
    """An :py:class:`~abc.ABC` that implements and extends the :class:`~tinydb.database.TinyDB` query functions."""

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

    @classmethod
    def _update_doc_metadata(
        cls,
        doc: Mapping,
        name: Optional[str],
        description: Optional[str],
        author: Optional[str],
    ) -> Mapping:
        """
        Add a name, description, author to a doc's metadata.

        :param doc: A doc.
        :param name: The doc name.
        :param description: The doc description.
        :param author: The docs author.
        :return: The updated doc.
        """
        if "_doc_metadata" in doc:
            if name:
                doc["_doc_metadata"]["name"] = name
            if description:
                doc["_doc_metadata"]["description"] = description
            if author:
                doc["_doc_metadata"]["author"] = author
        return doc

    @classmethod
    def _update_doc_updated_at_datetime(cls, doc: Mapping) -> Mapping:
        """
        Set the created_at field in doc_metadata to the current datetime in iso format.

        :param doc: A doc.
        :return: The updated doc.
        """
        doc["_doc_metadata"]["updated_at"] = datetime.now().isoformat()
        return doc

    @classmethod
    def is_locked(cls, doc: Mapping) -> bool:
        """
        Check whether a doc is locked for editing or not.

        :param doc: A doc.
        :return: ``True`` if the doc is locked, otherwise ``False``.
        """
        if "_doc_metadata" in doc:
            return doc["_doc_metadata"]["locked"]
        return False

    @property
    def name(self) -> str:
        """The DB name."""
        return self._name

    @property
    def db(self) -> TinyDB:
        """The instance of :class:`~tinydb.database.TinyDB`."""
        return self._db

    @abstractmethod
    def insert(
        self,
        doc: Mapping,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """
        An extension of :func:`tinydb.table.Table.insert`.

        If a doc doesn't have DocMetadata, the default DocMetadata is set.

        If a doc already exists with the same uuid, the insert is blocked and
        a :class:`~yawning_titan.exceptions.YawningTitanDBCriticalError` is
        raised alongside a log as ``CRITICAL`` level, as this would indicate
        db file is corrupted.

        :param doc: A doc.
        :param name: The doc name.
        :param description: The doc description.
        :param author: The docs author.
        :return: The inserted doc.
        :raise: :class:`~yawning_titan.exceptions.YawningTitanDBCriticalError`
            when a doc already exists with the same uuid.
        """
        if "_doc_metadata" not in doc:
            doc["_doc_metadata"] = DocMetadata()
        else:
            # Check for existing uuid entry
            uuid = doc["_doc_metadata"]["uuid"]
            if self.get_uuid(uuid):
                msg = (
                    f"Failed to insert doc into the {self._name} db with uuid='{uuid}' as one already exists. "
                    f"The '{self._path}' db file is corrupted."
                )
                try:
                    raise YawningTitanDBCriticalError(msg)
                except YawningTitanDBCriticalError as e:
                    _LOGGER.critical(msg, exc_info=True)
                    raise e
        self._update_doc_metadata(doc, name, description, author)
        if doc["_doc_metadata"]["locked"]:
            uuid = doc["_doc_metadata"]["uuid"]
            _LOGGER.info(
                f"Doc inserted into the {self._name} db with uuid='{uuid}' was inserted as locked."
            )
        self.db.insert(doc)
        return self.get_uuid(doc["_doc_metadata"]["uuid"])

    @abstractmethod
    def all(self) -> List[Document]:
        """A wrapper for :func:`tinydb.table.Table.all`."""
        return self.db.all()


    def get_uuid(self, uuid: str) -> Union[Document, None]:
        """
        Get a doc from its uuid.

        :param uuid: A uuid.
        :return: The matching doc if it exists, otherwise ``None``.
        :raise: :class:`~yawning_titan.exceptions.YawningTitanDBCriticalError`
            when the search returns multiple docs with the same uuid.
        """
        results = self.db.search(DocMetadataSchema.UUID == uuid)
        if results:
            if len(results) == 1:
                return results[0]
            else:
                msg = (
                    f"Get from the {self._name} db with uuid='{uuid}' aborted as multiple docs with the uuid "
                    f"exist. The '{self._path}' db file is corrupted."
                )
                try:
                    raise YawningTitanDBCriticalError(msg)
                except YawningTitanDBCriticalError as e:
                    _LOGGER.critical(msg, exc_info=True)
                    raise e

    @abstractmethod
    def search(self, cond: QueryInstance) -> List[Document]:
        """A wrapper for :func:`tinydb.table.Table.search`."""
        return self.db.search(cond)

    @abstractmethod
    def update(
        self,
        doc: Mapping,
        uuid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """
        An extension of :func:`tinydb.table.Table.update`.

        Performs a check that prevents locked files from being updated and raises
        :class:`~yawning_titan.exceptions.YawningTitanDBError` alongside a log at
        ``INFO`` level.

        :param doc: A doc.
        :param uuid: The docs uuid.
        :param name: The doc name.
        :param description: The doc description.
        :param author: The docs author.
        :return: The updated doc.
        :raise: :class:`~yawning_titan.exceptions.YawningTitanDBError` if
            the doc is locked.
        """
        existing_doc = self.get_uuid(uuid)
        if existing_doc and self.is_locked(existing_doc):
            msg = f"Cannot update doc with uuid='{uuid}' in the {self._name} db as it is locked for editing."
            try:
                raise YawningTitanDBError(msg)
            except YawningTitanDBError as e:
                _LOGGER.info(msg, exc_info=True)
                raise e
        self._update_doc_metadata(doc, name, description, author)
        self._update_doc_updated_at_datetime(doc)
        self.db.update(doc, cond=DocMetadataSchema.UUID == uuid)
        return self.get_uuid(uuid)

    @abstractmethod
    def upsert(
        self,
        doc: Mapping,
        uuid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Document:
        """
        A manual upsert method in place of :func:`tinydb.table.Table.upsert`.

        If the docs uuid already exists, the args are passed to
        :func:`yawning_titan.db.yawning_titan_db.YawningTitanDB.update` to
        perform an update, otherwise they're passed to
        :func:`~yawning_titan.db.yawning_titan_db.YawningTitanDB.insert` to
        perform an insert. This is done to make use of the existing uuid and
        locked file handling in the two methods.

        :param doc: A doc.
        :param uuid: The docs uuid.
        :param name: The doc name.
        :param description: The doc description.
        :param author: The docs author.
        :return: The updated doc.
        """
        existing_doc = self.get_uuid(uuid)
        if existing_doc:
            # Attempt to update
            return self.update(doc, uuid, name, description, author)
        else:
            # Insert
            return self.insert(doc, name, description, author)

    @abstractmethod
    def remove_by_cond(self, cond: QueryInstance) -> List[str]:
        """An abstract :func:`tinydb.table.Table.remove` method."""
        results = self.search(cond)
        removed_uuids = []
        for doc in results:
            try:
                uuid = doc["_doc_metadata"]["uuid"]
                removed_uuid = self.remove(uuid)
                if removed_uuid:
                    removed_uuids.append(removed_uuid)
            except YawningTitanDBError:
                pass
        return removed_uuids

    def remove(self, uuid: str) -> Union[str, None]:
        """
        Remove a document with a given _doc_metadata.uuid.

        :param uuid: A documents _doc_metadata.uuid.
        :return: The uuid of the removed document.
        :raises: :class:`~yawning_titan.exceptions.YawningTitanDBCriticalError`
            when there is more than one doc with the same uuid to remove.
            :class:`~yawning_titan.exceptions.YawningTitanDBError` when
            an attempt to remove a locked doc is made.
        """
        doc = self.db.search(DocMetadataSchema.UUID == uuid)
        print("")
        if doc:
            if len(doc) > 1:
                msg = (
                    f"Removal of a doc from the {self._name} db with uuid='{uuid}' aborted as multiple docs with "
                    f"the uuid exist. The '{self._path}' db file is corrupted."
                )
                try:
                    raise YawningTitanDBCriticalError(msg)
                except YawningTitanDBError as e:
                    _LOGGER.critical(msg, exc_info=True)
                    raise e
            else:
                doc = doc[0]
                if "_doc_metadata" in doc:
                    if doc["_doc_metadata"]["locked"]:
                        msg = (
                            f"Aborted removal of doc with uuid='{uuid}' from the {self._name} db as it is locked "
                            f"for removal."
                        )
                        try:
                            raise YawningTitanDBError(msg)
                        except YawningTitanDBError as e:
                            _LOGGER.info(msg, exc_info=True)
                            raise e
                self.db.remove(cond=DocMetadataSchema.UUID == uuid)
                return uuid
        return None
