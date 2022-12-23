# from __future__ import annotations

# from abc import ABC, abstractmethod
# from collections.abc import Iterable
# from dataclasses import dataclass
# from typing import Any, Dict, List, Optional, Union

# import yaml

# from yawning_titan.exceptions import (
#     ConfigGroupValidationError,
#     ConfigItemValidationError,
# )


# @dataclass()
# class ConfigItemValidation:
#     """
#     :class:`ConfigItemValidation` is used to return a validation result.

#     If validation fails, a reason why and any exception raised are returned.
#     """

#     passed: Optional[bool] = True
#     """``True`` if the _value has passed validation, otherwise ``False``."""
#     fail_reason: Optional[str] = None
#     """The reason why validation failed."""
#     fail_exception: Optional[Exception] = None
#     """The :class:`Exception` raised when validation failed."""


# class ConfigGroupCore:
#     """Used to provide helper methods to represent a ConfigGroup object."""

#     def get_config_elements(
#         self, _type: Union[ConfigItem, ConfigGroup] = None
#     ) -> Dict[str, Union[ConfigItem, ConfigGroup]]:
#         if _type is not None:
#             return {k: v for k, v in self.__dict__.items() if isinstance(v, _type)}
#         return {
#             k: v
#             for k, v in self.__dict__.items()
#             if isinstance(v, ConfigItem) or isinstance(v, ConfigGroup)
#         }

#     def get_non_config_elements(self) -> Dict[str, Any]:
#         return {
#             k: v
#             for k, v in self.__dict__.items()
#             if k not in self.get_config_elements()
#         }

#     def stringify(self):
#         string = f"{self.__class__.__name__}("
#         strings = [
#             f"{name}={val.stringify()}"
#             for name, val in self.get_config_elements().items()
#         ]
#         strings.extend(
#             [f"{name}={val}" for name, val in self.get_non_config_elements().items()]
#         )
#         return string + ", ".join(strings) + ")"

#     def __repr__(self) -> str:
#         return self.stringify()

#     def __str__(self) -> str:
#         return self.stringify()

#     def __hash__(self) -> int:
#         element_hash = [v.stringify() for v in self.get_config_elements().values()]
#         element_hash.extend(
#             [
#                 tuple(v) if isinstance(v, Iterable) else v
#                 for v in self.get_non_config_elements().values()
#             ]
#         )
#         return hash(tuple(element_hash))

#     def __eq__(self, other) -> bool:
#         if isinstance(other, self.__class__):
#             return hash(self) == hash(other)
#         return False


# class ConfigGroupValidation(ConfigGroupCore):
#     """
#     Used to return a validation result for a group of dependant config items, and the list of item validations.

#     If validation fails, a reason why and any exception raised are returned.
#     """

#     def __init__(
#         self,
#         passed: bool = True,
#         fail_reason: Optional[str] = None,
#         fail_exception: Optional[ConfigGroupValidationError] = None,
#     ):
#         self.passed: bool = passed
#         self.fail_reasons: List[str] = [fail_reason] if fail_reason is not None else []
#         self.fail_exceptions: List[ConfigGroupValidationError] = (
#             [fail_exception] if fail_exception is not None else []
#         )
#         self._element_validation = {}

#     def add_element_validation(
#         self,
#         element_name: str,
#         validation: Union[ConfigItemValidation, ConfigGroupValidation],
#     ):
#         """
#         Add a :class:`ConfigItemValidation` or :class:`ConfigGroupValidation` to the item validation dict.

#         :param element_name: The name of the element.
#         :param validation: the instance of ConfigItemValidation.
#         """
#         self._element_validation[element_name] = validation

#     def add_validation(self, fail_reason: str, exception: ConfigGroupValidationError):
#         self.passed = False
#         if fail_reason not in self.fail_reasons:
#             self.fail_reasons.append(fail_reason)
#         if exception not in self.fail_exceptions:
#             self.fail_exceptions.append(exception)

#     def to_dict(self, element_name: str = "root", root: bool = True) -> dict:
#         """
#         Express the error tree as a dictionary.

#         :param element_name: A string name for the element to be represented.

