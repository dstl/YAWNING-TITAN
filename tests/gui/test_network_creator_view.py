import json

import pytest
from django.test import Client
from django.urls import reverse

from yawning_titan.networks.node import Node
from yawning_titan_gui.forms.network_forms import NetworkFormManager
from yawning_titan_gui.helpers import NetworkManager

URL = reverse("node editor")
MANAGEMENT_URL = reverse("update network")
UPDATED_ATTRIBUTES = {
    "set_random_entry_nodes": "on",
    "num_of_random_entry_nodes": "2",
    "random_entry_node_preference": "CENTRAL",
    "set_random_high_value_nodes": "on",
    "num_of_random_high_value_nodes": "1",
    "random_high_value_node_preference": "FURTHEST_AWAY_FROM_ENTRY",
    "node_vulnerability_lower_bound": "0.5",
    "node_vulnerability_upper_bound": "0.5",
}


@pytest.mark.gui_test
def test_update_network_elements(temp_networks, client: Client):
    """Test that a network can be updated by positing a json representation of the form in the request body."""
    source_network = NetworkManager.db.all()[0]
    id = temp_networks(source_network.doc_metadata.uuid, 1)[0]
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
    assert new_node in updated_network.nodes and new_node not in source_network.nodes


@pytest.mark.gui_test
def test_update_network_attributes(temp_networks, client: Client):
    """Test that the attributes of a network can be updated independently of the elements from a django form."""
    source_network = NetworkManager.db.all()[0]
    id = temp_networks(source_network.doc_metadata.uuid, 1)[0]
    network = NetworkManager.db.get(id)
    UPDATED_ATTRIBUTES.update({"_network_id": id, "_operation": "update"})
    response = client.post(MANAGEMENT_URL, UPDATED_ATTRIBUTES)
    network_dict = json.loads(json.loads(response.content)["network_json"])
    assert response.status_code == 200
    assert (
        network.num_of_random_entry_nodes == 1
        and network_dict["num_of_random_entry_nodes"] == 2
    )
    assert id in NetworkFormManager.network_forms
    assert (
        NetworkFormManager.get_or_create_form(id).network.num_of_random_entry_nodes == 2
    )


@pytest.mark.gui_test
def test_cumulative_updates(temp_networks, client: Client):
    """Test that changes are persisted when updating network attributes then saving the complete network."""
    source_network = NetworkManager.db.all()[0]
    id = temp_networks(source_network.doc_metadata.uuid, 1)[0]
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
    UPDATED_ATTRIBUTES.update({"_network_id": id, "_operation": "update"})
    response = client.post(MANAGEMENT_URL, UPDATED_ATTRIBUTES)
    updated_network = NetworkManager.db.get(id)
    assert response.status_code == 200
    assert id in NetworkFormManager.network_forms
    assert (
        NetworkFormManager.get_or_create_form(id).network.to_dict()
        == updated_network.to_dict()
    )
    assert new_node in updated_network.nodes and new_node not in source_network.nodes
    assert (
        NetworkFormManager.get_or_create_form(id).network.num_of_random_entry_nodes == 2
    )
