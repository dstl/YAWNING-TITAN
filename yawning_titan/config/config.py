import yaml
import inspect
from yaml import SafeLoader
from typing import Dict, Any, List
from logging import getLogger
from dataclasses import asdict,dataclass
from yawning_titan.config import RedAgentConfig, BlueAgentConfig, GameRulesConfig, ObservationSpaceConfig, ResetConfig, RewardsConfig, NetworkConfig
from yawning_titan.config.game_config.config_group_class import ConfigGroupABC


_LOGGER = getLogger(__name__)

@dataclass
class MiscellaneousConfig(ConfigGroupABC):
    """
    Class that validates and stores the Blue Agent Configuration
    """
    misc_json_out: bool

    @classmethod
    def create(cls,settings: Dict[str, Any]):
        miscellaneous_config = MiscellaneousConfig(
            misc_json_out=settings["output_timestep_data_to_json"]
        )
        return miscellaneous_config

    @classmethod
    def _validate(cls, data: dict):
        pass

class Config:
    def __init__(
        self,
        red=RedAgentConfig,
        blue=BlueAgentConfig,
        game_rules=GameRulesConfig,
        reset=ResetConfig,
        miscellaneous=MiscellaneousConfig,
        network_config=NetworkConfig,
        observation_space=ObservationSpaceConfig,
        rewards=RewardsConfig
    ) -> None:
       
        self.red = red
        self.blue = blue
        self.game_rules = game_rules
        self.reset = reset
        self.miscellaneous = miscellaneous
        self.network_config = network_config
        self.observation_space = observation_space
        self.rewards = rewards


        if all(inspect.isclass(c) for c in [red,blue,game_rules,reset,miscellaneous,network_config,observation_space,rewards]):
            self.config_created = True
        else:
            self.config_created = False
    
    def create_section(self,obj,settings_dict,section_name,*args, **kwargs):
        if inspect.isclass(obj):
            settings = settings_dict[section_name]
            print(f"created {section_name}")
            return obj.create(settings,*args, **kwargs)
        return obj

    def create_from_file(self, settings_path:str):
        try:
            with open(settings_path) as f:
                settings_dict: Dict[str, Dict[str, Any]] = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        self.network_config = self.create_section(self.network_config,settings_dict,"NETWORK")
        self.red = self.create_section(self.red,settings_dict,"RED")
        self.blue = self.create_section(self.blue,settings_dict,"BLUE")
        self.game_rules = self.create_section(self.game_rules,settings_dict,"GAME_RULES", number_of_nodes=len(self.network_config.matrix), high_value_targets=self.network_config.high_value_targets)
        self.reset = self.create_section(self.reset,settings_dict,"RESET")
        self.miscellaneous = self.create_section(self.miscellaneous,settings_dict,"MISCELLANEOUS")
        self.observation_space = self.create_section(self.observation_space,settings_dict,"OBSERVATION_SPACE")
        self.rewards = self.create_section(self.rewards,settings_dict,"REWARDS",)
        

        self.config_created = True

    def write_to_file(self, settings_path):
        settings_dict = {key: val for key, val in self.__dict__.items() if key != "config_created"}
        _settings_dict = {}

        for section_name, section_class in settings_dict.items():
            _settings_dict[section_name.upper()] = asdict(section_class)

        with open(settings_path, 'w') as file:
            yaml.safe_dump(_settings_dict, file)