#         :return: A dict of element names to validation errors or validation dictionaries.
#         """
#         if self.passed:
#             d = {}
#         else:
#             d = {"group": self.fail_reasons}
#         for e, validation in self.element_validation.items():
#             if isinstance(validation, ConfigGroupValidation) and (
#                 not validation.group_passed or not validation.passed
#             ):
#                 d[e] = validation.to_dict(e, False)
#             elif not validation.passed:
#                 d[e] = validation.fail_reason
#         if root:
#             return {element_name: d}
#         return d

#     def log(self, element_name: str = "root") -> None:
#         """
#         Return the validation results as a formatted string.

#         :param element_name: A string name for the element to be represented.
#         """
#         string = "\nValidation results\n" "------------------\n"
#         d = self.to_dict(element_name)
#         if d:
#             string += yaml.dump(d, sort_keys=False)
#         else:
#             string += d.get(element_name, "Passed")
#         print(string)

#     @property
#     def element_validation(self) -> Dict[str, ConfigItemValidation]:
#         """
#         The dict of element to :class:`ConfigItemValidation` and :class:`ConfigGroupValidation` validations.

#         :return: A dict.
#         """
#         return self._element_validation

#     @property
#     def group_passed(self) -> bool:
#         """
#         Returns True if all items passed validation, otherwise returns False.

#         :return: A bool.
#         """
#         return all(v.passed for v in self.element_validation.values())


# @dataclass()
# class ItemTypeProperties(ABC):
#     """An Abstract Base Class that is inherited by config data type properties."""

#     allow_null: Optional[bool] = None
#     """`True` if the config _value can be left empty, otherwise `False`."""
#     default: Optional[Any] = None
#     """The items default value."""

#     @abstractmethod
#     def to_dict(self) -> Dict[str, Any]:
#         """
#         An abstract method that returns the properties as a dict.

#         :return: A dict.
#         """
#         return {k: v for k, v in self.__dict__.items() if v is not None}

#     @abstractmethod
#     def validate(self, val) -> ConfigItemValidation:
#         """An abstract group validation."""
#         pass


# @dataclass()
# class ConfigItem:
#     """The ConfigItem class holds an items value, doc, and properties."""

#     value: object
#     """The items value."""
#     doc: Optional[str] = None
#     """The items doc."""
#     properties: Optional[ItemTypeProperties] = None
#     """The items properties."""
#     validation: ConfigItemValidation = None
#     """The instance of ConfigItemValidation that provides access to the item validation details."""

#     def __post_init__(self):
#         if self.value is None and self.properties.default:
#             self.value = self.properties.default
#         self.validation = self.properties.validate(self.value)

#     def to_dict(self, as_key_val_pair: bool = False):
#         """
#         Return the ConfigItem as a dict.

#         :param as_key_val_pair: If true, the dict is returned as a value in
#             a key/value pair, the key being the class name.
#         :return: The ConfigItem as a dict.
#         """
#         d = {"value": self.value}
#         if self.doc:
#             d["doc"] = self.doc
#         if self.properties:
#             d["properties"] = self.properties.to_dict()
#         if as_key_val_pair:
#             return {self.__class__.__name__: d}
#         return d

#     def validate(self) -> ConfigItemValidation:
#         """
#         Validate the item against its properties.

#         If no properties exist,
#         simply return a default passed :class:`ConfigItemValidation`.

#         :return: An instance of :class:`ConfigItemValidation`.
#         """
#         # print("VALIDATING ITEM")
#         if self.properties:
#             return self.properties.validate(self.value)
#         return ConfigItemValidation()

#     def set_value(self, value: Any) -> None:
#         """
#         Set the value of the :class:`ConfigItem` after construction.

#         :param value: The value to be set.
#         """
#         self.value = value
#         # self.validate()

#     def stringify(self):
#         return self.value


# class ConfigGroup(ConfigGroupCore, ABC):
#     """The ConfigGroup class holds a ConfigItem's, doc, properties, and a ConfigItemValidation."""

#     def __init__(self, doc: Optional[str] = None):
#         """The ConfigGroup constructor.

#         :param doc: The groups doc.
#         """
#         self.doc: Optional[str] = doc
#         self.validation = self.validate()

