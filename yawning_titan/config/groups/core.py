from typing import Optional, Union

from yawning_titan.config.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.groups.validation import AnyNonZeroGroup
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.config.item_types.int_item import IntItem, IntProperties
from yawning_titan.exceptions import ConfigGroupValidationError

# TODO: make a factory class for actionX group


class ActionLikelihoodGroup(ConfigGroup):
    """Group to represent an action, likelihood common config group."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: bool = False,
        likelihood: Optional[Union[float, int]] = None,
    ):
        """The `ActionLikelihoodGroup` constructor.

        :param use: Whether to use the action or not.
        :param likelihood: The likelihood of the action.
        :param doc: An optional descriptor.
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc="Whether to use the action or not.",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.likelihood: FloatItem = FloatItem(
            value=likelihood,
            doc="The likelihood of the action.",
            properties=FloatProperties(
                allow_null=True,
                min_val=0,
                inclusive_min=True,
            ),
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """
        Validate the `ActionLikelihoodGroup`.

        This is done at two levels:
            1. A group level validation is performed that checks if likelihood
            and chance are provided when use is True.
            2. An item level validation is performed by calling .validate on
            the use and likelihood config items.

        :return: An instance of ConfigGroupValidation.
        """
        super().validate()
        if self.use.value is True:
            try:
                if self.likelihood.value is None:
                    msg = "Likelihood cannot be null when use=True"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)

        return self.validation


class ActionLikelihoodChanceGroup(ActionLikelihoodGroup):
    """Group to represent an action, likelihood, and chance common config group."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: bool = False,
        likelihood: Optional[Union[float, int]] = None,
        chance: Optional[Union[float, int]] = None,
    ):
        """The `ActionLikelihoodChanceGroup` constructor.

        :param use: Whether to use the action or not.
        :param likelihood: The likelihood of the action.
        :param chance: The chance of the action.
        :param doc: An optional descriptor.
        """
        self.chance: FloatItem = FloatItem(
            value=chance,
            doc="The chance of the action.",
            properties=FloatProperties(
                allow_null=True,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
        )
        super().__init__(doc, use, likelihood)

    def validate(self) -> ConfigGroupValidation:
        """
        Validate the `ActionLikelihoodChanceGroup`.

        This is done at two levels:
            1. A group level validation is performed that checks if likelihood
            and chance are provided when use is True.
            2. An item level validation is performed by calling .validate on
            the use, likelihood, and chance config items.

        :return: An instance of ConfigGroupValidation.
        """
        super().validate()

        if self.use.value is True:
            try:
                if self.chance.value is None:
                    msg = "Chance cannot be null when use=True"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)

        return self.validation


class UseValueGroup(ConfigGroup):
    """Group of values that collectively describe whether an item is used and if so what value to use with."""

    def __init__(
        self, doc: Optional[str] = None, use: bool = False, value: float = None
    ):
        """
        The `UseValueGroup` constructor.

        :param use: Whether to use the action or not.
        :param value: The value of the item.
        :param doc: An optional descriptor.
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc="Whether to use the action or not.",
            properties=BoolProperties(allow_null=False),
        )
        self.value: FloatItem = FloatItem(
            value=value,
            doc="The value of the item.",
            properties=FloatProperties(
                allow_null=True,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
        )
        super().__init__(doc)


class NodeChanceGroup(AnyNonZeroGroup):
    """Group to indicate chances of success for different node types."""

    def __init__(
        self,
        doc: Optional[str] = None,
        standard_node: Optional[Union[int, float]] = 0.5,
        deceptive_node: Optional[Union[int, float]] = 0.5,
    ):
        self.standard_node = FloatItem(
            value=standard_node,
            doc="The chance of the action succeeding for a standard node",
            properties=FloatProperties(
                allow_null=True,
                default=0.5,
                min_val=0,
                max_val=1,
                inclusive_min=False,
                inclusive_max=True,
            ),
        )
        self.deceptive_node = FloatItem(
            value=deceptive_node,
            doc="The chance of the action succeeding for a deceptive node",
            properties=FloatProperties(
                allow_null=True,
                default=0.5,
                min_val=0,
                max_val=1,
                inclusive_min=False,
                inclusive_max=True,
            ),
        )
        super().__init__(doc)


class UseChancesGroup(ConfigGroup):
    """Group to indicate whether an element is used and its associated chance of success for different node types."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        chance: NodeChanceGroup = None,
    ):
        self.use: BoolItem = BoolItem(
            doc="Whether the element is used",
            value=use,
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.chance: NodeChanceGroup = (
            chance
            if chance
            else NodeChanceGroup(doc="The chance(s) of the result occurring.")
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()
        if self.use.value is True:
            try:
                if (
                    self.chance.deceptive_node.value <= self.chance.standard_node.value
                ) and self.chance.deceptive_node.value != 1:
                    msg = "the detection chance of an attack on a deceptive node should be greater than that of a standard node."
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation


class RestrictRangeGroup(ConfigGroup):
    """:class:`~yawning_titan.config.base.core.ConfigGroup` to restrict the range of a given attribute to within :attribute: `min` and :attribute: `max`."""

    def __init__(
        self,
        doc: Optional[str] = None,
        restrict: Optional[bool] = False,
        min: Optional[int] = None,
        max: Optional[int] = None,
    ):
        self.restrict = BoolItem(
            value=restrict,
            doc="Whether to restrict this attribute.",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.min: IntItem = IntItem(
            value=min,
            doc="The minimum value of the attribute to restrict.",
            properties=IntProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        self.max: IntItem = IntItem(
            value=max,
            doc="The maximum value of the attribute to restrict.",
            properties=IntProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
        super().validate()

        if self.restrict.value:
            try:
                if all(e is None for e in [self.min.value, self.max.value]):
                    msg = "If an element is to be range bound either the min or max bounds must be set."
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)

            try:
                if (
                    all(e is not None for e in [self.min.value, self.max.value])
                    and self.min.value > self.max.value
                ):
                    msg = f"The minimum value of a range bound item ({self.min.value}) cannot be larger than the maximum value ({self.max.value})."
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation
