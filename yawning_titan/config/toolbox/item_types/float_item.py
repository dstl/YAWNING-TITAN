from dataclasses import dataclass
from typing import Dict, Optional, Union

from yawning_titan.config.toolbox.core import (
    ConfigItem,
    ConfigItemValidation,
    ItemTypeProperties,
)
from yawning_titan.exceptions import ConfigItemValidationError


@dataclass()
class FloatProperties(ItemTypeProperties):
    """The FloatProperties class holds the properties relevant for defining and validating a float value."""

    min_val: Optional[float] = None
    """A minimum float value."""
    inclusive_min: Optional[bool] = None
    """Indicates whether `min_val` is inclusive of the value (>=, rather than >)."""
    max_val: Optional[float] = None
    """A maximum float value."""
    inclusive_max: Optional[bool] = None
    """Indicates whether `max_val` is exclusive of the value (<=, rather than <)."""
    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[float] = None
    """The default value"""

    def __post_init__(self):
        self.allowed_types = [float, int]
        super().__post_init__()

    # def __post_init__(self):
    #     if self.default:
    #         validated_default = self.validate(self.default)
    #         if not validated_default.passed:
    #             raise validated_default.fail_exception

    def to_dict(self) -> Dict[str, Union[float, int]]:
        """
        Serializes the :class:`FloatProperties` as a dict.

        :return: The :class:`FloatProperties` as a dict.
        """
        config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.allow_null is not None:
            config_dict["allow_null"] = self.allow_null
        return config_dict

    def validate(self, val: Union[float, int]) -> ConfigItemValidation:
        """
        Validates a float against the properties set in :class:`FloatProperties`.

        :param val: A float or int value to be validated.
        :return: An instance of :class:`~yawning_titan.config.item_types.ConfigItemValidation`.
        :raise: :class:`~yawning_titan.exceptions.ConfigItemValidationError` when validation fails.
        """
        validation: ConfigItemValidation = super().validate(val)
        if val is not None and type(val) in self.allowed_types:
            print(
                "FLOAT VALIDATING...",
                val,
                self.min_val,
                self.max_val,
                self.inclusive_min,
                self.inclusive_max,
            )
            try:
                msg = f"Value {val} is"
                if self.min_val is not None and val < self.min_val:
                    msg = f"{msg} less than the min property {self.min_val}."
                    raise ConfigItemValidationError(msg)
                elif (
                    self.min_val is not None
                    and not self.inclusive_min
                    and val == self.min_val
                ):
                    msg = f"{msg} is equal to {self.min_val} but the range is not inclusive of this value."
                    raise ConfigItemValidationError(msg)

                if self.max_val is not None and val > self.max_val:
                    msg = f"{msg} less than the min property {self.max_val}."
                    raise ConfigItemValidationError(msg)
                elif (
                    self.max_val is not None
                    and not self.inclusive_max
                    and val == self.max_val
                ):
                    msg = f"{msg} is equal to {self.max_val} but the range is not inclusive of this value."
                    raise ConfigItemValidationError(msg)

            except ConfigItemValidationError as e:
                validation.add_validation(msg, e)
        return validation


@dataclass()
class FloatItem(ConfigItem):
    """A float config item."""

    def __init__(
        self,
        value: float,
        doc: Optional[str] = None,
        properties: Optional[FloatProperties] = None,
    ):
        if not properties:
            properties = FloatProperties()
        super().__init__(value, doc, properties)
