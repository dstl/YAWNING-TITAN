from dataclasses import dataclass
from typing import List, Optional

from yawning_titan.config.toolbox.core import ConfigItem, ItemTypeProperties


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
                raise TypeError(
                    "Properties of BoolItem should be of type BoolProperties."
                )
        else:
            properties = BoolProperties()
        super().__init__(value, doc, alias, depends_on, properties)
