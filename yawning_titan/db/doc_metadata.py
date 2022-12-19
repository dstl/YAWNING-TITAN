from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Final, Optional, Union
from uuid import uuid4

from yawning_titan.db.query import YawningTitanQuery


@dataclass()
class DocMetadata:
    """
    A secure class to hold metadata related to a document in a Yawning-Titan TinyDB file.

    The ``uuid`` and ``created_at`` attributes are set upon instantiation if they are not passed as params.
    Once set, they cannot be changed.
    """

    def __init__(
        self,
        uuid: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        locked: Optional[bool] = False,
    ):
        """
        The :class:`~yawning_titan.db.yawning_titan_db.DocMetadata` constructor.

        :param uuid: The documents globally unique identifier.
        :param created_at: The datetime the document was created at as an ISO 8601 str.
        :param updated_at: The datetime the document was last updated at as an ISO 8601 str.
        :param name: The name given to the document by the author.
        :param description: The description given to the document by the author.
        :param author: The original author of the document.
        :param locked: Whether the doc is locked for editing or not.
        """
        self._uuid: Final[str] = uuid if uuid is not None else str(uuid4())
        self._created_at: Final[str] = (
            created_at if created_at is not None else datetime.now().isoformat()
        )
        self._updated_at: Optional[str] = updated_at
        self._name: Optional[str] = name
        self._description: Optional[str] = description
        self._author: Optional[str] = author
        self._locked: bool = locked

    # region Getters
    @property
    def uuid(self) -> str:
        """The documents globally unique identifier."""
        return self._uuid

    @property
    def created_at(self) -> str:
        """The datetime the document was created at as an ISO 8601 str."""
        return self._created_at

    @property
    def updated_at(self) -> Union[str, None]:
        """The datetime the document was last updated at as an ISO 8601 str."""
        return self._created_at

    @property
    def name(self) -> Union[str, None]:
        """The name given to the document by the author."""
        return self._name

    @property
    def description(self) -> Union[str, None]:
        """The description given to the document by the author."""
        return self._description

    @property
    def author(self) -> Union[str, None]:
        """The original author of the document."""
        return self._author

    @property
    def locked(self) -> bool:
        """Whether the doc is locked for editing or not."""
        return self._locked

    # endregion

    # region Setters
    @updated_at.setter
    def updated_at(self, updated_at: str):
        self._updated_at = updated_at

    @name.setter
    def name(self, name: str):
        self._name = name

    @description.setter
    def description(self, description: str):
        self._description = description

    @author.setter
    def author(self, author: str):
        self._author = author

    # endregion

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
    ):
        """
        Updated the name, description, and author.

        :param name: The name given to the document by the author.
        :param description: The description given to the document by the author.
        :param author: The original author of the document.
        """
        if name:
            self.name = name
        if description:
            self.description = description
        if author:
            self.author = author

    def to_dict(self, include_none: bool = False) -> Dict[str, str]:
        """
        Serialize the :class:`~yawning_titan.db.yawning_titan_db.DocMetadata` as a :py:class:`dict`.

        :param include_none: Determines whether to include empty fields in the dict.
        :return: The DocMetadata as a Python dict.
        """
        doc_dict = {
            "uuid": self._uuid,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "name": self._name,
            "description": self._description,
            "author": self._author,
            "locked": self._locked,
        }
        if not include_none:
            return {k: v for k, v in doc_dict.items() if v is not None}
        return doc_dict

    def __repr__(self):
        repr_str = f"{self.__class__.__name__}("
        k_v_strs = []
        for k, v in self.to_dict().items():
            if isinstance(v, str):
                k_v_str = f"{k}='{v}'"
            else:
                k_v_str = f"{k}={v}"
            k_v_strs.append(k_v_str)
        repr_str += ", ".join(k_v_strs)
        repr_str += ")"
        return repr_str

    def __hash__(self):
        return hash(
            (
                self._uuid,
                self._created_at,
                self._updated_at,
                self._name,
                self._description,
                self._author,
                self._locked,
            )
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False


class DocMetadataSchema:
    """
    A schema-like class that defines the document metadata fields.

    Fields are defined using the :class:`~yawning_titan.db.query.YawningTitanQuery` class
    so that schema paths can be used directly within :func:`tinydb.table.Table.search`
    function calls. All fields are mapped to a property in the
    :class:`~yawning_titan.db.yawning_titan_db.DocMetadata` class.
    """

    UUID: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.uuid
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.uuid`."""
    CREATED_AT: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.created_at
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.created_at`."""
    UPDATED_AT: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.updated_at
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.updated_at`."""
    NAME: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.name
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.name`."""
    DESCRIPTION: Final[
        YawningTitanQuery
    ] = YawningTitanQuery()._doc_metadata.description
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.description`."""
    AUTHOR: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.author
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.author`."""
    LOCKED: Final[YawningTitanQuery] = YawningTitanQuery()._doc_metadata.locked
    """Mapped to :attr:`yawning_titan.db.yawning_titan_db.DocMetadata.locked`."""
