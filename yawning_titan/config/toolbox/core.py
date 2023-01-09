from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import yaml

from yawning_titan.config.game_config import _LOGGER
from yawning_titan.exceptions import (
    ConfigGroupValidationError,
    ConfigItemValidationError,
)

yaml.Dumper.ignore_aliases = lambda *args: True


class ConfigBase(ABC):
    """Used to provide helper methods to represent a ConfigGroup object."""

    def get_config_elements(
        self, types: Optional[Union[ConfigItem, ConfigGroup]] = None
    ) -> Dict[str, Union[ConfigItem, ConfigGroup]]:
        """
        Get the attributes of the class that are either :class: `ConfigGroup` or :class:`ConfigItem`.

        :param _type: An optional type for a specific type of config element.

        :return: A dictionary of names to config elements.
        """
        if types is not None:
            if isinstance(types, list):
                types = tuple(types)
            return {
                k: v
                for k, v in self.__dict__.items()
                if isinstance(v, types) and not k.startswith("_")
            }
        return {
            k: v
            for k, v in self.__dict__.items()
            if isinstance(v, (ConfigItem, ConfigGroup)) and not k.startswith("_")
        }

    def get_non_config_elements(self) -> Dict[str, Any]:
        """
        Get all attributes of the class that are not :class: `ConfigGroup` or :class: `ConfigItem`.

        :return: A dictionary of names to attributes.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if k not in self.get_config_elements() and not k.startswith("_")
        }

    def stringify(self):
        """Represent the class as a string.

        :return: A string.
        """
        string = f"{self.__class__.__name__}("
        strings = [
            f"{name}={val.stringify()}"
            for name, val in self.get_config_elements().items()
        ]
        strings.extend(
            [f"{name}={val}" for name, val in self.get_non_config_elements().items()]
        )
        return string + ", ".join(strings) + ")"

    def __repr__(self) -> str:
        """Return the result of :method: `ConfigBase.stringify`."""
        return self.stringify()

    def __str__(self) -> str:
        """Return the result of :method: `ConfigBase.stringify`."""
        return self.stringify()

    def __hash__(self) -> int:
        """Generate a unique hash for the class."""
        element_hash = [v.stringify() for v in self.get_config_elements().values()]
        element_hash.extend(
            [
                tuple(v) if type(v) in [list, dict, set] else v
                for v in self.get_non_config_elements().values()
            ]
        )
        tuple_hash = tuple(element_hash)
        return hash(tuple_hash)

    def __eq__(self, other) -> bool:
        """Check the equality of any 2 instances of class.

        :param other: Another potential instance of the class to be compared against.

        :return: A boolean True if the elements holds the same data otherwise False.
        """
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False


@dataclass()
class ItemTypeProperties(ABC):
    """An Abstract Base Class that is inherited by config data type properties."""

    _allowed_types: List[type] = None
    """The allowed data types for the item."""
    allow_null: Optional[bool] = None
    """`True` if the config _value can be left empty, otherwise `False`."""
    default: Optional[Any] = None
    """The items default value."""

    def __post_init__(self):
        if self.default:
            validated_default = self.validate(self.default)
            if not validated_default.passed:
                raise validated_default.fail_exceptions[0]

    def to_dict(self) -> Dict[str, Any]:
        """
        An abstract method that returns the properties as a dict.

        :return: A dict.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if v is not None and not k.startswith("_")
        }

    def validate(self, val) -> ConfigItemValidation:
        """Perform the base validation checks common to all `ConfigItem` elements.

        These checks include:
        - Check that the value is not null if :attribute: `allow_null` is False
        - Check that the type of the value is in :attribute: `allowed_types`
        """
        validation = ConfigItemValidation()
        try:
            if not self.allow_null and val is None:
                msg = f"Value {val} when allow_null is not permitted."
                raise ConfigItemValidationError(msg)
        except ConfigItemValidationError as e:
            validation.add_validation(msg, e)
        try:
            if val is not None and type(val) not in self._allowed_types:
                msg = (
                    f"Value {val} is of type {type(val)}, should be "
                    + " or ".join(map(str, self._allowed_types))
                    + "."
                )
                raise ConfigItemValidationError(msg)
        except ConfigItemValidationError as e:
            validation.add_validation(msg, e)
        return validation


