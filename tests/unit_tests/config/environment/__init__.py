from typing import Final
import os
from pathlib import Path
from typing import Final

from tests import TEST_CONFIG_PATH

TEST_GAME_RULES_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_game_rules_config.yaml")
)

TEST_OBSERVATION_SPACE_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_observation_space_config.yaml")
)

TEST_RESET_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_reset_config.yaml")
)

TEST_REWARDS_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_rewards_config.yaml")
)
