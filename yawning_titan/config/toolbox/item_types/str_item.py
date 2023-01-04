from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from yawning_titan.config.toolbox.core import (
    ConfigItem,
    ConfigItemValidation,
    ItemTypeProperties,
)
from yawning_titan.exceptions import ConfigItemValidationError, InvalidPropertyTypeError


@dataclass()
class StrProperties(ItemTypeProperties):
    """The BoolProperties class holds the properties relevant for defining and validating a bool value."""

    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[bool] = None
    """The default value"""
    options: Optional[List[str]] = None
    """A list of allowed values for the item."""

    def __post_init__(self):
        self._allowed_types = [str]
        super().__post_init__()

    def to_dict(self) -> Dict[str, Union[bool, str]]:
        """
        Serializes the :class:`BoolProperties` as a dict.

        :return: The :class:`BoolProperties` as a dict.
        """
        config_dict = {k: v for k, v in self.__dict__.items() if v is not None}

        return config_dict

    def validate(self, val: bool) -> ConfigItemValidation:
        """
        Validates a bool against the properties set in :class:`BoolProperties`.

        :param val: A bool to be validated.
        :return: An instance of :class:`config_toolbox.config.types.ValueValidation`.
        :raise: :class:`config_toolbox.exceptions.ValidationError` when validation fails.
        """
        validation: ConfigItemValidation = super().validate(val)

        if val is not None:
            try:
                if self.options is not None and val not in self.options:
                    msg = f"Value {val} should be one of {', '.join(self.options)}"
                    raise ConfigItemValidationError(msg)
            except ConfigItemValidationError as e:
                validation.add_validation(msg, e)

        return validation


@dataclass()
class StrItem(ConfigItem):
    """The bool config item."""

    def __init__(
        self,
        value: bool,
        doc: Optional[str] = None,
        alias: Optional[str] = None,
        depends_on: Optional[List[str]] = None,
        properties: Optional[StrProperties] = None,
    ):
        if properties:
            if not isinstance(properties,StrProperties):
                raise InvalidPropertyTypeError("Properties of StrItem should be of type StrProperties.")
        else:
            properties = StrProperties()
        super().__init__(value, doc, alias, depends_on, properties)
