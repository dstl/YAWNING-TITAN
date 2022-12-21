from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union, Callable
from collections.abc import Iterable
import yaml
from yawning_titan.exceptions import ConfigGroupValidationError, ConfigItemValidationError


@dataclass()
class ConfigItemValidation:
    """
    :class:`ConfigItemValidation` is used to return a validation result.

    If validation fails, a reason why and any exception raised are returned.
    """
    passed: Optional[bool] = True
    """``True`` if the _value has passed validation, otherwise ``False``."""
    fail_reason: Optional[str] = None
    """The reason why validation failed."""
    fail_exception: Optional[Exception] = None
    """The :py::class:`Exception` raised when validation failed."""


class ConfigGroupCore:
    """
    Used to provide helper methods to represent a ConfigGroup object.
    """
    def get_config_elements(self)->Dict[str,Union[ConfigItem,ConfigGroup]]:
        return {k:v for k,v in self.__dict__.items() if isinstance(v,ConfigItem) or isinstance(v,ConfigGroup)}

    def get_non_config_elements(self)->Dict[str,Any]:
        return {k:v for k,v in self.__dict__.items() if k not in self.get_config_elements()}

    def stringify(self):
        string = f"{self.__class__.__name__}("
        strings = [f"{name}={val.stringify()}" for name,val in self.get_config_elements().items()]
        strings.extend([f"{name}={val}" for name,val in self.get_non_config_elements().items()])
        return string + ", ".join(strings)


    def __repr__(self) -> str:
        return self.stringify()

    def __str__(self) -> str:
        return self.stringify()

    def __hash__(self) -> int:
        element_hash = [v.stringify() for v in self.get_config_elements().values()]
        element_hash.extend([tuple(v) if isinstance(v,Iterable) else v for v in self.get_non_config_elements().values()])
        return hash(tuple(element_hash))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

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
        self.fail_reasons: List[str] = [fail_reason] if fail_reason is not None else []
        self.fail_exceptions:  List[ConfigGroupValidationError] = [fail_exception] if fail_exception is not None else []
        self._element_validation = {}

    def add_element_validation(self, element_name: str, validation: Union[ConfigItemValidation,ConfigGroupValidation]):
        """
        Add a :class:`ConfigItemValidation` or :class:`ConfigGroupValidation` to the item validation dict.

        :param element_name: The name of the element.
        :param validation: the instance of ConfigItemValidation.
        """
        self._element_validation[element_name] = validation

    def add_validation(self, fail_reason:str, exception:ConfigGroupValidationError):
        self.passed = False
        self.fail_reasons.append(fail_reason)
        self.fail_exceptions.append(exception)

    def check(self,method:Callable,element:Union[ConfigItem,ConfigGroup]):
        try:
            msg = method(element)
            if msg is not None:
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            print("ERROR: ",e)
            self.add_validation(msg,e)

    def to_dict(self,element_name:str="root")->dict:
        """
        Express the error tree as a dictionary.

        :param element_name: A string name for the element to be represented.

        :return: A dict of element names to validation errors or validation dictionaries.
        """ 
        if self.passed:
            d = {}
        else:
            d = {"group": self.fail_exceptions}  
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


@dataclass()
class ItemTypeProperties(ABC):
    """An Abstract Base Class that is inherited by config data type properties."""

    allow_null: Optional[bool] = None
    """`True` if the config _value can be left empty, otherwise `False`."""
    default: Optional[Any] = None
    """The items default value."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        An abstract method that returns the properties as a dict.

        :return: A dict.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @abstractmethod
    def validate(self, val) -> ConfigItemValidation:
        """An abstract group validation."""
        pass

@dataclass()
class ConfigItem:
    """The ConfigItem class holds an items value, doc, and properties."""

    value: object
    """The items value."""
    doc: Optional[str] = None
    """The items doc."""
    properties: Optional[ItemTypeProperties] = None
    """The items properties."""
    validation: ConfigItemValidation = None
    """The instance of ConfigItemValidation that provides access to the item validation details."""

    def __post_init__(self):
        if self.value is None and self.properties.default:
            self.value = self.properties.default
        self.validation = self.properties.validate(self.value)

    def to_dict(self, as_key_val_pair: bool = False):
        """
        Return the ConfigItem as a dict.

        :param as_key_val_pair: If true, the dict is returned as a value in
            a key/value pair, the key being the class name.
        :return: The ConfigItem as a dict.
        """
        d = {"value": self.value}
        if self.doc:
            d["doc"] = self.doc
        if self.properties:
            d["properties"] = self.properties.to_dict()
        if as_key_val_pair:
            return {self.__class__.__name__: d}
        return d

    def validate(self) -> ConfigItemValidation:
        """
        Validate the item against its properties.

        If no properties exist,
        simply return a default passed :class:`ConfigItemValidation`.

        :return: An instance of :class:`ConfigItemValidation`.
        """
        #print("VALIDATING ITEM")
        if self.properties:
            return self.properties.validate(self.value)
        return ConfigItemValidation()

    def set_value(self, value:Any) -> None:
        """
        Set the value of the :class:`ConfigItem` after construction.

        :param value: The value to be set.
        """
        self.value = value
        #self.validate()

    def stringify(self):
        return self.value


class ConfigGroup(ConfigGroupCore, ABC):
    """The ConfigGroup class holds a ConfigItem's, doc, properties, and a ConfigItemValidation."""

    def __init__(self, doc: Optional[str] = None):
        """The ConfigGroup constructor.

        :param doc: The groups doc.
        """
        self.doc: Optional[str] = doc        
        self.validation = self.validate()

    #@abstractmethod
    def validate(self) -> ConfigGroupValidation:
        """
        Validate the grouped items against their properties.

        :return: An instance of :class:`ConfigGroupValidation`.
        """
        #print("VALIDATE IN BASE CONFIG GROUP")
        if not hasattr(self, "validation"):
            print("SETTING VALIDATION ATTR")
            self.validation = ConfigGroupValidation()
        self.validate_elements()
        return self.validation

    #@abstractmethod
    def to_dict(self): # TODO: replace with generic method
        """
        Return the ConfigGroup as a dict.

        :return: The ConfigGroup as a dict.
        """
        attr_dict = {"doc": self.doc} if self.doc is not None else {}
        element_dict = {k:e.to_dict() for k,e in self.get_config_elements().items()}
        return {**attr_dict,**element_dict}     
   
    def validate_elements(self):
        """
        Call the .validate() method on each of the elements in the group.
        """
        for k, element in self.get_config_elements().items():
            self.validation.add_element_validation(k, element.validate())

    def set_from_dict(self,config_dict:dict,validate:bool=True):
        """

        :param config_dict: _description_
        :type config_dict: dict
        """
       # print("-----------------\nSETTING FROM DICT\n-----------------")
        for element_name,v in config_dict.items():
            #print(f"===========\n{element_name}\n===========")
            element = getattr(self,element_name,None)
            if type(v) == dict and isinstance(element,ConfigGroup):
                element.set_from_dict(v,False)
            elif type(v) != dict and isinstance(element, ConfigItem):
                element.set_value(v)
        if validate:
            self.validate()
