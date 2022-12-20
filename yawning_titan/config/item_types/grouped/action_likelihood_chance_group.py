from typing import Dict, Optional, Union

from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.core import ConfigGroupValidation, ConfigGroup
from yawning_titan.config.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.exceptions import ConfigGroupValidationError


class ActionLikelihoodChanceGroup(ConfigGroup):
    """The ConfigGroup to represent an action, likelihood, and chance common config group."""

    def __init__(
        self,
        use: bool = False,
        likelihood: Optional[float] = None,
        chance: Optional[float] = None,
        doc: Optional[str] = None,
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param use: Whether to use the action or not.
        :param likelihood: The likelihood of the action.
        :param chance: The chance of the action.
        :param doc: An optional descriptor.
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc="Whether to use the action or not.",
            properties=BoolProperties(allow_null=False),
        )
        self.likelihood: FloatItem = FloatItem(
            value=likelihood,
            doc="The likelihood of the action.",
            properties=FloatProperties(allow_null=True, min_val=0, max_val=1),
        )
        self.chance: FloatItem = FloatItem(
            value=chance,
            doc="The chance of the action.",
            properties=FloatProperties(allow_null=True, min_val=0, max_val=1),
        )
        super().__init__(doc)
        

    def _items_map(self) -> Dict[str, Union[BoolItem, FloatItem]]:
        return {"use": self.use, "likelihood": self.likelihood, "chance": self.chance}

    def to_dict(self) -> Dict[str, Union[bool, float, str]]:
        """
        Return the ActionLikelihoodChance group as a dict.

        :return: The ActionLikelihoodChance group as a dict.
        """
        d = {"items": {}}
        for k, item in self._items_map().items():
            d["items"][k] = item.to_dict()
        if self.doc:
            d["doc"] = self.doc
        return d

    def validate(self) -> ConfigGroupValidation:
        """
        Validate the ActionLikelihoodChance group.

        This is done at two levels:
            1. A group level validation is performed that checks if likelihood
            and chance are provided when use is True.
            2. An item level validation is performed by calling .validate on
            the use, likelihood, and chance config items.

        :return: An instance of ConfigGroupValidation.
        """
        validation = ConfigGroupValidation()
        msg = None
        try:
            if self.use.value is True:
                msg = None
                if self.likelihood.value is None:
                    msg = "Likelihood cannot be null when use=True"
                    raise ConfigGroupValidationError(msg)
                if self.chance.value is None:
                    msg = "chance cannot be null when use=True"
                    raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            validation = ConfigGroupValidation(False, msg, e)

        # for k, item in self._items_map().items():
        #     validation.add_item_validation(k, item.validation)
        super().validate_elements()

        return validation


    

alc = ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=-5)

print(alc)
print(alc.validation)
print(hash(alc))
#print(ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=-5) == ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=-5))