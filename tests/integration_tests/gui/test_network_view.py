import json
from typing import List
from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import Client
from django.urls import reverse

from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.networks.network_db import NetworkDB
from yawning_titan_gui.helpers import NetworkManager


class TestNetworkView:
    """Test processes executed through requests to the 'Manage game modes' and 'db manager' endpoints."""

    # test filtering where no high value nodes exist on a network!

    def setup_class(self):
        """Setup the components required to test the management of yawning titan networks."""
        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            NetworkManager.db = NetworkDB()

        self.management_url = reverse("db manager")
        self.url = reverse("Manage networks")

    def teardown_class(self):
        """Reset the components required to test the management of yawning titan networks."""
        NetworkManager.db._db.close_and_delete_temp_db()

    def assert_correct_response_and_network(
        self, network_name: str, load: str, response: HttpResponse
    ):
        """A method to execute some generic assertions that the view reports.

        - Status code is success (200)
        - The correct game mode config url is returned
        - The game mode exists in the :class: `~yawning_titan.networks.network_db.NetworkDB`
        """
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

    def create_temp_networks(self, source_network_id: str, n: int = 1) -> List[str]:
        """Create a number of temporary networks as copies of an existing network.

        :param source_network: The network id to copy
        :param n: The number of networks to create

        :return: a list of created network Ids.
        """
        ids = []
        for i in range(n):
            network = NetworkManager.db.get(source_network_id)
            meta = network.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            network._doc_metadata = DocMetadata(**meta)
            NetworkManager.db.insert(network=network, name="temp")
            ids.append(network.doc_metadata.uuid)
        return ids

    def test_get(self, client: Client):
        """Test that the Manage networks view can accept GET requests."""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_post_invalid_operation(self, client: Client):
        """Test the function that processes gui requests when given an invalid operation."""
        response = client.post(self.url, {"attribute": "test", "min": 1, "max": 1})
        assert response.status_code == 200
        assert response.content == json.dumps({"ids": None}).encode("utf-8")

    def test_create(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode`."""
        network_name = "test1"
        response = client.post(
            self.management_url,
            {
                "item_type": "network",
                "item_names[]": [network_name],
                "operation": "create",
            },
        )
        self.assert_correct_response_and_network(network_name, "next", response)

    def test_create_from(self, client: Client):
        """Test the function that processes gui requests to :method: `~yawning_titan_gui.helpers.GameModeManager.create_game_mode_from`."""
        network_name = "test2"
        source_network = NetworkManager.db.all()[0]
        response = client.post(
            self.management_url,
            {
                "item_type": "network",
                "operation": "create from",
                "source_item_id": source_network.doc_metadata.uuid,
                "item_names[]": [network_name],
            },
        )
        network = self.assert_correct_response_and_network(
            network_name, "next", response
        )
        network_dict = network.to_dict()
        network_dict.pop("_doc_metadata")
        source_network_dict = source_network.to_dict()
        source_network_dict.pop("_doc_metadata")
        assert network_dict == source_network_dict

    def test_delete_single(self, client: Client):
        """Test that a request to delete a single network results in the network associated with the parsed id to be removed from the database."""
        network = NetworkManager.db.all()[0]
        id = self.create_temp_networks(network.doc_metadata.uuid, 1)[0]
        response = client.post(
            self.management_url,
            {"item_type": "network", "operation": "delete", "item_ids[]": [id]},
        )
        assert response.status_code == 200
        assert NetworkManager.db.get(id) is None

    def test_delete_multiple(self, client: Client):
        """Test that a request to delete multiple networks results in all the networks associated with the parsed ids to be removed from the database."""
        network = NetworkManager.db.all()[0]
        ids = self.create_temp_networks(network.doc_metadata.uuid, 5)
        response = client.post(
            self.management_url,
            {"item_type": "network", "operation": "delete", "item_ids[]": ids},
        )
        assert response.status_code == 200
        for id in ids:
            assert NetworkManager.db.get(id) is None
