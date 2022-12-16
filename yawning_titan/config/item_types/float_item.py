from dataclasses import dataclass
from typing import Dict, Optional, Union

from yawning_titan.config.item_types.core import ConfigItem, ConfigValidation, ItemTypeProperties
from yawning_titan.exceptions import ConfigValidationError


@dataclass()
class FloatProperties(ItemTypeProperties):
    """
    The :class:`FloatProperties` class holds the properties relevant for defining
    and validating a float value.
    """

    min_val: Optional[float] = None
    """A minimum float value."""
    exclusive_min: Optional[bool] = None
    """Indicates whether `min_val` is exclusive of the value (>, rather than >=)."""
    max_val: Optional[float] = None
    """A maximum float value."""
    exclusive_max: Optional[bool] = None
    """Indicates whether `max_val` is exclusive of the value (<, rather than <=)."""
    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[float] = None
    """The default value"""

    def __post_init__(self):
        if self.default:
            validated_default = self.validate(self.default)
            if not validated_default.passed:
                raise validated_default.fail_exception

    def to_dict(self) -> Dict[str, Union[float, str]]:
        """
        Serializes the :class:`FloatProperties` as a dict.

        :return: The :class:`FloatProperties` as a dict.
        """
        config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.allow_null is not None:
            config_dict["allow_null"] = self.allow_null
        return config_dict

    def validate(self, val: float) -> ConfigValidation:
        """
        Validates a float against the properties set in :class:`FloatProperties`.

        :param val: A float to be validated.
        :return: An instance of :class:`config_toolbox.config.types.ValueValidation`.
        :raise: :class:`config_toolbox.exceptions.ValidationError` when validation fails.
        """
        msg = None
        try:
            if not self.allow_null and val is None:
                msg = f"Value {val} when allow_null is not permitted."
                raise ConfigValidationError(msg)
            if val is not None:
                msg = f"Value {val} is"
                if not isinstance(val, float):
                    msg = f"{msg} of type {type(val)}, not {float}."
                    raise ConfigValidationError(msg)

                if self.exclusive_min:
                    if self.min_val is not None and val <= self.min_val:
                        msg = f"{msg} less than the min property {self.min_val+1} " \
                              f"(min={self.min_val} exclusive of this value)."
                        raise ConfigValidationError(msg)
                else:
                    if self.min_val is not None and val < self.min_val:
                        msg = f"{msg} less than the min property {self.min_val}."
                        raise ConfigValidationError(msg)

                if self.exclusive_max:
                    if self.max_val is not None and val >= self.max_val:
                        msg = f"{msg} greater than the max property {self.max_val-1} " \
                              f"(max={self.max_val} exclusive of this value)."
                        print(msg)
                        raise ConfigValidationError(msg)
                else:
                    if self.max_val is not None and val > self.max_val:
                        msg = f"{msg} greater than the max property {self.max_val}."
                        print(msg)
                        raise ConfigValidationError(msg)

        except ConfigValidationError as e:
            return ConfigValidation(False, msg, e)
        return ConfigValidation()


@dataclass()
class FloatItem(ConfigItem):

    def __init__(self, value: float, doc: Optional[str] = None,
                 properties: Optional[FloatProperties] = None):
        if not properties:
            properties = FloatProperties()
        super().__init__(value, doc, properties)