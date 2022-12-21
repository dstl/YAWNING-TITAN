
class ConfigGroupValidation(ConfigGroupCore):
    """
    Used to return a validation result for a group of dependant config items, and the list of item validations.

    If validation fails, a reason why and any exception raised are returned.
    """

    def __init__(
        self,
        passed: bool = True,
        fail_reason: Optional[str] = None,
        fail_exception: Optional[ConfigGroupValidationError] = None,
    ):
        self.passed: bool = passed
        self.fail_reason: str = fail_reason
        self.fail_exception: ConfigGroupValidationError = fail_exception
        self._element_validation = {}

    def add_element_validation(self, element_name: str, validation: Union[ConfigItemValidation,ConfigGroupValidation]):
        """
        Add a :class:`ConfigItemValidation` or :class:`ConfigGroupValidation` to the item validation dict.

        :param element_name: The name of the element.
        :param validation: the instance of ConfigItemValidation.
        """
        self._element_validation[element_name] = validation

    def to_dict(self,element_name:str="root")->dict:
        """
        Express the error tree as a dictionary.

        :param element_name: A string name for the element to be represented.

        :return: A dict of element names to validation errors or validation dictionaries.
        """ 
        if self.passed:
            d = {}
        else:
            d = {"group": self.fail_reason}  
        for e,validation in self.element_validation.items():
            if isinstance(validation,ConfigGroupValidation) and (not validation.group_passed or not validation.passed):
                d[e] = validation.to_dict(e)
            elif not validation.passed:
                d[e] = validation.fail_reason
        return d

    def log(self, element_name:str="root") -> None:
        """
        Return the validation results as a formatted string.

        :param element_name: A string name for the element to be represented.
        """
        string = (
            "\nValidation results\n"
            "------------------\n"
        )
        d = self.to_dict(element_name)
        if d:
            string += yaml.dump(d,sort_keys=False)
        else:
            string += d.get(element_name,"Passed")
        print(string)


    @property
    def element_validation(self) -> Dict[str, ConfigItemValidation]:
        """
        The dict of element to :class:`ConfigItemValidation` and :class:`ConfigGroupValidation` validations.

        :return: A dict.
        """
        return self._element_validation

    @property
    def group_passed(self) -> bool:
        """
        Returns True if all items passed validation, otherwise returns False.

        :return: A bool.
        """
        return all(v.passed for v in self.element_validation.values())

    # def __repr__(self) -> str:
    #     return (
    #         f"ConfigGroupValidation("
    #         f"passed={self.passed}, "
    #         f"fail_reason='{self.fail_reason}', "
    #         f"fail_exception={self.fail_exception}, "
    #         f"item_validation={self._item_validation}, "
    #         f"group_passed={self.group_passed}"
    #         f")"
    #     )

    # def __hash__(self) -> int:
    #     return hash(
    #         (
    #             self.passed,
    #             self.fail_reason,
    #             self.fail_exception,
    #             tuple(self._item_validation),
    #         )
    #     )

    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, ConfigGroupValidation):
    #         return hash(self) == hash(other)
    #    return False


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
        msg = None
        try:
            if self.use.value is True:
                print("f",self.chance.value,self.likelihood.value)
                if self.likelihood.value is None:
                    msg = "Likelihood cannot be null when use=True"
                    print("E1",msg)
                    raise ConfigGroupValidationError(msg)
                if self.chance.value is None:
                    msg = "chance cannot be null when use=True"
                    print("E2",msg)
                    raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            print("ERROR: ",e)
            self.validation = ConfigGroupValidation(False, msg, e)   

        ConfigGroup.validate(self)
        return self.validation
