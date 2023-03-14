import json
from typing import List
from unittest.mock import patch

from django.test import Client
from django.urls import reverse

from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.networks.network_db import NetworkDB
from yawning_titan.networks.node import Node
from yawning_titan_gui.forms.network_forms import NetworkFormManager
from yawning_titan_gui.helpers import NetworkManager


class TestNetworkEditorView:
    """Test processes executed through requests to the 'Manage game modes' and 'db manager' endpoints."""

    # test filtering where no high value nodes exist on a network!

    def setup_class(self):
        """Setup the components required to test the management of yawning titan networks."""
        with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
            NetworkManager.db = NetworkDB()

        self.url = reverse("node editor")
        self.management_url = reverse("update network")
        self.updated_attr_example = {
            "set_random_entry_nodes": "on",
            "num_of_random_entry_nodes": "2",
            "random_entry_node_preference": "CENTRAL",
            "set_random_high_value_nodes": "on",
            "num_of_random_high_value_nodes": "1",
            "random_high_value_node_preference": "FURTHEST_AWAY_FROM_ENTRY",
            "node_vulnerability_lower_bound": "0.5",
            "node_vulnerability_upper_bound": "0.5",
        }

    def teardown_class(self):
        """Reset the components required to test the management of yawning titan networks."""
        NetworkManager.db._db.close_and_delete_temp_db()

    def create_temp_networks(self, source_network_id: str, n: int = 1) -> List[str]:
        """Create a number of temporary networks as copies of an existing network.

        :param source_network: The network id to copy
        :param n: The number of networks to create

        :return: a list of created network Ids.
        """
        ids = []
        for _ in range(n):
            network = NetworkManager.db.get(source_network_id)
            meta = network.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            network._doc_metadata = DocMetadata(**meta)
            NetworkManager.db.insert(network=network, name="temp")
            ids.append(network.doc_metadata.uuid)
        return ids

    def test_update_network_elements(self, client: Client):
        """Test that a network can be updated by positing a json representation of the form in the request body."""
        source_network = NetworkManager.db.all()[0]
        id = self.create_temp_networks(source_network.doc_metadata.uuid, 1)[0]
        network = NetworkManager.db.get(id)
        new_node = Node(name="new")
        network.add_node(new_node)
        response = client.post(
            reverse(
                "node editor",
                kwargs={"network_id": id},
            ),
            data=json.dumps(network.to_dict(json_serializable=True)),
            content_type="application/json",
        )
        updated_network = NetworkManager.db.get(id)
        assert response.status_code == 200
        assert id in NetworkFormManager.network_forms
        assert (
            NetworkFormManager.get_or_create_form(id).network.to_dict()
            == updated_network.to_dict()
        )
        assert (
            new_node in updated_network.nodes and new_node not in source_network.nodes
        )

    def test_update_network_attributes(self, client: Client):
        """Test that the attributes of a network can be updated independently of the elements from a django form."""
        source_network = NetworkManager.db.all()[0]
        id = self.create_temp_networks(source_network.doc_metadata.uuid, 1)[0]
        network = NetworkManager.db.get(id)
        self.updated_attr_example.update({"_network_id": id, "_operation": "update"})
        response = client.post(self.management_url, self.updated_attr_example)
        network_dict = json.loads(json.loads(response.content)["network_json"])
        assert response.status_code == 200
        assert (
            network.num_of_random_entry_nodes == 1
            and network_dict["num_of_random_entry_nodes"] == 2
        )
        assert id in NetworkFormManager.network_forms
        assert (
            NetworkFormManager.get_or_create_form(id).network.num_of_random_entry_nodes
            == 2
        )

    def test_cumulative_updates(self, client: Client):
        """Test that changes are persisted when updating network attributes then saving the complete network."""
        source_network = NetworkManager.db.all()[0]
        id = self.create_temp_networks(source_network.doc_metadata.uuid, 1)[0]
        network = NetworkManager.db.get(id)
        new_node = Node(name="new")
        network.add_node(new_node)
        client.post(
            reverse(
                "node editor",
                kwargs={"network_id": id},
            ),
            data=json.dumps(network.to_dict(json_serializable=True)),
            content_type="application/json",
        )
        self.updated_attr_example.update({"_network_id": id, "_operation": "update"})
        response = client.post(self.management_url, self.updated_attr_example)
        updated_network = NetworkManager.db.get(id)
        assert response.status_code == 200
        assert id in NetworkFormManager.network_forms
        assert (
            NetworkFormManager.get_or_create_form(id).network.to_dict()
            == updated_network.to_dict()
        )
        assert (
            new_node in updated_network.nodes and new_node not in source_network.nodes
        )
        assert (
            NetworkFormManager.get_or_create_form(id).network.num_of_random_entry_nodes
            == 2
        )