#     # @abstractmethod
#     def validate(self) -> ConfigGroupValidation:
#         """
#         Validate the grouped items against their properties.

#         :return: An instance of :class:`ConfigGroupValidation`.
#         """
#         # print("VALIDATE IN BASE CONFIG GROUP")
#         if not hasattr(self, "validation"):
#             # print("SETTING VALIDATION ATTR")
#             self.validation = ConfigGroupValidation()
#         self.validate_elements()
#         return self.validation

#     # @abstractmethod
#     def to_dict(self):  # TODO: replace with generic method
#         """
#         Return the ConfigGroup as a dict.

#         :return: The ConfigGroup as a dict.
#         """
#         attr_dict = {"doc": self.doc} if self.doc is not None else {}
#         element_dict = {k: e.to_dict() for k, e in self.get_config_elements().items()}
#         return {**attr_dict, **element_dict}

#     def validate_elements(self):
#         """
#         Call the .validate() method on each of the elements in the group.
#         """
#         for k, element in self.get_config_elements().items():
#             self.validation.add_element_validation(k, element.validate())

#     def set_from_dict(self, config_dict: dict, root: bool = True):
#         """

#         :param config_dict: _description_
#         :type config_dict: dict
#         """
#         # print("-----------------\nSETTING FROM DICT\n-----------------")
#         for element_name, v in config_dict.items():
#             element = getattr(self, element_name, None)
#             if type(v) == dict and isinstance(element, ConfigGroup):
#                 element.set_from_dict(v, False)
#             elif type(v) != dict and isinstance(element, ConfigItem):
#                 element.set_value(v)
#         if root:
#             self.validate()


# from dataclasses import dataclass, field
# from typing import Dict, List, Optional, Union

# from yawning_titan.config.toolbox.core import (
#     ConfigItem,
#     ConfigItemValidation,
#     ItemTypeProperties,
# )
# from yawning_titan.exceptions import ConfigItemValidationError


# @dataclass()
# class FloatProperties(ItemTypeProperties):
#     """The FloatProperties class holds the properties relevant for defining and validating a float value."""

#     min_val: Optional[float] = None
#     """A minimum float value."""
#     inclusive_min: Optional[bool] = None
#     """Indicates whether `min_val` is inclusive of the value (>=, rather than >)."""
#     max_val: Optional[float] = None
#     """A maximum float value."""
#     inclusive_max: Optional[bool] = None
#     """Indicates whether `max_val` is exclusive of the value (<=, rather than <)."""
#     allow_null: Optional[bool] = None
#     """`True` if the config value can be left empty, otherwise `False`."""
#     default: Optional[float] = None
#     """The default value"""

#     def __post_init__(self):
#         if self.default:
#             validated_default = self.validate(self.default)
#             if not validated_default.passed:
#                 raise validated_default.fail_exception

#     def to_dict(self) -> Dict[str, Union[float, str]]:
#         """
#         Serializes the :class:`FloatProperties` as a dict.

#         :return: The :class:`FloatProperties` as a dict.
#         """
#         config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
#         if self.allow_null is not None:
#             config_dict["allow_null"] = self.allow_null
#         return config_dict

#     def validate(self, val: float) -> ConfigItemValidation:
#         """
#         Validates a float against the properties set in :class:`FloatProperties`.

#         :param val: A float or int value to be validated.
#         :return: An instance of :class:`~yawning_titan.config.item_types.ConfigItemValidation`.
#         :raise: :class:`~yawning_titan.exceptions.ConfigItemValidationError` when validation fails.
#         """
#         msg = None
#         # TODO: make each element callable in turn like on ConfigGroup i.e. use add_validation()
#         try:
#             if not self.allow_null and val is None:
#                 msg = f"Value {val} when allow_null is not permitted."
#                 raise ConfigItemValidationError(msg)
#             if val is not None:
#                 if not any(isinstance(val, _type) for _type in [int, float]):
#                     msg = (
#                         f"Value {val} is of type {type(val)}, should be "
#                         + " or ".join(map(str, [int, float]))
#                         + "."
#                     )
#                     raise ConfigItemValidationError(msg)

