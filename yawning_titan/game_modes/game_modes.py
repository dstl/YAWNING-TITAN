"""
The game_modes module.

The game_modes config class is responsible for creating, saving, deleting, and retrieving game modes, both default
and custom.
"""
import os
import pathlib
from pathlib import Path

from yawning_titan.game_modes import _GAME_MODES_ROOT_PATH


def default_game_mode_path() -> Path:
    """
    Return the path.

    Returns: The path to the default_game_mode.yaml as an instance of
        pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _GAME_MODES_ROOT_PATH,
            "_package_data",
            "default_game_mode.yaml",
        )
    )


def default_new_game_mode_path() -> Path:
    """
    Return the path.

    Returns: The path to the default_new_game_mode.yaml as an instance of
        pathlib.Path.
    """
    return pathlib.Path(
        os.path.join(
            _GAME_MODES_ROOT_PATH,
            "_package_data",
            "default_new_game_mode.yaml",
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
            _GAME_MODES_ROOT_PATH,
            "_package_data",
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
            _GAME_MODES_ROOT_PATH,
            "_package_data",
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
            _GAME_MODES_ROOT_PATH,
            "_package_data",
            "multiple_high_value_targets.yaml",
        )
    )
