import yaml
import inspect
import ruamel.yaml as ry

from yaml import SafeLoader
from typing import Dict, Any, List
from logging import getLogger
from dataclasses import asdict,dataclass
from yawning_titan.config.agents import BlueAgentConfig,RedAgentConfig
from yawning_titan.config.environment import ObservationSpaceConfig, ResetConfig, RewardsConfig, NetworkConfig, GameRulesConfig
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.config import ConfigGroupABC

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
    """
    Class that holds the configuration for YAWNING-TITAN
    """

    red: RedAgentConfig
    """
    Red agent configuration object
    """

    blue: BlueAgentConfig
    """
    Blue agent configuration object
    """

    observation_spaceg: ObservationSpaceConfig
    """
    Observation space configuration object
    """

    game_rules: GameRulesConfig
    """
    Game rules configuration object
    """

    reset: ResetConfig
    """
    Reset configuration object
    """

    miscellaneous: MiscellaneousConfig
    """
    Miscellaneous configuration object
    """

    network_config: NetworkConfig
    """
    Network configuration object
    """

    rewards: RewardsConfig
    """
    Rewards configuration object
    """

    def __init__(
        self,
        red=RedAgentConfig,
        blue=BlueAgentConfig,
        game_rules=GameRulesConfig,
        reset=ResetConfig,
        miscellaneous=MiscellaneousConfig,
        network=NetworkConfig,
        observation_space=ObservationSpaceConfig,
        rewards=RewardsConfig
    ) -> None:
       
        self.red:RedAgentConfig = red
        self.blue:BlueAgentConfig = blue
        self.game_rules:GameRulesConfig = game_rules
        self.reset:ResetConfig = reset
        self.miscellaneous:MiscellaneousConfig = miscellaneous
        self.network:NetworkConfig = network_config
        self.observation_space:ObservationSpaceConfig = observation_space
        self.rewards:RewardsConfig = rewards

        if all(inspect.isclass(c) for c in self.__dict__.values()):
            self.config_created = True
        else:
            self.config_created = False
    
    def create_section(self,obj,settings_dict,section_name,*args, **kwargs):
        if inspect.isclass(obj):
            settings = settings_dict[section_name]
            print(f"created {section_name}")
            return obj.create(settings,*args, **kwargs)
        return obj

    def create_from_file(self, settings_path:str)->None:
        """
        Create a config class from a YAML file
        """
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

    def as_formatted_dict(self):
        settings_dict = {key: val for key, val in self.__dict__.items() if isinstance(val,ConfigGroupABC)}
        _settings_dict = {}

        for section_name, section_class in settings_dict.items():
            section_dict = {key:val for key,val in asdict(section_class).items() if type(val) in [int,str,list,bool]}
            _settings_dict[section_name.upper()] = section_dict
        return _settings_dict

    def write_to_file(self, settings_path):
        self.file_path = settings_path
        with open(settings_path, 'w') as file:
            yaml.safe_dump(self.as_formatted_dict(), file)

    def write_to_file_with_comments(self,file_path):
        
        
        settings_dict = self.as_formatted_dict()
        data = ry.round_trip_load(ry.round_trip_dump(settings_dict))
        MAPIND = 4

        _yaml = ry.YAML()
        _yaml.indent(mapping=2)

        with open(file_path,"w") as f:
            #data = _yaml.load(f)
            print("DOC",data)

            for section_name, section_config in settings_dict.items():
                data[section_name].yaml_set_start_comment('after test2', indent=2)
                s = ry.CommentedMap(section_config)
                for key,val in section_config.items():
                    #print("k",self.__dict__[section_name.lower()].__dict__[key].__doc__)
                    s.yaml_set_comment_before_after_key(key,"test comment",indent=2)
                data[section_name] = s
                    
            print(data)
            _yaml.dump(data,f)



node_positions,matrix = network_creator.create_18_node_network()
network_config = NetworkConfig.create(
    {
        "high_value_targets": ["9"],
        "entry_nodes": ["0", "1", "2"],
        "vulnerabilities":None,
        "positions": node_positions,
        "matrix": matrix
    }
)

print("="*150)
print(NetworkConfig.high_value_targets.__doc__)
for key,val in network_config.__dict__.items():
    print("k",key,val,val.__doc__)
# conf = Config(network_config=network_config)
# conf.create_from_file(r"D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\tests\test_configs\base_config.yaml")
# print(conf.red.red_always_succeeds)
# #conf.write_to_file("test.yaml")
# conf.write_to_file_with_comments("test.yaml")