from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, Any, List, Tuple

import ruamel.yaml as ry


@dataclass
class ConfigItem:
    value: Any
    description: str
    def __post_init__(self):
        self.__doc__ = 

def just_value_factory(data: List[Tuple[str, Any]]):
    return {
        field: value.value if isinstance(value, ConfigItem) else value
        for field, value in data
    }
@dataclass()
class ConfigGroupABC(ABC):
    def __setattr__(self, __name: str, __value: Any) -> None:
        print("£",__name,__value)
        if isinstance(__value,ConfigItem):
            print(1)
            super().__setattr__(__name,__value)
        else:
            print(2)
            try:
                self.__dict__[__name].value = __value
            except AttributeError:
                super().__setattr__(__name,__value)

    def __getattribute__(self, __name: str) -> Any:
        print("$",__name,super().__getattribute__(__name))
        return super().__getattribute__(__name).value

    def to_dict(self,fetch_descriptions=False):
        if fetch_descriptions:
            return asdict(self)
        return asdict(self,dict_factory=just_value_factory)

    def as_commented_yaml(self):
        config_items = self.to_dict()
        s = ry.CommentedMap(config_items)
        key:str
        val:ConfigItem
        for key,val in config_items.items():
            #print("k",self.__dict__[section_name.lower()].__dict__[key].__doc__)
            s.yaml_set_comment_before_after_key(key,val.description,indent=2)
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
