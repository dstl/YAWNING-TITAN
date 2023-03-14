import json

import pytest
from django.http.response import HttpResponse
from django.test import Client
from django.urls import reverse

from yawning_titan.networks.network import Network
from yawning_titan_gui.helpers import NetworkManager

URL = reverse("Manage networks")
MANAGEMENT_URL = reverse("db manager")


@pytest.fixture
def assert_correct_response_and_network():
    """A method to execute some generic assertions that the view reports.

    - Status code is success (200)
    - The correct game mode config url is returned
    - The game mode exists in the :class: `~yawning_titan.networks.network_db.NetworkDB`
    """

    def _assert_correct_response_and_network(
        network_name: str, load: str, response: HttpResponse
    ):
        networks = [
            g for g in NetworkManager.db.all() if g.doc_metadata.name == network_name
        ]
        network = networks[0]
        assert len(networks) > 0
        if load == "next":
            load = reverse(
                "node editor",
                kwargs={"network_id": network.doc_metadata.uuid},
            )

        assert response.status_code == 200
        assert response.content == json.dumps({"load": load}).encode("utf-8")
        assert network.doc_metadata.name == network_name
        return network

    return _assert_correct_response_and_network


@pytest.mark.gui_test
def test_get(client: Client):
    """Test that the Manage networks view can accept GET requests."""
    response = client.get(URL)
    assert response.status_code == 200


@pytest.mark.gui_test
def test_post_invalid_operation(client: Client):
    """Test the function that processes gui requests when given an invalid operation."""
    response = client.post(URL, {"attribute": "test", "min": 1, "max": 1})
    assert response.status_code == 200
    assert response.content == json.dumps({"item_ids": []}).encode("utf-8")


@pytest.mark.gui_test
def test_create(assert_correct_response_and_network, client: Client):
    """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode`."""
    network_name = "test1"
    response = client.post(
        MANAGEMENT_URL,
        {
            "item_type": "network",
            "item_names[]": [network_name],
            "operation": "create",
        },
    )
    assert_correct_response_and_network(network_name, "next", response)


@pytest.mark.gui_test
def test_create_from(assert_correct_response_and_network, client: Client):
    """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode_from`."""
    network_name = "test2"
    source_network = NetworkManager.db.all()[0]
    response = client.post(
        MANAGEMENT_URL,
        {
            "item_type": "network",
            "operation": "create from",
            "source_item_id": source_network.doc_metadata.uuid,
            "item_names[]": [network_name],
        },
    )
    network: Network = assert_correct_response_and_network(
        network_name, "next", response
    )
    network_dict = network.to_dict()
    network_dict.pop("_doc_metadata")
    source_network_dict = source_network.to_dict()
    source_network_dict.pop("_doc_metadata")
    assert network_dict == source_network_dict


@pytest.mark.gui_test
def test_delete_single(temp_networks, client: Client):
    """Test that a request to delete a single network results in the network associated with the parsed id to be removed from the database."""
    network = NetworkManager.db.all()[0]
    id = temp_networks(network.doc_metadata.uuid, 1)[0]
    response = client.post(
        MANAGEMENT_URL,
        {"item_type": "network", "operation": "delete", "item_ids[]": [id]},
    )
    assert response.status_code == 200
    assert NetworkManager.db.get(id) is None


@pytest.mark.gui_test
def test_delete_multiple(temp_networks, client: Client):
    """Test that a request to delete multiple networks results in all the networks associated with the parsed ids to be removed from the database."""
    network = NetworkManager.db.all()[0]
    ids = temp_networks(network.doc_metadata.uuid, 5)
    response = client.post(
        MANAGEMENT_URL,
        {"item_type": "network", "operation": "delete", "item_ids[]": ids},
    )
    assert response.status_code == 200
    for id in ids:
        assert NetworkManager.db.get(id) is None
