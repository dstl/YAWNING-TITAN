from pathlib import Path
from typing import Final

_LIB_CONFIG_ROOT_PATH: Final[Path] = Path(__file__).parent.resolve()
"""
The path to the library config root directory as an instance of pathlib.Path.
"""

from .agents import BlueAgentConfig,RedAgentConfig
from .environment import GameRulesConfig,ObservationSpaceConfig,ResetConfig,RewardsConfig
from .config import Config
#from .game_config import 