from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any
from collections import namedtuple

ConfigItem = namedtuple("value","description")
@dataclass()
class ConfigGroupABC(ABC):
    def __setattr__(self, __name: str, __value: Any) -> None:
        if hasattr(self,__name):
            attr:ConfigItem = getattr(self,__name)
            attr = attr._replace(value=__value)
            setattr(self,__name,attr)
        elif isinstance(__value,namedtuple):
            super().__setattr__(__name,attr)

    def __getattribute__(self, __name: str) -> Any:
        if hasattr(self,__name) and isinstance(getattr(self,__name),ConfigItem):
            return getattr(self,__name).value
        return super().__getattribute__(__name)

    @classmethod
    @abstractmethod
    def create(
            cls,
            **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def _validate(
            cls,
            **kwargs
    ):
        pass
