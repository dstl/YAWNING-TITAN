from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

def set_prop(x, doc):
    def _get(self):
        return getattr(self, '_' + x)

    def _set(self, val):
        setattr(self, '_' + x, val)

    def _del(self):
        delattr(self, '_' + x)

    return property(_get, _set, _del, doc)

@dataclass
class ConfigGroupABC(ABC):

    @classmethod
    @abstractmethod
    def create(cls, settings: Dict[str, Any]):
        pass

    @classmethod
    @abstractmethod
    def _validate(cls,data: dict):
        pass