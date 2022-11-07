from __future__ import annotations
from dataclasses import asdict, dataclass
from logging import getLogger

import yaml
from yaml import SafeLoader

from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.config.game_modes import default_game_mode_path

import ruamel.yaml as ry

_LOGGER = getLogger(__name__)


@dataclass()
class GameModeConfig:
    """
    Class that holds the configuration for YAWNING-TITAN
    """

    red_agent_config: RedAgentConfig
    """
    Red agent configuration object
    """

    blue_agent_config: BlueAgentConfig
    """
    Blue agent configuration object
    """

    observation_space_config: ObservationSpaceConfig
    """
    Observation space configuration object
    """

    game_rules_config: GameRulesConfig
    """
    Game rules configuration object
    """

    reset_config: ResetConfig
    """
    Reset configuration object
    """

    rewards_config: RewardsConfig
    """
    Rewards configuration object
    """

    output_timestep_data_to_json: bool
    """
    Is true if the timestep data is output to JSON
    """

    @classmethod
    def create(
            cls,
            config_path=None
    ) -> GameModeConfig:
        """
        Creates an instance of the GameModeConfig class
        """
        
        # if no config provided, use default game mode
        if not config_path:
            settings_path = default_game_mode_path()
        # otherwise, the settings path will be the path provided
        else:
            settings_path = config_path

        try:
            with open(settings_path) as f:
                settings = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        return GameModeConfig(
            red_agent_config=RedAgentConfig.create(settings["RED"]),
            blue_agent_config=BlueAgentConfig.create(settings["BLUE"]),
            observation_space_config=ObservationSpaceConfig.create(settings["OBSERVATION_SPACE"]),
            game_rules_config=GameRulesConfig.create(settings=settings["GAME_RULES"]),
            reset_config=ResetConfig.create(settings["RESET"]),
            rewards_config=RewardsConfig.create(settings["REWARDS"]),
            output_timestep_data_to_json=settings["MISCELLANEOUS"]["output_timestep_data_to_json"]
        )

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

c = GameModeConfig.create("D:/Pycharm projects/YAWNING-TITAN-DEV/YAWNING-TITAN/tests/test_configs/base_config.yaml")
# obs_compromised_status_config = {
#     "obs_compromised_status":False,
#     "obs_node_vuln_status":False,
#     "obs_node_connections"
# }
print(c.observation_space_config.obs_compromised_status)