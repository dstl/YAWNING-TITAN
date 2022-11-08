from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict

import ruamel.yaml as ry

@dataclass()
class ConfigGroupABC(ABC):
    def to_dict(self,alias=True):
        if alias:
            return {self.__dataclass_fields__[key].metadata["alias"]:val for key,val in asdict(self).items()}
        return asdict(self)
            
    def as_commented_yaml(self):
        config_items = self.to_dict()
        s = ry.CommentedMap(config_items)
        for key in config_items.keys():
            s.yaml_set_comment_before_after_key(key,str(self.__dataclass_fields__[key].metadata["description"]),indent=2)
        return s

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