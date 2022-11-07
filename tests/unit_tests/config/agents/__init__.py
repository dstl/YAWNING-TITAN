import os
from pathlib import Path
from typing import Final

from tests import TEST_CONFIG_PATH

TEST_BLUE_AGENT_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_blue_agent_config.yaml")
)

TEST_RED_AGENT_CONFIG_PATH: Final[Path] = Path(
    os.path.join(TEST_CONFIG_PATH, "config_sections", "complete_red_agent_config.yaml")
)
