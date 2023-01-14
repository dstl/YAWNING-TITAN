import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest
from django.test import Client
from django.urls import reverse

from dist.manage.django.http.response import HttpResponse
from yawning_titan import GAME_MODES_DIR
from yawning_titan.config import _LIB_CONFIG_ROOT_PATH
from yawning_titan_gui.helpers import GameModeManager


def test_game_modes_view(client: Client):
    url = reverse("Manage game modes")
    response = client.get(url)
    assert response.status_code == 200


class TestConfigFileManager:
    def setup_class(self):
        f = tempfile.mktemp()
        GameModeManager.root_dir = Path(f)
        shutil.copytree(
            os.path.join(_LIB_CONFIG_ROOT_PATH, "_package_data", "game_modes"), f
        )
        GameModeManager.load_game_mode_info()
        self.url = reverse("file manager")

    def teardown_class(self):
        GameModeManager.root_dir = GAME_MODES_DIR
        GameModeManager.game_modes = []

    def assert_correct_response_and_game_mode(
        self, game_mode_filename: str, response: HttpResponse
    ):
        load = reverse(
            "game mode config",
            kwargs={"game_mode_filename": game_mode_filename},
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"load": load}).encode("utf-8")
        assert game_mode_filename in GameModeManager.game_modes

    def test_get(self, client: Client):
        response = client.get(self.url)
        assert response.status_code == 400

    def test_post_invalid_operation(self, client: Client):
        game_mode_name = "test"
        response = client.post(
            self.url, {"game_mode_name": game_mode_name, "operation": "foo"}
        )
        assert response.status_code == 400

    def test_create(self, client: Client):
        game_mode_name = "test"
        game_mode_filename = f"{game_mode_name}.yaml"
        response = client.post(
            self.url, {"game_mode_name": game_mode_name, "operation": "create"}
        )
        self.assert_correct_response_and_game_mode(game_mode_filename, response)

    def test_create_from(self, client: Client):
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
