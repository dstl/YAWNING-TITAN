import json

import pytest
from django.http.response import HttpResponse
from django.test import Client
from django.urls import reverse

from tests.gui import DEFAULT_GAME_MODE_ID
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_mode_db import default_game_mode
from yawning_titan_gui.views.utils.helpers import GameModeManager

URL = reverse("Manage game modes")
MANAGEMENT_URL = reverse("db manager")


@pytest.fixture
def assert_correct_response_and_game_mode(game_mode_manager: GameModeManager):
    """A method to execute some generic assertions that the view reports.

    - Status code is success (200)
    - The correct game mode config url is returned
    - The game mode exists in the :class: `~yawning_titan_gui.helpers.GameModeManager`
    """

    def _assert_correct_response_and_game_mode(
        game_mode_name: str, response: HttpResponse
    ):
        game_modes = [
            g
            for g in game_mode_manager.db.all()
            if g.doc_metadata.name == game_mode_name
        ]
        assert len(game_modes) > 0
        load = reverse(
            "game mode config",
            kwargs={"game_mode_id": game_modes[0].doc_metadata.uuid},
        )
        assert response.status_code == 200
        assert response.content == json.dumps({"load": load}).encode("utf-8")
        return game_modes[0]

    return _assert_correct_response_and_game_mode


@pytest.mark.gui_test
def test_get(client: Client):
    """Test that the `db manager` view cannot accept get requests."""
    response = client.get(MANAGEMENT_URL)
    assert response.status_code == 400


@pytest.mark.gui_test
def test_game_modes_view_get(client: Client):
    """Test that the Manage game modes view can accept GET requests."""
    response = client.get(URL)
    assert response.status_code == 200


@pytest.mark.gui_test
def test_game_modes_view_post(client: Client):
    """Test that the Manage game modes view can accept POST requests."""
    response = client.post(URL)
    assert response.status_code == 500


@pytest.mark.gui_test
def test_post_invalid_operation(client: Client):
    """Test the function that processes gui requests when given an invalid operation."""
    game_mode_name = "test1"
    response = client.post(
        MANAGEMENT_URL, {"game_mode_name": game_mode_name, "operation": "foo"}
    )
    assert response.status_code == 400


@pytest.mark.gui_test
def test_create(assert_correct_response_and_game_mode, client: Client):
    """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode`."""
    game_mode_name = "test2"
    response = client.post(
        MANAGEMENT_URL,
        {
            "item_names[]": [game_mode_name],
            "operation": "create",
            "item_type": "game_mode",
        },
    )
    assert_correct_response_and_game_mode(game_mode_name, response)


@pytest.mark.gui_test
def test_create_from(assert_correct_response_and_game_mode, client: Client):
    """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode_from`."""
    game_mode_name = "test"
    response = client.post(
        MANAGEMENT_URL,
        {
            "operation": "create from",
            "item_names[]": [game_mode_name],
            "item_type": "game_mode",
            "source_item_id": DEFAULT_GAME_MODE_ID,
        },
    )
    game_mode: GameMode = assert_correct_response_and_game_mode(
        game_mode_name, response
    )
    assert game_mode.doc_metadata.uuid != default_game_mode().doc_metadata.uuid
    assert game_mode == default_game_mode()


@pytest.mark.gui_test
def test_delete(game_mode_manager: GameModeManager, client: Client):
    """Test that a request to delete a game mode results in the correct game mode file being remove from the directory."""
    game_mode_name = "test3"
    doc = DocMetadata(name=game_mode_name)
    game_mode = GameMode(doc=doc)
    game_mode_manager.db.insert(game_mode)
    response = client.post(
        MANAGEMENT_URL,
        {
            "item_ids[]": [game_mode.doc_metadata.uuid],
            "item_names": [game_mode_name],
            "operation": "delete",
            "item_type": "game_mode",
        },
    )
    assert response.status_code == 200
    assert not GameModeManager.db.get(game_mode.doc_metadata.uuid)
