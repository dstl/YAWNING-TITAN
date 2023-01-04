from dataclasses import dataclass
from typing import List, Optional

from yawning_titan.config.toolbox.core import ConfigItem, ItemTypeProperties
from yawning_titan.exceptions import InvalidPropertyTypeError


@dataclass()
class BoolProperties(ItemTypeProperties):
    """The BoolProperties class holds the properties relevant for defining and validating a bool value."""

    allow_null: Optional[bool] = None
    """`True` if the config value can be left empty, otherwise `False`."""
    default: Optional[bool] = None
    """The default value"""

    def __post_init__(self):
        self._allowed_types = [bool]
        super().__post_init__()

    # def to_dict(self) -> Dict[str, Union[bool, str]]:
    #     """
    #     Serializes the :class:`BoolProperties` as a dict.

    #     :return: The :class:`BoolProperties` as a dict.
    #     """
    #     config_dict = {k: v for k, v in self.__dict__.items() if v is not None}

    #     return config_dict


@dataclass()
class BoolItem(ConfigItem):
    """The bool config item."""

    def __init__(
        self,
        value: bool,
        doc: Optional[str] = None,
        alias: Optional[str] = None,
        depends_on: Optional[List[str]] = None,
        properties: Optional[BoolProperties] = None,
    ):
        if properties:
            if not isinstance(properties, BoolProperties):
                raise InvalidPropertyTypeError(
                    "Properties of BoolItem should be of type BoolProperties."
                )
        else:
            properties = BoolProperties()
        super().__init__(value, doc, alias, depends_on, properties)
