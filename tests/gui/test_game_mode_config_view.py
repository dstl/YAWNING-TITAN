import json
from typing import List

import pytest
from django.test import Client
from django.urls import reverse

from tests.gui import DEFAULT_GAME_MODE_ID
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.game_modes.game_mode_db import default_game_mode
from yawning_titan_gui.forms.game_mode_forms import GameModeFormManager
from yawning_titan_gui.views.utils.helpers import GameModeManager

URL = reverse(
    "game mode config",
    kwargs={
        "game_mode_id": DEFAULT_GAME_MODE_ID,
        "section_name": "red",
    },
)
UPDATE_URL = reverse("update config")


@pytest.fixture
def temp_game_modes(game_mode_manager: GameModeManager) -> List[str]:
    """Create a number of temporary networks as copies of an existing network.

    :param source_network: The network id to copy
    :param n: The number of networks to create

    :return: a list of created network Ids.
    """

    def _temp_game_modes(source_game_mode_id: str, n: int = 1):
        ids = []
        for _ in range(n):
            game_mode = game_mode_manager.db.get(source_game_mode_id)
            meta = game_mode.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            game_mode._doc_metadata = DocMetadata(**meta)
            game_mode_manager.db.insert(game_mode=game_mode, name="temp")
            ids.append(game_mode.doc_metadata.uuid)
        return ids

    return _temp_game_modes


@pytest.mark.gui_test
def test_get_with_no_args(client: Client):
    """Test that a game mode config cannot be retrieved without a _game_mode_id."""
    url = reverse("game mode config")
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.gui_test
def test_get(client: Client):
    """Test that a valid game mode config url responds successfully to a get request."""
    response = client.get(URL)
    assert response.status_code == 200
    assert "game_mode_config.html" in (t.name for t in response.templates)
    assert default_game_mode().doc_metadata.uuid in GameModeFormManager.game_mode_forms


@pytest.mark.gui_test
def test_finish(game_mode_manager: GameModeManager, client: Client):
    """Test that when the last game mode section is updated the return is a redirect to the game mode manager."""
    url = reverse(
        "game mode config",
        kwargs={
            "game_mode_id": DEFAULT_GAME_MODE_ID,
            "section_name": "miscellaneous",
        },
    )
    response = client.post(url)

    assert response.status_code == 302
    assert response["location"] == reverse("Manage game modes")
    assert game_mode_manager.db.get(DEFAULT_GAME_MODE_ID)


@pytest.mark.gui_test
def test_next_section(client: Client):
    """Test the next section is correctly chosen when a valid config is posted to the endpoint."""
    response = client.post(URL)
    assert response.status_code == 302
    assert response["location"].split("/")[-2] == "blue"


@pytest.mark.gui_test
def test_save(game_mode_manager: GameModeManager, temp_game_modes, client: Client):
    """Test that a save operation results in a file being created in the correct location."""
    id = temp_game_modes(DEFAULT_GAME_MODE_ID, 1)[0]
    response = client.post(
        UPDATE_URL,
        {
            "_game_mode_id": id,
            "_section_name": "red",
            "_form_id": 3,
            "_operation": "save",
        },
    )
    assert response.status_code == 200
    assert response.content == json.dumps({"message": "saved"}).encode("utf-8")
    assert game_mode_manager.db.get(id)


@pytest.mark.gui_test
def test_update_fail(temp_game_modes, client: Client):
    """Test that when a config is updates and becomes invalid that an appropriate error message is returned."""
    id = temp_game_modes(DEFAULT_GAME_MODE_ID, 1)[0]
    response = client.post(
        UPDATE_URL,
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
