from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ConfigValidation:
    """
    :class:`ConfigValidation` is used to return a validation result.
    If validation fails, a reason why and any exception raised are returned.
    """

    passed: Optional[bool] = True
    """``True`` if the _value has passed validation, otherwise ``False``."""
    fail_reason: Optional[str] = None
    """The reason why validation failed."""
    fail_exception: Optional[Exception] = None
    """The :py::class:`Exception` raised when validation failed."""


@dataclass()
class ItemTypeProperties(ABC):
    """
    An Abstract Base Class that is inherited by config data type properties.
    """

    allow_null: Optional[bool] = None
    """`True` if the config _value can be left empty, otherwise `False`."""
    default: Optional[Any] = None
    """The items default value."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        An abstract method that returns the properties as a dict.

        :return: A dict.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @abstractmethod
    def validate(self, val) -> ConfigValidation:
        pass


@dataclass()
class ConfigItem:
    """The ConfigItem class holds an items value, doc, and properties."""
    value: object
    """The items value."""
    doc: Optional[str] = None
    """The items doc."""
    properties: Optional[ItemTypeProperties] = None
    """The items properties."""

    def __post_init__(self):
        if self.value is None and self.properties.default:
            self.value = self.properties.default
        if self.properties:
            value_validation = self.properties.validate(self.value)
            if not value_validation.passed:
                raise value_validation.fail_exception

    def to_dict(self, as_key_val_pair: bool = False):
        """
        Return the ConfigItem as a dict.

        :param as_key_val_pair: If true, the dict is returned as a value in
            a key/value pair, the key being the class name.
        :return: The ConfigItem as a dict.
        """
        d = {"value": self.value}
        if self.doc:
            d["doc"] = self.doc
        if self.properties:
            d["properties"] = self.properties.to_dict()
        if as_key_val_pair:
            return {self.__class__.__name__: d}
        return d
    
    def validate(self) -> ConfigValidation:
        """
        Validate the item against its properties. If no properties exist,
        simply return a default passed :class:`ConfigValidation`.

        :return: An instance of :class:`ConfigValidation`.
        """
        if self.properties:
            return self.properties.validate(self.value)
        return ConfigValidation()
