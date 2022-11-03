from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


<<<<<<< HEAD
@dataclass
=======
@dataclass()
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
class ConfigGroupABC(ABC):

    @classmethod
    @abstractmethod
<<<<<<< HEAD
    def create(cls, settings: Dict[str, Any]):
=======
    def create(
            cls,
            settings: Dict[str, Any]
    ):
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
        pass

    @classmethod
    @abstractmethod
<<<<<<< HEAD
    def _validate(cls,data: dict):
        pass
=======
    def _validate(
            cls,
            data: dict
    ):
        pass
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
