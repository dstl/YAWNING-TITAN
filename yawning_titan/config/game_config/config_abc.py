from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass()
class ConfigABC(ABC):
    """
    The `ConfigABC` class is an abstract base class Yawning-Titan config
    classes inherit from. `ConfigABC` has two abstract class methods,
    `.create` and `._validate`. `ConfigABC` also has a `to_dict()` function
    with predefined logic.
    """

    def to_dict(self) -> Dict:
        """
        Serializes a subclass of ConfigABC as a dict. As instances of
        ConfigABC are dataclasses, the default `__dict__` method is
        used to access the attributes. The private key name of each
        attribute has its underscore prefix removed before the key and value
        is added to a dict and returned.

        Returns:
            The subclass of ConfigABC as a dict.
        """
        d = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                k = k[1:]
            d[k] = v
        return d

    @classmethod
    @abstractmethod
    def create(cls, config_dict: Dict[str, Any]):
        """
        An abstract class method that is to be implemented by subclasses of
        `ConfigGroupClass`. The `.create` method should take a dict
        containing the config item keys and values required to instantiate
        the config class. The implementation of `.create` should pass the
        `config_dict` to `cls._validate` for the config data to be validated.
        """

    @classmethod
    @abstractmethod
    def _validate(cls, config_dict: Dict[str, Any]):
        """
        An abstract class method that is to be implemented by subclasses of
        `ConfigGroupClass`. The `._validate` method should take a dict
        containing the config item keys and values that are to be validated.
        The `_validate` function is called from `cls.create`.
        """
        pass
