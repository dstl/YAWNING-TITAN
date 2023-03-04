from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

from yawning_titan.config.toolbox.core import (
    ConfigItem,
    ConfigItemValidation,
    ItemTypeProperties,
)
from yawning_titan.db.query import YawningTitanQuery
from yawning_titan.exceptions import ConfigItemValidationError


class Parity(Enum):
    """Integer parity."""

    ODD = 1
    EVEN = 2

    def __str__(self):
        """:return: The Parity name as a string."""
        return str(self.name)


# TODO: range should probably work more intuitively ie be represented by ['>=',a'<=',b]
@dataclass()
class IntProperties(ItemTypeProperties):
    """The IntProperties class holds the properties relevant for defining and validating an int value."""

    min_val: Optional[int] = None
    """A minimum int value."""
    inclusive_min: Optional[bool] = None
    """Indicates whether `min_val` is exclusive of the value (>=, rather than >)."""
    max_val: Optional[int] = None
    """A maximum int value."""
    inclusive_max: Optional[bool] = None
    """Indicates whether `max_val` is exclusive of the value (<=, rather than <)."""
    parity: Optional[Parity] = None
    """The integer parity."""
    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[int] = None
    """The default value"""

    def __post_init__(self):
        self._allowed_types = [int]
        super().__post_init__()

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Serializes the :class:`IntProperties` as a dict.

        :return: The :class:`IntProperties` as a dict.
        """
        config_dict = super().to_dict()
        if "parity" in config_dict:
            config_dict["parity"] = str(config_dict["parity"])
        if self.allow_null is not None:
            config_dict["allow_null"] = self.allow_null
        return config_dict

    def validate(self, val: int) -> ConfigItemValidation:
        """
        Validates an int against the properties set in :class:`IntProperties`.

        :param val: A int to be validated.
        :return: An instance of :class:`~yawning_titan.config.item_types.ConfigItemValidation`.
        :raise: :class:`~yawning_titan.exceptions.ConfigItemValidationError` when validation fails.
        """
        validation: ConfigItemValidation = super().validate(val)

        if val is not None and type(val) in self._allowed_types:
            try:
                if self.min_val is not None and val < self.min_val:
                    msg = f"Value {val} is less than the min property {self.min_val}."
                    raise ConfigItemValidationError(msg)
                elif (
                    self.min_val is not None
                    and not self.inclusive_min
                    and val == self.min_val
                ):
                    msg = f"Value {val} is equal to the min value {self.min_val} but the range is not inclusive of this value."
                    raise ConfigItemValidationError(msg)

                if self.max_val is not None and val > self.max_val:
                    msg = (
                        f"Value {val} is greater than the max property {self.max_val}."
                    )
                    raise ConfigItemValidationError(msg)
                elif (
                    self.max_val is not None
                    and not self.inclusive_max
                    and val == self.max_val
                ):
                    msg = f"Value {val} is equal to the max value {self.max_val} but the range is not inclusive of this value."
                    raise ConfigItemValidationError(msg)

            except ConfigItemValidationError as e:
                validation.add_validation(msg, e)

            if self.parity:
                try:
                    if self.parity is Parity.EVEN and val % 2 != 0:
                        msg = f"Value {val} is not even."
                        raise ConfigItemValidationError(msg)
                    if self.parity is Parity.ODD and val % 2 == 0:
                        msg = f"Value {val} is not odd."
                        raise ConfigItemValidationError(msg)

                except ConfigItemValidationError as e:
                    validation.add_validation(msg, e)

        return validation


@dataclass()
class IntItem(ConfigItem):
    """An int config item type."""

    def __init__(
        self,
        value: bool,
        doc: Optional[str] = None,
        query: YawningTitanQuery = None,
        alias: Optional[str] = None,
        depends_on: Optional[List[str]] = None,
        properties: Optional[IntProperties] = None,
    ):
        if properties:
            if not isinstance(properties, IntProperties):
                raise TypeError(
                    "Properties of IntItem should be of type IntProperties."
                )
        else:
            properties = IntProperties()
        super().__init__(value, doc, query, alias, depends_on, properties)
