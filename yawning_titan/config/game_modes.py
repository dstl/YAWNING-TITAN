"""
The game_modes module.

The game_modes config class is responsible for creating, saving, deleting, and retrieving game modes, both default
and custom.
"""
import os
import pathlib
from pathlib import Path

from yawning_titan.config import _LIB_CONFIG_ROOT_PATH


def default_game_mode_path() -> Path:
    """
    Return the path.

    Returns: The path to the default_game_mode.yaml as an instance of
        pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _LIB_CONFIG_ROOT_PATH,
            "_package_data",
            "game_modes",
            "default_game_mode.yaml",
        )
    )


def low_skill_red_with_random_infection_perfect_detection_path() -> Path:
    """
    Return the path.

    Returns: The path to the
        low_skill_red_with_random_infection_perfect_detection.yaml as an instance
        of pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _LIB_CONFIG_ROOT_PATH,
            "_package_data",
            "game_modes",
            "low_skill_red_with_random_infection_perfect_detection.yaml",
        )
    )


def dcbo_game_mode_path() -> Path:
    """
    Return the path.

    Returns: The path to the dcbo_config.yaml as an instance of pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _LIB_CONFIG_ROOT_PATH,
            "_package_data",
            "game_modes",
            "dcbo_config.yaml",
        )
    )


def multiple_high_value_targets_game_mode_path() -> Path:
    """
    Return the path.

    Returns: The path to the multiple_high_value_targets.yaml as an instance
        of pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _LIB_CONFIG_ROOT_PATH,
            "_package_data",
            "game_modes",
            "multiple_high_value_targets.yaml",
        )
    )