class ConfigValidationBase(ConfigBase):
    """The base validation methods for a config element."""

    def __init__(
        self,
        fail_reasons: Optional[Union[List[str], str]] = None,
        fail_exceptions: Optional[
            Union[
                List[Union[ConfigGroupValidationError, ConfigItemValidationError]],
                Union[ConfigGroupValidationError, ConfigItemValidationError],
            ]
        ] = None,
    ):
        if isinstance(fail_reasons, list):
            self.fail_reasons: List[str] = fail_reasons
        elif isinstance(fail_reasons, str):
            self.fail_reasons: List[str] = [fail_reasons]
        else:
            self.fail_reasons: List[str] = []

        if isinstance(fail_exceptions, list):
            self.fail_exceptions: List[
                Union[ConfigGroupValidationError, ConfigItemValidationError]
            ] = fail_exceptions
        elif isinstance(fail_reasons, str):
            self.fail_exceptions: List[
                Union[ConfigGroupValidationError, ConfigItemValidationError]
            ] = [fail_exceptions]
        else:
            self.fail_exceptions: List[
                Union[ConfigGroupValidationError, ConfigItemValidationError]
            ] = []

    def add_validation(self, fail_reason: str, exception: ConfigGroupValidationError):
        """
        Add a validation fail_reason, exception pair to their respective lists.

        Additionally check that no such error already exists.

        :param fail_reason: A string message to describe a particular error.
        :param exception: A wrapped `Exception` object that can be used to raise an error for the `fail_reason`.
        """
        if fail_reason not in self.fail_reasons:
            self.fail_reasons.append(fail_reason)
        if exception not in self.fail_exceptions:
            self.fail_exceptions.append(exception)

    def stringify(self):
        """Represent the class as a string.

        :return: A string.
        """
        string = f"{self.__class__.__name__}("

        strings = [f"passed={self.passed}"]
        strings.extend(
            [f"{name}={val}" for name, val in self.get_non_config_elements().items()]
        )
        return string + ", ".join(strings) + ")"

    @property
    @abstractmethod
    def passed(self) -> bool:
        """
        Returns True if there are no :attribute: `fail_reasons` or :attribute: `fail_exceptions`.

        :return: A bool.
        """
        pass


class ConfigItemValidation(ConfigValidationBase):
    """Create :class:`ConfigItemValidation` from :class:`ConfigValidationBase`."""

    @property
    def passed(self) -> bool:
        """
        Returns True if there are no :attribute: `fail_reasons` or :attribute: `fail_exceptions`.

        :return: A bool.
        """
        return not (self.fail_exceptions or self.fail_reasons)


