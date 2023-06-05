import os
from logging import getLogger
from pathlib import Path

import yawning_titan  # noqa - To use the Yawning-Titan logging config

_LOGGER = getLogger(__name__)


def _clean_up_pre_v2_0_0():
    """
    Performs the clean-up for Yawning-Titan installations before v2.0.0.

    Files that are deleted:

    - ~/yawning_titan/notebooks/Create a Network.ipynb
    - ~/yawning_titan/notebooks/Creating and playing as a Keyboard Agent.ipynb
    - ~/yawning_titan/notebooks/Using the Network DB.ipynb
    - ~/yawning_titan/notebooks/Using YawningTitanRun.ipynb
    - ~/yawning_titan/notebooks/sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb
    - ~/yawning_titan/notebooks/sb3/Using an Evaluation Callback to monitor progress during training.ipynb

    Directories that are deleted are:

    - ~/yawning_titan/notebooks/sb3/
    """
    # Delete old default notebooks
    old_notebooks = [
        "Create a Network.ipynb",
        "Creating and playing as a Keyboard Agent.ipynb",
        "Using the Network DB.ipynb",
        "Using YawningTitanRun.ipynb",
        "sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb",
        "sb3/Using an Evaluation Callback to monitor progress during training.ipynb",
    ]

    user_notebooks_dir = Path.home() / "yawning_titan" / "notebooks"

    for nb_file in old_notebooks:
        nb_path = user_notebooks_dir / nb_file
        if nb_path.is_file():
            os.remove(nb_path)
            _LOGGER.info(f"Deleted default notebook: {nb_path}")

    sb3_dir = user_notebooks_dir / "sb3"
    if sb3_dir.is_dir():
        if not os.listdir(sb3_dir):
            sb3_dir.rmdir()
            _LOGGER.info(f"Deleted default notebook directory: {sb3_dir}")


def run():
    """Perform the full clean-up."""
    _clean_up_pre_v2_0_0()


if __name__ == "__main__":
    run()