#                 msg = f"Value {val} is"
#                 if self.inclusive_min:
#                     if self.min_val is not None and val <= self.min_val:
#                         msg = (
#                             f"{msg} less than the min property {self.min_val+1} "
#                             f"(min={self.min_val} exclusive of this value)."
#                         )
#                         raise ConfigItemValidationError(msg)
#                 else:
#                     if self.min_val is not None and val < self.min_val:
#                         msg = f"{msg} less than the min property {self.min_val}."
#                         raise ConfigItemValidationError(msg)

#                 if self.inclusive_max:
#                     if self.max_val is not None and val >= self.max_val:
#                         msg = (
#                             f"{msg} greater than the max property {self.max_val-1} "
#                             f"(max={self.max_val} exclusive of this value)."
#                         )
#                         print(msg)
#                         raise ConfigItemValidationError(msg)
#                 else:
#                     if self.max_val is not None and val > self.max_val:
#                         msg = f"{msg} greater than the max property {self.max_val}."
#                         print(msg)
#                         raise ConfigItemValidationError(msg)

#         except ConfigItemValidationError as e:
#             return ConfigItemValidation(False, msg, e)
#         return ConfigItemValidation()


# @dataclass()
# class FloatItem(ConfigItem):
#     """A float config item."""

#     def __init__(
#         self,
#         value: float,
#         doc: Optional[str] = None,
#         properties: Optional[FloatProperties] = None,
#     ):
#         if not properties:
#             properties = FloatProperties()
#         super().__init__(value, doc, properties)


# from dataclasses import dataclass
# from typing import Dict, Optional, Union

# from yawning_titan.config.toolbox.core import (
#     ConfigItem,
#     ConfigItemValidation,
#     ItemTypeProperties,
# )
# from yawning_titan.exceptions import ConfigItemValidationError


# @dataclass()
# class BoolProperties(ItemTypeProperties):
#     """The BoolProperties class holds the properties relevant for defining and validating a bool value."""

#     allow_null: Optional[bool] = None
#     """`True` if the config value can be left empty, otherwise `False`."""
#     default: Optional[bool] = None
#     """The default value"""

#     def __post_init__(self):
#         if self.default:
#             validated_default = self.validate(self.default)
#             if not validated_default.passed:
#                 raise validated_default.fail_exception

#     def to_dict(self) -> Dict[str, Union[bool, str]]:
#         """
#         Serializes the :class:`BoolProperties` as a dict.

#         :return: The :class:`BoolProperties` as a dict.
#         """
#         config_dict = {k: v for k, v in self.__dict__.items() if v is not None}

#         return config_dict

#     def validate(self, val: bool) -> ConfigItemValidation:
#         """
#         Validates a bool against the properties set in :class:`BoolProperties`.

#         :param val: A bool to be validated.
#         :return: An instance of :class:`config_toolbox.config.types.ValueValidation`.
#         :raise: :class:`config_toolbox.exceptions.ValidationError` when validation fails.
#         """
#         try:
#             if not self.allow_null and val is None:
#                 msg = f"Value {val} when allow_null is not permitted."
#                 raise ConfigItemValidationError(msg)
#             if val is not None:
#                 if not isinstance(val, bool):
#                     msg = f"Value {val} is of type {type(val)}, not {bool}."
#                     raise ConfigItemValidationError(msg)
#         except ConfigItemValidationError as e:
#             return ConfigItemValidation(False, msg, e)
#         return ConfigItemValidation()


# @dataclass()
# class BoolItem(ConfigItem):
#     """The bool config item."""

#     def __init__(
#         self,
#         value: bool,
#         doc: Optional[str] = None,
#         properties: Optional[BoolProperties] = None,
#     ):
#         if not properties:
#             properties = BoolProperties()
#         super().__init__(value, doc, properties)


# from dataclasses import dataclass
# from enum import Enum
# from typing import Dict, Optional, Union

# from yawning_titan.config.toolbox.core import (
#     ConfigItem,
#     ConfigItemValidation,
#     ItemTypeProperties,
# )
# from yawning_titan.exceptions import ConfigItemValidationError


# class Parity(Enum):
#     """Integer parity."""

#     ODD = 1
#     EVEN = 2

#     def __str__(self):
#         """:return: The Parity name as a string."""
#         return str(self.name)


