import json
from typing import List
from unittest.mock import patch

from django.test import Client
from django.urls import reverse

from tests.mock_and_patch.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.game_modes.game_mode_db import GameModeDB, default_game_mode
from yawning_titan_gui.forms.game_mode_forms import GameModeFormManager
from yawning_titan_gui.helpers import GameModeManager


class TestGameModeConfigView:
    """Test processes executed through requests to the 'game mode config' and 'update config' endpoints."""

    def setup_class(self):
        """Setup the components required to test the management of yawning titan networks."""
        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            GameModeManager.db = GameModeDB()

        self.default_game_mode_id = default_game_mode().doc_metadata.uuid
        self.url = reverse(
            "game mode config",
            kwargs={
                "game_mode_id": self.default_game_mode_id,
                "section_name": "red",
            },
        )
        self.update_url = reverse("update config")

    def teardown_class(self):
        """Reset the components required to test the management of yawning titan networks."""
        GameModeManager.db._db.close_and_delete_temp_db()

    def create_temp_game_modes(self, source_game_mode_id: str, n: int = 1) -> List[str]:
        """Create a number of temporary networks as copies of an existing network.

        :param source_network: The network id to copy
        :param n: The number of networks to create

        :return: a list of created network Ids.
        """
        ids = []
        for _ in range(n):
            game_mode = GameModeManager.db.get(source_game_mode_id)
            meta = game_mode.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            game_mode._doc_metadata = DocMetadata(**meta)
            GameModeManager.db.insert(game_mode=game_mode, name="temp")
            ids.append(game_mode.doc_metadata.uuid)
        return ids

    def test_get_with_no_args(self, client: Client):
        """Test that a game mode config cannot be retrieved without a game_mode_filename."""
        url = reverse("game mode config")
        response = client.get(url)
        assert response.status_code == 404

    def test_get(self, client: Client):
        """Test that a valid game mode config url responds successfully to a get request."""
        response = client.get(self.url)
        assert response.status_code == 200
        assert "game_mode_config.html" in (t.name for t in response.templates)
        assert (
            default_game_mode().doc_metadata.uuid in GameModeFormManager.game_mode_forms
        )

    def test_finish(self, client: Client):
        """Test that when the last game mode section is updated the return is a redirect to the game mode manager."""
        url = reverse(
            "game mode config",
            kwargs={
                "game_mode_id": self.default_game_mode_id,
                "section_name": "miscellaneous",
            },
        )
        response = client.post(url)

        assert response.status_code == 302
        assert response["location"] == reverse("Manage game modes")
        assert GameModeManager.db.get(self.default_game_mode_id)
        # TODO add check that game mode saved

    def test_next_section(self, client: Client):
        """Test the next section is correctly chosen when a valid config is posted to the endpoint."""
        response = client.post(self.url)
        assert response.status_code == 302
        assert response["location"].split("/")[-2] == "blue"

    def test_save(self, client: Client):
        """Test that a save operation results in a file being created in the correct location."""
        id = self.create_temp_game_modes(default_game_mode().doc_metadata.uuid, 1)[0]
        response = client.post(
            self.update_url,
            {
                "_game_mode_id": id,
                "_section_name": "red",
                "_form_id": 3,
                "_operation": "save",
            },
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"message": "saved"}).encode("utf-8")
        assert GameModeManager.db.get(id)

    def test_update_fail(self, client: Client):
        """Test that when a config is updates and becomes invalid that an appropriate error message is returned."""
        id = self.create_temp_game_modes(default_game_mode().doc_metadata.uuid, 1)[0]
        response = client.post(
            self.update_url,
            {
                "_game_mode_id": id,
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
            in GameModeFormManager.game_mode_forms[id]
            .sections["red"]
            .forms[3]
            .config_class.validation.fail_reasons
        )
