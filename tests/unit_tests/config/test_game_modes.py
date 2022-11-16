import os

import pytest

from yawning_titan.config.game_modes import (
    default_game_mode_path,
    low_skill_red_with_random_infection_perfect_detection_path,
)


@pytest.mark.unit_test
def test_default_game_mode_path():
    """
    Tests that returned pile path exists.

    This tests that the dynamic generation of the path to the default_game_mode.yaml file returns a Path to the file
    that exists.
    """
    assert os.path.isfile(default_game_mode_path())


@pytest.mark.unit_test
def test_low_skill_red_with_random_infection_perfect_detection_path():
    """
    Tests that a file at the filepath returned exists.

    Tests that the dynamic generation of the path to the
    low_skill_red_with_random_infection_perfect_detection.yaml file returns a
    Path to the file that exists.
    """
    assert os.path.isfile(low_skill_red_with_random_infection_perfect_detection_path())