# # TODO: range should probably work more intuitively ie be represented by ['>=',a'<=',b]
# @dataclass()
# class IntProperties(ItemTypeProperties):
#     """The IntProperties class holds the properties relevant for defining and validating an int value."""

#     min_val: Optional[int] = None
#     """A minimum int value."""
#     inclusive_min: Optional[bool] = None
#     """Indicates whether `min_val` is exclusive of the value (>=, rather than >)."""
#     max_val: Optional[int] = None
#     """A maximum int value."""
#     inclusive_max: Optional[bool] = None
#     """Indicates whether `max_val` is exclusive of the value (<=, rather than <)."""
#     parity: Optional[Parity] = None
#     """The integer parity."""
#     allow_null: Optional[bool] = None
#     """`True` if the config value can be left empty, otherwise `False`."""
#     default: Optional[int] = None
#     """The default value"""

#     def __post_init__(self):
#         # Validate the default value to ensure it is a 'legal' default
#         if self.default:
#             validated_default = self.validate(self.default)
#             if not validated_default.passed:
#                 raise validated_default.fail_exception

#     def to_dict(self) -> Dict[str, Union[int, str]]:
#         """
#         Serializes the :class:`IntProperties` as a dict.

#         :return: The :class:`IntProperties` as a dict.
#         """
#         config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
#         if "parity" in config_dict:
#             config_dict["parity"] = str(config_dict["parity"])
#         if self.allow_null is not None:
#             config_dict["allow_null"] = self.allow_null
#         return config_dict

#     def validate(self, val: int) -> ConfigItemValidation:
#         """
#         Validates an int against the properties set in :class:`IntProperties`.

#         :param val: A int to be validated.
#         :return: An instance of :class:`~yawning_titan.config.item_types.ConfigItemValidation`.
#         :raise: :class:`~yawning_titan.exceptions.ConfigItemValidationError` when validation fails.
#         """
#         msg = None
#         # TODO: make each element callable in turn like on ConfigGroup i.e. use add_validation()
#         try:
#             if not self.allow_null and val is None:
#                 msg = f"Value {val} when allow_null is not permitted."
#                 raise ConfigItemValidationError(msg)
#             if val is not None:
#                 msg = f"Value {val} is"
#                 if not isinstance(val, int):
#                     msg = f"{msg} of type {type(val)}, not {int}."
#                     raise ConfigItemValidationError(msg)

#                 if self.inclusive_max:
#                     if self.min_val is not None and val <= self.min_val:
#                         msg = (
#                             f"{msg} less than the min property {self.min_val+1} "
#                             f"(min={self.min_val} exclusive of this value)."
#                         )
#                         raise ConfigItemValidationError(msg)
#                 else:
#                     if self.min_val is not None and val < self.min_val:
#                         msg = f"{msg} less than the min property {self.min_val}."
#                         raise ConfigItemValidationError(msg)

#                 if self.inclusive_max:
#                     if self.max_val is not None and val >= self.max_val:
#                         msg = (
#                             f"{msg} greater than the max property {self.max_val-1} "
#                             f"(max={self.max_val} exclusive of this value)."
#                         )
#                         print(msg)
#                         raise ConfigItemValidationError(msg)
#                 else:
#                     if self.max_val is not None and val > self.max_val:
#                         msg = f"{msg} greater than the max property {self.max_val}."
#                         print(msg)
#                         raise ConfigItemValidationError(msg)

#             if self.parity:
#                 if self.parity is Parity.EVEN and val % 2 != 0:
#                     msg = f"{msg} not even."
#                     raise ConfigItemValidationError(msg)
#                 if self.parity is Parity.ODD and val % 2 == 0:
#                     msg = f"{msg} not odd."
#                     raise ConfigItemValidationError(msg)

#         except ConfigItemValidationError as e:
#             return ConfigItemValidation(False, msg, e)
#         return ConfigItemValidation()


# @dataclass()
# class IntItem(ConfigItem):
#     """An int config item type."""

#     def __init__(
#         self,
#         value: int,
#         doc: Optional[str] = None,
#         properties: Optional[IntProperties] = None,
#     ):
#         if not properties:
#             properties = IntProperties()
#         super().__init__(value, doc, properties)
