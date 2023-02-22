import json
import os
import shutil
import tempfile
from pathlib import Path

from django.http.response import HttpResponse
from django.test import Client
from django.urls import reverse

from yawning_titan import GAME_MODES_DIR
from yawning_titan.game_modes import _GAME_MODES_ROOT_PATH
from yawning_titan_gui.helpers import GameModeManager


def test_game_modes_view_get(client: Client):
    """Test that the Manage game modes view can accept GET requests."""
    url = reverse("Manage game modes")
    response = client.get(url)
    assert response.status_code == 200


def test_game_modes_view_post(client: Client):
    """Test that the Manage game modes view cannot accept POST requests.

    Status 405 represents not allowed request method.
    """
    url = reverse("Manage game modes")
    response = client.post(url)
    assert response.status_code == 405


class TestGameModeManagerView:
    """Test processes executed through requests to the 'Manage game modes' and 'file manager' endpoints."""

    def setup_class(self):
        """Setup a test :class: `~yawning_titan_gui.helpers.GameModeManager`."""
        self.temp_dir = tempfile.TemporaryDirectory()
        GameModeManager.root_dir = Path(self.temp_dir.name)
        shutil.copytree(
            os.path.join(_GAME_MODES_ROOT_PATH, "_package_data"),
            self.temp_dir.name,
            dirs_exist_ok=True,
        )
        GameModeManager.load_game_modes(info_only=True)
        self.url = reverse("file manager")

    def teardown_class(self):
        """Reset the :class: `~yawning_titan_gui.helpers.GameModeManager`."""
        GameModeManager.root_dir = GAME_MODES_DIR
        GameModeManager.game_modes = []

    def assert_correct_response_and_game_mode(
        self, game_mode_filename: str, response: HttpResponse
    ):
        """A method to execute some generic assertions that the view reports.

        - Status code is success (200)
        - The correct game mode config url is returned
        - The game mode exists in the :class: `~yawning_titan_gui.helpers.GameModeManager`
        """
        load = reverse(
            "game mode config",
            kwargs={"game_mode_filename": game_mode_filename},
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"load": load}).encode("utf-8")
        assert game_mode_filename in GameModeManager.game_modes

    def test_get(self, client: Client):
        """Test that the `file manager` view cannot accept get requests."""
        response = client.get(self.url)
        assert response.status_code == 400

    def test_post_invalid_operation(self, client: Client):
        """Test the function that processes gui requests when given an invalid operation."""
        game_mode_name = "test"
        response = client.post(
            self.url, {"game_mode_name": game_mode_name, "operation": "foo"}
        )
        assert response.status_code == 400

    def test_create(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode`."""
        game_mode_name = "test"
        game_mode_filename = f"{game_mode_name}.yaml"
        response = client.post(
            self.url, {"game_mode_name": game_mode_name, "operation": "create"}
        )
        self.assert_correct_response_and_game_mode(game_mode_filename, response)

    def test_create_from(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode_from`."""
        game_mode_name = "test"
        game_mode_filename = f"{game_mode_name}.yaml"
        response = client.post(
            self.url,
            {
                "game_mode_name": game_mode_name,
                "operation": "create from",
                "source_game_mode": "default_new_game_mode",
            },
        )
        self.assert_correct_response_and_game_mode(game_mode_filename, response)
        assert GameModeManager.get_game_mode(
            game_mode_filename
        ) == GameModeManager.get_game_mode("default_new_game_mode.yaml")

    def test_delete(self, client: Client, tmpdir_factory):
        """Test that a request to delete a game mode results in the correct game mode file being remove from the directory."""
        game_mode_name = "test"
        old_root = GameModeManager.root_dir
        GameModeManager.root_dir = Path(tmpdir_factory.mktemp("tmp_config"))
        GameModeManager.create_game_mode("test.yaml")
        response = client.post(
            self.url, {"game_mode_name": game_mode_name, "operation": "delete"}
        )
        assert response.status_code == 200
        assert not os.path.exists(GameModeManager.root_dir / "test.yaml")
        GameModeManager.root_dir = old_root
