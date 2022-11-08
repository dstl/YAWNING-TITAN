import os
from pathlib import Path
from typing import Final

TEST_CONFIG_PATH: Final[Path] = Path(
    os.path.join(Path(__file__).parent.resolve(), "test_configs")
)

TEST_BASE_CONFIG_PATH = Path(
    os.path.join(Path(__file__).parent.resolve(), "test_configs", "base_config.yaml")
)
