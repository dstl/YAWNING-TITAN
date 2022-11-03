import yaml
from yaml import SafeLoader
from typing import Dict,Any
from logging import getLogger

_LOGGER = getLogger(__name__)

class BaseConfig:
    def __init__(self,settings_dict,section_name):
        print("$$",section_name)
        if section_name in settings_dict:
            for key,val in settings_dict[section_name].items():
                setattr(self, key, val)

    # def __setattr__(self, name, value):
    #     if name != "config_created":
    #         #self.config_created = True
    #         print("%",name,value)
    #     super().__setattr__(name, value)

class Red(BaseConfig):
    def __init__(self,settings_dict={}):    
        super().__init__(settings_dict,"RED")

class Blue(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"BLUE")

class GameRules(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"GAME_RULES")

class ObservationSpace(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"OBSERVATION_SPACE")

class Reset(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"RESET")

class Rewards(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"REWARDS")

class Miscellaneous(BaseConfig):
    def __init__(self,settings_dict={}):
        super().__init__(settings_dict,"MISCELLANEOUS")

class Config:
    def __init__(self) -> None:
        #self.config_created = False    
        
        self.red = Red()
        self.blue = Blue()
        self.game_rules = GameRules()
        self.reset = Reset()
        self.miscellaneous = Miscellaneous()
        self.observation_space = ObservationSpace()
        self.rewards = Rewards()

    def read_config_file(self,settings_path):
        try:
            with open(settings_path) as f:
                settings_dict:Dict[str,Dict[str,Any]] = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        self.red = Red(settings_dict)
        self.blue = Blue(settings_dict)
        self.game_rules = GameRules(settings_dict)
        self.reset = Reset(settings_dict)
        self.miscellaneous = Miscellaneous(settings_dict)
        self.observation_space = ObservationSpace(settings_dict)
        self.rewards = Rewards(settings_dict)

    def write_to_file(self,settings_path):
        settings_dict = {key:val for key,val in self.__dict__.items() if key != "config_created"}
        _settings_dict = {}
        for section_name, section_class in settings_dict.items():
            _settings_dict[section_name.upper()] = section_class.__dict__
        
        with open(settings_path, 'w') as file:
            yaml.safe_dump(_settings_dict, file)

config = Config()
#config.read_config_file("D:/Pycharm projects/YAWNING-TITAN-DEV/YAWNING-TITAN/tests/test_configs/base_config.yaml")
#config.write_to_file("test.yaml")
#print(config.red.red_skill,config.rewards.reward_function)