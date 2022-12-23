# -- Validation groups --

from yawning_titan.config.toolbox.core import (
    ConfigGroup,
    ConfigGroupValidation,
    ConfigItem,
)
from yawning_titan.exceptions import ConfigGroupValidationError


class AnyNonZeroGroup(ConfigGroup):
    """Inherit from this group if any value should be greater 0 in order to be valid."""

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        # print("ANY NOT 0 VAL")
        super().validate()
        try:
            elements = self.get_config_elements(ConfigItem)
            if not any(e.value > 0 for e in elements.values()):
                msg = f"At least 1 of {', '.join(elements.keys())} should be above 0"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class AnyTrueGroup(ConfigGroup):
    """Inherit from this group if any value should be greater 0 in order to be valid."""

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        # print("ANY NOT 0 VAL")
        super().validate()
        try:
            elements = self.get_config_elements(ConfigItem)
            if not any(e.value is True for e in elements.values()):
                msg = f"At least 1 of {', '.join(elements.keys())} should be True"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation
