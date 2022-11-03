from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


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