from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict

import ruamel.yaml as ry

@dataclass()
class ConfigGroupABC(ABC):
    def to_dict(self):
        return asdict(self)
            
    def as_commented_yaml(self):
        config_items = self.to_dict()
        s = ry.CommentedMap(config_items)
        for key in config_items.keys():
            s.yaml_set_comment_before_after_key(key,str(self.__dataclass_fields__[key].metadata),indent=2)
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


@dataclass()
class MiscellaneousConfig(ConfigGroupABC):
    """
    Class that validates and stores Rewards Configuration
    """

    output_timestep_data_to_json: bool = field(metadata="Is true if the timestep data is output to JSON")
    """Is true if the timestep data is output to JSON"""

    @classmethod
    def create(
            cls,
            settings: Dict[str, Any]
    ) -> MiscellaneousConfig:
        cls._validate(settings)

        misc = MiscellaneousConfig(output_timestep_data_to_json=settings["output_timestep_data_to_json"])        

        return misc

    @classmethod
    def _validate(cls, data: dict):
        pass