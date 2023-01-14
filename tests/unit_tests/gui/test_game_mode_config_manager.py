import json
import os
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
    def setup_class(self):
        GameModeManager.root_dir = Path(
            os.path.join(_LIB_CONFIG_ROOT_PATH, "_package_data", "game_modes")
        )
        self.url = reverse(
            "game mode config",
            kwargs={
                "game_mode_filename": "default_new_game_mode.yaml",
                "section_name": "red",
            },
        )
        self.update_url = reverse("update config")

    def teardown_class(self):
        GameModeManager.root_dir = GAME_MODES_DIR
        GameModeManager.game_modes = []
        GameModeFormManager.game_modes = []

    def test_get_with_no_args(self, client: Client):
        with pytest.raises(
            Http404, match="Can't find game mode section None in game mode None"
        ):
            url = reverse("game mode config")
            response = client.get(url)

    def test_get(self, client: Client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert "game_mode_config.html" in (t.name for t in response.templates)
        assert "default_new_game_mode.yaml" in GameModeFormManager.game_modes

    def test_finish(self, client: Client):
        url = reverse(
            "game mode config",
            kwargs={
                "game_mode_filename": "default_new_game_mode.yaml",
                "section_name": "miscellaneous",
            },
        )
        response = client.post(url)
        assert response.status_code == 302
        assert response["location"] == reverse("Manage game modes")
        # TODO add check that game mode saved

    def test_next_section(self, client: Client):
        response = client.post(self.url)
        assert response.status_code == 302
        assert response["location"].split("/")[-2] == "blue"

    def test_save(self, client: Client):
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
