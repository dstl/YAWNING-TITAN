from typing import Dict

from tests.config_test_utils import read_yaml_file
from yawning_titan.config.game_modes import default_new_game_mode_path


def get_default_config_dict() -> Dict:
    """Return the default game mode config."""
    return read_yaml_file(default_new_game_mode_path())
