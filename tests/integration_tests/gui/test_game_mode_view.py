import json
from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import Client
from django.urls import reverse

from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_mode_db import GameModeDB, default_game_mode
from yawning_titan_gui.helpers import GameModeManager


class TestGameModeManagerView:
    """Test processes executed through requests to the 'Manage game modes' and 'db manager' endpoints."""

    def setup_class(self):
        """Setup the components required to test the management of yawning titan networks."""
        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            GameModeManager.db = GameModeDB()

        _default_game_mode = default_game_mode()
        self.default_game_mode_id = _default_game_mode.doc_metadata.uuid
        self.url = reverse("Manage game modes")
        self.management_url = reverse("db manager")

    def teardown_class(self):
        """Reset the components required to test the management of yawning titan networks."""
        GameModeManager.db._db.close_and_delete_temp_db()

    def assert_correct_response_and_game_mode(
        self, game_mode_name: str, response: HttpResponse
    ):
        """A method to execute some generic assertions that the view reports.

        - Status code is success (200)
        - The correct game mode config url is returned
        - The game mode exists in the :class: `~yawning_titan_gui.helpers.GameModeManager`
        """
        game_modes = [
            g for g in GameModeManager.db.all() if g.doc_metadata.name == game_mode_name
        ]
        assert len(game_modes) > 0
        load = reverse(
            "game mode config",
            kwargs={"game_mode_id": game_modes[0].doc_metadata.uuid},
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"load": load}).encode("utf-8")
        return game_modes[0]

    def test_get(self, client: Client):
        """Test that the `db manager` view cannot accept get requests."""
        response = client.get(self.management_url)
        assert response.status_code == 400

    def test_game_modes_view_get(self, client: Client):
        """Test that the Manage game modes view can accept GET requests."""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_game_modes_view_post(self, client: Client):
        """Test that the Manage game modes view cannot accept POST requests.

        Status 405 represents not allowed request method.
        """
        response = client.post(self.url)
        assert response.status_code == 405

    def test_post_invalid_operation(self, client: Client):
        """Test the function that processes gui requests when given an invalid operation."""
        game_mode_name = "test1"
        response = client.post(
            self.management_url, {"game_mode_name": game_mode_name, "operation": "foo"}
        )
        assert response.status_code == 400

    def test_create(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode`."""
        game_mode_name = "test2"
        response = client.post(
            self.management_url,
            {
                "item_names[]": [game_mode_name],
                "operation": "create",
                "item_type": "game mode",
            },
        )
        self.assert_correct_response_and_game_mode(game_mode_name, response)

    def test_create_from(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode_from`."""
        game_mode_name = "test"
        response = client.post(
            self.management_url,
            {
                "operation": "create from",
                "item_names[]": [game_mode_name],
                "item_type": "game mode",
                "source_item_id": self.default_game_mode_id,
            },
        )
        game_mode = self.assert_correct_response_and_game_mode(game_mode_name, response)
        assert game_mode.doc_metadata.uuid != default_game_mode().doc_metadata.uuid
        assert game_mode == default_game_mode()

    def test_delete(self, client: Client):
        """Test that a request to delete a game mode results in the correct game mode file being remove from the directory."""
        game_mode_name = "test3"
        doc = DocMetadata(name=game_mode_name)
        game_mode = GameMode(doc=doc)
        GameModeManager.db.insert(game_mode)
        response = client.post(
            self.management_url,
            {
                "item_ids[]": [game_mode.doc_metadata.uuid],
                "item_names": [game_mode_name],
                "operation": "delete",
                "item_type": "game mode",
            },
        )
        assert response.status_code == 200
        assert not GameModeManager.db.get(game_mode.doc_metadata.uuid)
