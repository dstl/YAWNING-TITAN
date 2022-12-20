from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from collections.abc import Iterable

from yawning_titan.exceptions import ConfigGroupValidationError


@dataclass()
class ConfigItemValidation:
    """
    :class:`ConfigItemValidation` is used to return a validation result.

    If validation fails, a reason why and any exception raised are returned.
    """

    passed: Optional[bool] = True
    """``True`` if the _value has passed validation, otherwise ``False``."""
    fail_reason: Optional[str] = None
    """The reason why validation failed."""
    fail_exception: Optional[Exception] = None
    """The :py::class:`Exception` raised when validation failed."""


class ConfigGroupCore:
    """
    Used to provide helper methods to represent a ConfigGroup object.
    """
    def get_config_elements(self)->Dict[str,Union[ConfigItem,ConfigGroup]]:
        return {k:v for k,v in self.__dict__.items() if isinstance(v,ConfigItem) or isinstance(v,ConfigGroup)}

    def get_non_config_elements(self)->Dict[str,Any]:
        return {k:v for k,v in self.__dict__.items() if k not in self.get_config_elements()}

    def stringify(self):
        string = f"{self.__class__.__name__}("
        strings = [f"{name}={val.stringify()}" for name,val in self.get_config_elements().items()]
        strings.extend([f"{name}={val}" for name,val in self.get_non_config_elements().items()])
        return string + ", ".join(strings)


    def __repr__(self) -> str:
        return self.stringify()

    def __str__(self) -> str:
        return self.stringify()

    def __hash__(self) -> int:
        element_hash = [v.stringify() for v in self.get_config_elements().values()]
        element_hash.extend([tuple(v) if isinstance(v,Iterable) else v for v in self.get_non_config_elements().values()])
        return hash(tuple(element_hash))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

class ConfigGroupValidation(ConfigGroupCore):
    """
    Used to return a validation result for a group of dependant config items, and the list of item validations.

    If validation fails, a reason why and any exception raised are returned.
    """

    def __init__(
        self,
        passed: bool = True,
        fail_reason: Optional[str] = None,
        fail_exception: Optional[ConfigGroupValidationError] = None,
    ):
        self.passed: bool = passed
        self.fail_reason: str = fail_reason
        self.fail_exception: ConfigGroupValidationError = fail_exception
        self._element_validation = {}

    def add_element_validation(self, element_name: str, validation: ConfigItemValidation):
        """
        Add a :class:`ConfigItemValidation` or :class:`ConfigGroupValidation` to the item validation dict.

        :param element_name: The name of the element.
        :param validation: the instance of ConfigItemValidation.
        """
        self._element_validation[element_name] = validation


    @property
    def element_validation(self) -> Dict[str, ConfigItemValidation]:
        """
        The dict of element to :class:`ConfigItemValidation` and :class:`ConfigGroupValidation` validations.

        :return: A dict.
        """
        return self._element_validation

    @property
    def group_passed(self) -> bool:
        """
        Returns True if all items passed validation, otherwise returns False.

        :return: A bool.
        """
        return all(v.passed for v in self.element_validation.values())

    # def __repr__(self) -> str:
    #     return (
    #         f"ConfigGroupValidation("
    #         f"passed={self.passed}, "
    #         f"fail_reason='{self.fail_reason}', "
    #         f"fail_exception={self.fail_exception}, "
    #         f"item_validation={self._item_validation}, "
    #         f"group_passed={self.group_passed}"
    #         f")"
    #     )

    # def __hash__(self) -> int:
    #     return hash(
    #         (
    #             self.passed,
    #             self.fail_reason,
    #             self.fail_exception,
    #             tuple(self._item_validation),
    #         )
    #     )

    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, ConfigGroupValidation):
    #         return hash(self) == hash(other)
    #    return False


@dataclass()
class ItemTypeProperties(ABC):
    """An Abstract Base Class that is inherited by config data type properties."""

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
    def validate(self, val) -> ConfigItemValidation:
        """An abstract group validation."""
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
    validation: ConfigItemValidation = None
    """The instance of ConfigItemValidation that provides access to the item validation details."""

    def __post_init__(self):
        if self.value is None and self.properties.default:
            self.value = self.properties.default
        self.validation = self.properties.validate(self.value)

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

    def validate(self) -> ConfigItemValidation:
        """
        Validate the item against its properties.

        If no properties exist,
        simply return a default passed :class:`ConfigItemValidation`.

        :return: An instance of :class:`ConfigItemValidation`.
        """
        if self.properties:
            return self.properties.validate(self.value)
        return ConfigItemValidation()

    def stringify(self):
        return self.value


class ConfigGroup(ConfigGroupCore, ABC):
    """The ConfigGroup class holds a ConfigItem's, doc, properties, and a ConfigItemValidation."""

    def __init__(self, doc: Optional[str] = None):
        self.doc: Optional[str] = doc
        """The groups doc."""
        self.validation = self.validate()

    @abstractmethod
    def _items_map(self) -> Dict[str, Union[ConfigItem, ConfigGroup]]: # TODO: remove this, its not necessary as can be replaced with getter methods on ConfigGroupCore
        pass

    @abstractmethod
    def to_dict(self): # TODO: replace with generic method
        """
        Return the ConfigGroup as a dict.

        :return: The ConfigGroup as a dict.
        """
        d = {"doc": self.doc}
        return d

    @abstractmethod
    def validate(self) -> ConfigGroupValidation:
        """
        Validate the grouped items against their properties.

        :return: An instance of :class:`ConfigGroupValidation`.
        """
        pass
        # TODO: modify this so that 

    def validate_elements(self):
        """
        

        :param elements: _description_
        :type elements: Dict[str,Union[ConfigItem,ConfigGroup]]
        """
        for k, element in self.get_config_elements().items():
            self.validation.add_element_validation(k, element.validation)