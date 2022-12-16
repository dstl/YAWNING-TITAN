from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Union

from yawning_titan.config.item_types.core import ConfigItem, ConfigValidation, ItemTypeProperties
from yawning_titan.exceptions import ConfigValidationError


@dataclass()
class BoolProperties(ItemTypeProperties):
    """
    The :class:`BoolProperties` class holds the properties relevant for defining
    and validating a bool value.
    """

    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[bool] = None
    """The default value"""

    def __post_init__(self):
        if self.default:
            validated_default = self.validate(self.default)
            if not validated_default.passed:
                raise validated_default.fail_exception

    def to_dict(self) -> Dict[str, Union[bool, str]]:
        """
        Serializes the :class:`BoolProperties` as a dict.

        :return: The :class:`BoolProperties` as a dict.
        """
        config_dict = {k: v for k, v in self.__dict__.items() if v is not None}

        return config_dict

    def validate(self, val: bool) -> ConfigValidation:
        """
        Validates a bool against the properties set in :class:`BoolProperties`.

        :param val: A bool to be validated.
        :return: An instance of :class:`config_toolbox.config.types.ValueValidation`.
        :raise: :class:`config_toolbox.exceptions.ValidationError` when validation fails.
        """
        try:
            if not self.allow_null and val is None:
                msg = f"Value {val} when allow_null is not permitted."
                raise ConfigValidationError(msg)
            if val is not None:
                if not isinstance(val, bool):
                    msg = f"Value {val} is of type {type(val)}, not {bool}."
                    raise ConfigValidationError(msg)
        except ConfigValidationError as e:
            return ConfigValidation(False, msg, e)
        return ConfigValidation()


@dataclass()
class BoolItem(ConfigItem):

    def __init__(self, value: bool, doc: Optional[str] = None,
                 properties: Optional[BoolProperties] = None):
        if not properties:
            properties = BoolProperties()
        super().__init__(value, doc, properties)