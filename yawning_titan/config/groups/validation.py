# -- Validation groups --

from yawning_titan.config.core import (
    ConfigGroup,
    ConfigGroupValidation,
    ConfigItem,
)
from yawning_titan.config.item_types.bool_item import BoolItem
from yawning_titan.config.item_types.float_item import FloatItem
from yawning_titan.config.item_types.int_item import IntItem
from yawning_titan.exceptions import ConfigGroupValidationError


class AnyNonZeroGroup(ConfigGroup):
    """Inherit from this group if any value should be greater 0 in order to be valid."""

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        try:
            elements = self.get_config_elements([IntItem, FloatItem])
            if not any(
                e.value > 0 for e in elements.values() if type(e.value) in [int, float]
            ):
                msg = f"At least 1 of {', '.join(elements.keys())} should be above 0"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class AnyTrueGroup(ConfigGroup):
    """Inherit from this group if any value should be True."""

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        try:
            elements = self.get_config_elements(BoolItem)
            if not any(e.value is True for e in elements.values()):
                msg = f"At least 1 of {', '.join(elements.keys())} should be True"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class AnyUsedGroup(ConfigGroup):
    """Inherit from this group if any element should have a value of `True` or should be a group with `use` as `True`."""

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        try:
            values = [e.value for e in self.get_config_elements(ConfigItem).values()]
            values.extend(
                [
                    g.use.value
                    for g in self.get_config_elements(ConfigGroup).values()
                    if hasattr(g, "use")
                ]
            )
            if not any(v is True for v in values):
                msg = f"At least 1 of {', '.join(self.get_config_elements().keys())} should be used"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation
