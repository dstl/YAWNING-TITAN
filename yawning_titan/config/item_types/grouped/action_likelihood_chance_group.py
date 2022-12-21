from typing import Dict, Optional, Union

from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.core import ConfigGroupValidation, ConfigGroup
from yawning_titan.config.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.exceptions import ConfigGroupValidationError

class ActionLikelihoodGroup(ConfigGroup):
    """The ConfigGroup to represent an action, likelihood common config group."""
    def __init__(
        self,
        doc: Optional[str] = None,
        use: bool = False,
        likelihood: Optional[float] = None,        
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param use: Whether to use the action or not.
        :param likelihood: The likelihood of the action.
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
            properties=FloatProperties(allow_null=True, min_val=0, max_val=1, inclusive_min=True, inclusive_max=True),
        )        
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """
        Validate the ActionLikelihoodChance group.

        This is done at two levels:
            1. A group level validation is performed that checks if likelihood
            and chance are provided when use is True.
            2. An item level validation is performed by calling .validate on
            the use and likelihood config items.

        :return: An instance of ConfigGroupValidation.
        """
        #print("VALIDATE IN AL")        
        msg = None
        try:
            if self.use.value is True:
                if self.likelihood.value is None:
                    msg = "Likelihood cannot be null when use=True"
                    raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation = ConfigGroupValidation(False, msg, e)        
        
        ConfigGroup.validate(self)
        return self.validation
class ActionLikelihoodChanceGroup(ActionLikelihoodGroup):
    """The ConfigGroup to represent an action, likelihood, and chance common config group."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: bool = False,
        likelihood: Optional[float] = None,
        chance: Optional[float] = None,        
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param use: Whether to use the action or not.
        :param likelihood: The likelihood of the action.
        :param chance: The chance of the action.
        :param doc: An optional descriptor.
        """
        self.chance: FloatItem = FloatItem(
            value=chance,
            doc="The chance of the action.",
            properties=FloatProperties(allow_null=True, min_val=0, max_val=1, inclusive_min=True, inclusive_max=True),
        )
        super().__init__(doc,use,likelihood)

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
        #print("VALIDATE IN ALC")
        ConfigGroup.validate(self)
        def check_likelihood(element:ActionLikelihoodChanceGroup):
            if element.likelihood.value is None:
                msg = "Likelihood cannot be null when use=True"
                print("E1",msg)
                return msg
            return None

        def check_chance(element:ActionLikelihoodChanceGroup):
            if element.chance.value is None:
                msg = "chance cannot be null when use=True"
                print("E2",msg)
                return msg
            return None

        if self.use.value is True:
            self.validation.check(check_likelihood,self)
            self.validation.check(check_chance,self)

        
        return self.validation




    

#alc = ActionLikelihoodChanceGroup(use=True, likelihood=0.5, chance=-5)
alc = ActionLikelihoodChanceGroup(use=True)
# print(alc,"\n")
# print("VALIDATION STR:",alc.validation,"\n")
# print("HASH:",hash(alc),"\n")
# print("DICT:",alc.to_dict(),"\n")
# print("LOG:",alc.validation.to_dict(),"\n")
alc.validation.log()