class ConfigGroupValidation(ConfigValidationBase):
    """
    Used to return a validation result for a group of dependant config items, and the list of item validations.

    If validation fails, a reason why and any exception raised are returned.
    """

    def __init__(
        self,
        fail_reasons: Optional[Union[List[str], str]] = None,
        fail_exceptions: Optional[
            Union[
                List[Union[ConfigGroupValidationError, ConfigItemValidationError]],
                Union[ConfigGroupValidationError, ConfigItemValidationError],
            ]
        ] = None,
    ):
        self._element_validation = {}
        super().__init__(fail_reasons, fail_exceptions)

    def add_element_validation(
        self,
        element_name: str,
        validation: Union[ConfigItemValidation, ConfigGroupValidation],
    ):
        """
        Add a :class:`ConfigItemValidation` or :class:`ConfigGroupValidation` to the item validation dict.

        :param element_name: The name of the element.
        :param validation: the instance of ConfigItemValidation.
        """
        self._element_validation[element_name] = validation

    def to_dict(self, element_name: str = "root", root: bool = True) -> dict:
        """
        Express the error tree as a dictionary.

        :param element_name: A string name for the element to be represented.

        :return: A dict of element names to validation errors or validation dictionaries.
        """
        if self.passed:
            d = {}
        else:
            d = {"group": self.fail_reasons}
        for e, validation in self.element_validation.items():
            if isinstance(validation, ConfigGroupValidation) and (
                not validation.group_passed or not validation.passed
            ):
                d[e] = validation.to_dict(e, False)
            elif not validation.passed:
                d[e] = validation.fail_reasons

        if root:
            if not d:
                return {element_name: "Passed"}
            return {element_name: d}
        return d

    def log(self, element_name: str = "root") -> None:
        """
        Return the validation results as a formatted string.

        :param element_name: A string name for the element to be represented.
        """
        string = "\nValidation results\n" "------------------\n"
        d = self.to_dict(element_name)
        if d:
            string += yaml.dump(d, sort_keys=False, default_flow_style=False)
        else:
            string += d.get(element_name, "Passed")
        print(string)

    @property
    def passed(self) -> bool:
        """
        Returns True if there are no :attribute: `fail_reasons` or :attribute: `fail_exceptions` and the group passed.

        The group validation has passed and all element validation has passed.

        :return: A bool.
        """
        return self.elements_passed and self.group_passed

    @property
    def group_passed(self) -> bool:
        """
        Returns True if there are no :attribute: `fail_reasons` or :attribute: `fail_exceptions`.

        :return: A bool.
        """
        return not (self.fail_exceptions or self.fail_reasons)

    @property
    def element_validation(
        self,
    ) -> Dict[str, Union[ConfigItemValidation, ConfigGroupValidationError]]:
        """
        The dict of element to :class:`ConfigItemValidation` and :class:`ConfigGroupValidation` validations.

        :return: A dict.
        """
        return self._element_validation

    @property
    def elements_passed(self) -> bool:
        """
        Returns True if all items passed validation, otherwise returns False.

        :return: A bool.
        """
        return all(v.passed for v in self.element_validation.values())


@dataclass
class ConfigItem:
    """The ConfigItem class holds an items value, doc, and properties."""

    value: object
    """The items value."""
    doc: Optional[str] = None
    """The items doc."""
    alias: str = field(default=None, repr=False)
    """The alias of the config item, i.e. its representation from the original config."""
    depends_on: List[str] = field(default_factory=list, repr=False)
    """A list of :class: `ConfigItem`'s upon which this item depends. If these items are set so must this item be."""
    properties: Optional[ItemTypeProperties] = None
    """The items properties."""
    validation: ConfigItemValidation = None
    """The instance of ConfigItemValidation that provides access to the item validation details."""

    def __post_init__(self):
        if self.value is None and self.properties.default:
            self.value = self.properties.default
        self.validate()

    def __setattr__(self, __name: str, __value: Any) -> None:
        """
        Set an attribute of the :class: `ConfigItem` if the value is to be set, call the validation method.

        :param __name: the name of the attribute to be set
        :param __value: the value to set the attribute to
        """
        self.__dict__[__name] = __value
        if __name == "value":
            self.validate()

    def to_dict(
        self,
        as_key_val_pair: Optional[bool] = False,
        values_only: Optional[bool] = False,
    ):
        """
        Return the ConfigItem as a dict.

        :param as_key_val_pair: If true, the dict is returned as a value in
            a key/value pair, the key being the class name.
        :return: The ConfigItem as a dict.
        """
        if values_only:
            return self.value
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
        self.validation = ConfigItemValidation()
        if self.properties:
            self.validation = self.properties.validate(self.value)
        return self.validation

    def set_value(self, value: Any) -> None:
        """
        Set the value of the :class:`ConfigItem` bypassing the validation.

        :param value: The value to be set.
        """
        self.__dict__["value"] = value

    def stringify(self):
        """This is here to allow stringify methods to be call on both :class: `ConfigItem` and :class: `ConfigGroup` classes."""
        return self.value


