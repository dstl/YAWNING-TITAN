import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest
from django.test import Client
from django.urls import reverse

from dist.manage.django.http.response import Http404
from yawning_titan import GAME_MODES_DIR
from yawning_titan.config import _LIB_CONFIG_ROOT_PATH
from yawning_titan_gui.forms import GameModeFormManager
from yawning_titan_gui.helpers import GameModeManager


class TestGameModeConfigView:
    """Test processes executed through requests to the 'game mode config' and 'update config' endpoints."""

    def setup_class(self):
        """Initialise the objects required for the test suite."""
        self.temp_dir = tempfile.TemporaryDirectory()
        GameModeManager.root_dir = Path(self.temp_dir.name)
        shutil.copytree(
            os.path.join(_LIB_CONFIG_ROOT_PATH, "_package_data", "game_modes"),
            self.temp_dir.name,
            dirs_exist_ok=True,
        )
        GameModeManager.load_game_modes()
        self.url = reverse(
            "game mode config",
            kwargs={
                "game_mode_filename": "default_new_game_mode.yaml",
                "section_name": "red",
            },
        )
        self.update_url = reverse("update config")

    def teardown_class(self):
        """Reset the objects used in the test suite."""
        GameModeManager.root_dir = GAME_MODES_DIR
        GameModeManager.game_modes = {}
        GameModeFormManager.game_modes = {}
        self.temp_dir.cleanup()

    def test_get_with_no_args(self, client: Client):
        """Test that a game mode config cannot be retrieved without a game_mode_filename."""
        with pytest.raises(
            Http404, match="Can't find game mode section None in game mode None"
        ):
            url = reverse("game mode config")
            response = client.get(url)  # noqa: F841

    def test_get(self, client: Client):
        """Test that a valid game mode config url responds successfully to a get request."""
        response = client.get(self.url)
        assert response.status_code == 200
        assert "game_mode_config.html" in (t.name for t in response.templates)
        assert "default_new_game_mode.yaml" in GameModeFormManager.game_modes

    def test_finish(self, client: Client):
        """Test that when the last game mode section is updated the return is a redirect to the game mode manager."""
        url = reverse(
            "game mode config",
            kwargs={
                "game_mode_filename": "default_new_game_mode.yaml",
                "section_name": "miscellaneous",
            },
        )
        game_mode_path = GameModeManager.root_dir / "default_new_game_mode.yaml"
        game_mode_path.unlink()
        response = client.post(url)

        assert response.status_code == 302
        assert response["location"] == reverse("Manage game modes")
        assert os.path.exists(game_mode_path)
        # TODO add check that game mode saved

    def test_next_section(self, client: Client):
        """Test the next section is correctly chosen when a valid config is posted to the endpoint."""
        response = client.post(self.url)
        assert response.status_code == 302
        assert response["location"].split("/")[-2] == "blue"

    def test_save(self, client: Client):
        """Test that a save operation results in a file being created in the correct location."""
        game_mode_path = GameModeManager.root_dir / "default_new_game_mode.yaml"
        game_mode_path.unlink()
        response = client.post(
            self.update_url,
            {
                "_game_mode_filename": "default_new_game_mode.yaml",
                "_section_name": "red",
                "_form_id": 3,
                "_operation": "save",
            },
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"message": "saved"}).encode("utf-8")
        assert os.path.exists(game_mode_path)

    def test_update_fail(self, client: Client):
        """Test that when a config is updates and becomes invalid that an appropriate error message is returned."""
        response = client.post(
            self.update_url,
            {
                "_game_mode_filename": "default_new_game_mode.yaml",
                "_section_name": "red",
                "_form_id": 3,
                "_operation": "update",
                "only_main_red_node": True,
                "any_red_node": True,
            },
        )
        assert response.status_code == 400
        assert response.content == json.dumps(
            {
                "errors": '{"3": {"group": ["The red agent cannot attack from multiple sources simultaneously."], "items": {"only_main_red_node": [], "any_red_node": []}}}'
            }
        ).encode("utf-8")
        assert (
            "The red agent cannot attack from multiple sources simultaneously."
            in GameModeFormManager.game_modes["default_new_game_mode.yaml"]["red"]
            .forms[3]
            .config_class.validation.fail_reasons
        )
