from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass()
class ConfigABC(ABC):
    """
    :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>` class is an :py:class:`ABC <abc.ABC>`.

    The :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>`
    has two abstract class functions,
    :func:`create() <yawning_titan.config.game_config.config_abc.ConfigABC.create>` and
    :func:`validate() <yawning_titan.config.game_config.config_abc.ConfigABC.validate>`.

    The :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>` clas
    also has a :func:`to_dict() <yawning_titan.config.game_config.config_abc.ConfigABC.to_dict>`
    method with predefined logic.
    """

    def to_dict(self) -> Dict:
        """
        Serializes a :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>` as a :py:class:`dict`.

        As instances of :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>`
        are dataclasses, the default `__dict__` method is
        used to access the attributes. The private key name of each
        attribute has its underscore prefix removed before the key and value
        is added to a dict and returned.

        :returns: The :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>` as a :py:class:`dict`.
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
        Create abstract class method.

        An abstract class method that is to be implemented by subclasses of
        :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>`. The
        Implementations of the `.create` method should take a dict containing
        the config item keys and values required to instantiate the config
        class. The implementation of `.create` should pass the `config_dict`
        to `cls.validate` for the config data to be validated.
        """

    @classmethod
    @abstractmethod
    def validate(cls, config_dict: Dict[str, Any]):
        """
        Validate abstract class method.

        An abstract class method that is to be implemented by subclasses of
        :class:`ConfigABC <yawning_titan.config.game_config.config_abc.ConfigABC>`.
        Implementations of `.validate` method should take a dict containing the config item
        keys and values that are to be validated.
        The `validate` function is called from `cls.create`.
        """
        pass