class ConfigGroup(ConfigBase, ABC):
    """The ConfigGroup class holds a ConfigItem's, doc, properties, and a ConfigItemValidation."""

    def __init__(self, doc: Optional[str] = None):
        """The ConfigGroup constructor.

        :param doc: The groups doc.
        """
        self.doc: Optional[str] = doc
        self.validation = self.validate()

    def validate(self, raise_overall_exception: bool = False) -> ConfigGroupValidation:
        """
        Validate the grouped items against their properties.

        :return: An instance of :class:`ConfigGroupValidation`.
        """
        self.validation = ConfigGroupValidation()
        self.validate_elements()

        if raise_overall_exception and not self.validation.passed:
            raise ConfigGroupValidationError(self.validation.log())
        return self.validation

    def to_dict(self, values_only: Optional[bool] = False, legacy: bool = False):
        """
        Return the ConfigGroup as a dict.

        :param values_only: Create a dictionary containing only the value of :class: `ConfigItem`'s
        :param legacy: Convert the group into a unitary depth dictionary of legacy config value (aliases) to :class: `ConfigItem`'s
            by calling :method: `ConfigGroup.to_legacy`.

        :return: The ConfigGroup as a dict.
        """
        if legacy:
            return self.to_legacy_dict()

        attr_dict = {"doc": self.doc} if self.doc is not None else {}
        # attr_dict = self.get_non_config_elements()
        element_dict = {
            k: e.to_dict(values_only=values_only)
            for k, e in self.get_config_elements().items()
            if not k.startswith("_")
        }

        if values_only:
            return element_dict
        return {**attr_dict, **element_dict}

    def to_legacy_dict(
        self, flattened_dict: Dict[str, Any] = None
    ) -> Dict[str, ConfigItem]:
        """Convert the group into a unitary depth dictionary of legacy config value (aliases) to :class: `ConfigItem`'s.

        :return: a dictionary
        """
        if flattened_dict is None:
            flattened_dict = {}
        for v in self.get_config_elements().values():
            if isinstance(v, ConfigItem):
                flattened_dict[v.alias] = v
            else:
                flattened_dict.update(v.to_legacy_dict(flattened_dict))

        return flattened_dict

    def validate_elements(self):
        """Call the .validate() method on each of the elements in the group."""
        for k, element in self.get_config_elements().items():
            self.validation.add_element_validation(k, element.validate())

    def set_from_dict(
        self,
        config_dict: dict,
        root: bool = True,
        legacy: bool = False,
        legacy_lookup=None,
    ):
        """
        Set the values of all :class: `ConfigGroup` or :class:`ConfigItem` elements.

        :param config_dict: A dictionary representing values of all config elements.
        :param root: Whether the element is a base level element or not.
            if the element is a root then it should validate all of its descendants.
        :param legacy: Whether to use the alias names for config elements to construct the config from a legacy dictionary.
        """
        if legacy:
            if legacy_lookup is None:
                legacy_lookup = self.to_legacy_dict()

            for element_name, v in config_dict.items():
                element: ConfigItem = legacy_lookup.get(element_name)
                if isinstance(v, dict):
                    self.set_from_dict(
                        v, legacy=True, root=False, legacy_lookup=legacy_lookup
                    )
                if element is not None:
                    element.set_value(v)
        else:
            for element_name, v in config_dict.items():
                element = getattr(self, element_name, None)
                if isinstance(v, dict) and isinstance(element, ConfigGroup):
                    element.set_from_dict(v, False)
                elif not isinstance(v, dict) and isinstance(element, ConfigItem):
                    element.set_value(v)
        if root:
            self.validate()

    def set_from_yaml(self, file_path: str, legacy: bool = False):
        """
        Set the elements of the group from a .yaml file.

        :param file_path: The path to the .yaml file.
        :param legacy: Whether to use the alias names for config elements to construct the config from a legacy dictionary.
        """
        try:
            with open(file_path) as f:
                config_dict = yaml.safe_load(f)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {file_path}"
            _LOGGER.critical(msg, exc_info=True)
            raise e
        self.set_from_dict(config_dict, legacy=legacy)

    def to_yaml(self, file_path: str):
        """
        Save the values of the elements of the group to a .yaml file.

        :param file_path: The path to the .yaml file
        """
        with open(file_path, "w") as file:
            yaml.safe_dump(
                self.to_dict(values_only=True),
                file,
                sort_keys=False,
                default_flow_style=False,
            )
