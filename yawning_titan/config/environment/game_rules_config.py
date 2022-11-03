from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC


<<<<<<< HEAD
@dataclass
=======
@dataclass()
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
class GameRulesConfig(ConfigGroupABC):
    """
    Class that validates and stores Game Rules Configuration
    """

    @classmethod
    def create(cls, settings: Dict[str, Any]):
        pass

    @classmethod
    def _validate(cls, data: dict):
<<<<<<< HEAD
        pass
=======
        pass
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
