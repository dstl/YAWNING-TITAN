import yaml
from yaml import SafeLoader
from typing import Dict, Any
from logging import getLogger
from dataclasses import asdict
from yawning_titan.config import RedAgentConfig, BlueAgentConfig, GameRulesConfig, ObservationSpaceConfig, ResetConfig, RewardsConfig

_LOGGER = getLogger(__name__)


class Config:
    def __init__(self) -> None:
        self.config_created = False
        self.red = RedAgentConfig
        self.blue = BlueAgentConfig
        #self.game_rules = GameRulesConfig
        self.reset = ResetConfig
        # self.miscellaneous = Miscellaneous()
        self.observation_space = ObservationSpaceConfig
        self.rewards = RewardsConfig

    def create_from_file(self, settings_path):
        try:
            with open(settings_path) as f:
                settings_dict: Dict[str, Dict[str, Any]] = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {settings_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            _LOGGER.critical(msg, exc_info=True)
            raise e

        self.red = self.red.create(settings_dict["RED"])
        self.blue = self.blue.create(settings_dict["BLUE"])
        #self.game_rules = self.game_rules.create(settings_dict["GAME_RULES"])
        self.reset = self.reset.create(settings_dict["RESET"])
        # self.miscellaneous
        self.observation_space = self.observation_space.create(settings_dict["OBSERVATION_SPACE"])
        self.rewards = self.rewards.create(settings_dict["REWARDS"])

        self.config_created = True

    def write_to_file(self, settings_path):
        settings_dict = {key: val for key, val in self.__dict__.items() if key != "config_created"}
        _settings_dict = {}

        for section_name, section_class in settings_dict.items():
            _settings_dict[section_name.upper()] = asdict(section_class)

        with open(settings_path, 'w') as file:
            yaml.safe_dump(_settings_dict, file)

