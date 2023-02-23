import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from yawning_titan import GAME_MODES_DIR
from yawning_titan.game_modes import _GAME_MODES_ROOT_PATH
from yawning_titan_gui.helpers import GameModeManager


class TestGameModeManager:
    """Test the methods of the :class: `~yawning_titan_gui.helpers.GameModeManager`."""

    def setup_class(self):
        """Initialise the objects required for the test suite."""
        self.temp_dir = tempfile.TemporaryDirectory()
        GameModeManager.root_dir = Path(self.temp_dir.name)
        shutil.copytree(
            os.path.join(_GAME_MODES_ROOT_PATH, "_package_data"),
            self.temp_dir.name,
            dirs_exist_ok=True,
        )

    def teardown_class(self):
        """Reset the objects used in the test suite."""
        GameModeManager.root_dir = GAME_MODES_DIR
        GameModeManager.game_modes = {}

    def test_get_game_mode_path_exists(self):
        """Tests that the correct path is return from :method: `~yawning_titan_gui.helpers.GameModeManager.get_game_mode_path`."""
        path = GameModeManager.get_game_mode_path("default_new_game_mode.yaml")
        assert path == Path(self.temp_dir.name) / "default_new_game_mode.yaml"

    def test_get_game_mode_invalid_path(self):
        """Tests that the correct error is raised when :method: `~yawning_titan_gui.helpers.GameModeManager.get_game_mode_path` is called with a non existent path."""
        with pytest.raises(FileNotFoundError):
            path = GameModeManager.get_game_mode_path("test.yaml")  # noqa: F841

    def test_load_game_modes_valid_only(self):
        """Test only non erroneous game modes are loaded when `valid_only` in :method: `~yawning_titan_gui.helpers.GameModeManager.load_game_modes` is set to True."""

        def check_game_mode_fail(*args, **kwargs):
            return False

        GameModeManager.game_modes = {}
        with mock.patch.object(
            GameModeManager, "check_game_mode", new=check_game_mode_fail
        ):
            GameModeManager.load_game_modes(valid_only=True)
            assert GameModeManager.game_modes == {}

    def test_load_game_modes_info_only(self):
        """Test no game mode objects are loaded when `info_only` in :method: `~yawning_titan_gui.helpers.GameModeManager.load_game_modes` is set to True."""
        GameModeManager.game_modes = {}
        GameModeManager.load_game_modes(info_only=True)
        assert all(
            game_mode["config_class"] is None
            for game_mode in GameModeManager.game_modes.values()
        )
