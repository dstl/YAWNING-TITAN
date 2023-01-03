from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Union

from yawning_titan.config.item_types.core import (
    ConfigItem,
    ConfigItemValidation,
    ItemTypeProperties,
)
from yawning_titan.exceptions import ConfigItemValidationError


class Parity(Enum):
    """Integer parity."""

    ODD = 1
    EVEN = 2

    def __str__(self):
        """:return: The Parity name as a string."""
        return str(self.name)


@dataclass()
class IntProperties(ItemTypeProperties):
    """The IntProperties class holds the properties relevant for defining and validating an int value."""

    min_val: Optional[int] = None
    """A minimum int value."""
    exclusive_min: Optional[bool] = None
    """Indicates whether `min_val` is exclusive of the value (>, rather than >=)."""
    max_val: Optional[int] = None
    """A maximum int value."""
    exclusive_max: Optional[bool] = None
    """Indicates whether `max_val` is exclusive of the value (<, rather than <=)."""
    parity: Optional[Parity] = None
    """The integer parity."""
    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[int] = None
    """The default value"""

    def __post_init__(self):
        # Validate the default value to ensure it is a 'legal' default
        if self.default:
            validated_default = self.validate(self.default)
            if not validated_default.passed:
                raise validated_default.fail_exception

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Serializes the :class:`IntProperties` as a dict.

        :return: The :class:`IntProperties` as a dict.
        """
        config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        if "parity" in config_dict:
            config_dict["parity"] = str(config_dict["parity"])
        if self.allow_null is not None:
            config_dict["allow_null"] = self.allow_null
        return config_dict

    def validate(self, val: int) -> ConfigItemValidation:
        """
        Validates an int against the properties set in :class:`IntProperties`.

        :param val: A int to be validated.
        :return: An instance of :class:`config_toolbox.config.types.ValueValidation`.
        :raise: :class:`config_toolbox.exceptions.ValidationError` when validation fails.
        """
        msg = None
        try:
            if not self.allow_null and val is None:
                msg = f"Value {val} when allow_null is not permitted."
                raise ConfigItemValidationError(msg)
            if val is not None:
                msg = f"Value {val} is"
                if not isinstance(val, int):
                    msg = f"{msg} of type {type(val)}, not {int}."
                    raise ConfigItemValidationError(msg)

                if self.exclusive_min:
                    if self.min_val is not None and val <= self.min_val:
                        msg = (
                            f"{msg} less than the min property {self.min_val+1} "
                            f"(min={self.min_val} exclusive of this value)."
                        )
                        raise ConfigItemValidationError(msg)
                else:
                    if self.min_val is not None and val < self.min_val:
                        msg = f"{msg} less than the min property {self.min_val}."
                        raise ConfigItemValidationError(msg)

                if self.exclusive_max:
                    if self.max_val is not None and val >= self.max_val:
                        msg = (
                            f"{msg} greater than the max property {self.max_val-1} "
                            f"(max={self.max_val} exclusive of this value)."
                        )
                        print(msg)
                        raise ConfigItemValidationError(msg)
                else:
                    if self.max_val is not None and val > self.max_val:
                        msg = f"{msg} greater than the max property {self.max_val}."
                        print(msg)
                        raise ConfigItemValidationError(msg)

            if self.parity:
                if self.parity is Parity.EVEN and val % 2 != 0:
                    msg = f"{msg} not even."
                    raise ConfigItemValidationError(msg)
                if self.parity is Parity.ODD and val % 2 == 0:
                    msg = f"{msg} not odd."
                    raise ConfigItemValidationError(msg)

        except ConfigItemValidationError as e:
            return ConfigItemValidation(False, msg, e)
        return ConfigItemValidation()


@dataclass()
class IntItem(ConfigItem):
    """An int config item type."""

    def __init__(
        self,
        value: int,
        doc: Optional[str] = None,
        properties: Optional[IntProperties] = None,
    ):
        if properties:
            if not isinstance(properties, IntProperties):
                raise TypeError(
                    f"The properties param must be of type {IntProperties}, not {type(properties)}."
                )
        else:
            properties = IntProperties()
        super().__init__(value, doc, properties)
