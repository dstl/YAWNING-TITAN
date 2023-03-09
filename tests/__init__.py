import os
from pathlib import Path
from typing import Final

TEST_PACKAGE_DATA_PATH: Final[Path] = Path(
    os.path.join(Path(__file__).parent.resolve(), "_package_data")
)
