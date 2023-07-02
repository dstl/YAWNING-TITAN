import pytest

from yawning_titan.exceptions import NetworkError
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import default_18_node_network
from yawning_titan.networks.node import Node


@pytest.mark.unit_test
def test_reset_high_value_nodes_randomly():
    """Test the random setting of high value nodes in a network."""
    network = default_18_node_network()
    assert len(network.high_value_nodes) == 1  # starts with 1 entry node set

    network.num_of_random_high_value_nodes = 3
    network.reset_random_high_value_nodes()
    assert len(network.high_value_nodes) == 3

    # resetting hvn's overwrites the set of hvn's
    network.num_of_random_high_value_nodes = 1
    network.reset_random_high_value_nodes()
    assert len(network.high_value_nodes) == 1

    # setting too many hvn's overwrites the set number of hvn's to 15% num nodes
    network.num_of_random_high_value_nodes = 18
    network.reset_random_high_value_nodes()
    assert len(network.high_value_nodes) == 3


@pytest.mark.unit_test
def test_reset_entry_nodes_randomly():
    """Test the random setting of high value nodes in a network."""
    network = default_18_node_network()
    assert len(network.entry_nodes) == 1  # starts with 1 entry node set

    network.num_of_random_entry_nodes = 3
    network.reset_random_entry_nodes()
    assert len(network.entry_nodes) == 3

    # resetting entry nodes overwrites the set of entry nodes
    network.num_of_random_entry_nodes = 1
    network.reset_random_entry_nodes()
    assert len(network.entry_nodes) == 1

    # setting too many entry nodes has no effect
    network.num_of_random_entry_nodes = 18
    network.reset_random_entry_nodes()
    assert len(network.entry_nodes) == 18


@pytest.mark.unit_test
def test_setting_high_value_nodes_before_entry_nodes():
    """Test setting high value node before entry nodes."""
    router_1 = Node()
    switch_1 = Node()
    switch_2 = Node()
    pc_1 = Node()
    pc_2 = Node()
    pc_3 = Node()
    pc_4 = Node()
    pc_5 = Node()
    pc_6 = Node()
    server_1 = Node()
    server_2 = Node()
    network = Network(
        set_random_entry_nodes=True,
        num_of_random_entry_nodes=3,
        set_random_high_value_nodes=True,
        num_of_random_high_value_nodes=3,
        set_random_vulnerabilities=True,
    )
    network.add_node(router_1)
    network.add_node(switch_1)
    network.add_node(switch_2)
    network.add_node(pc_1)
    network.add_node(pc_2)
    network.add_node(pc_3)
    network.add_node(pc_4)
    network.add_node(pc_5)
    network.add_node(pc_6)
    network.add_node(server_1)
    network.add_node(server_2)
    network.add_edge(router_1, switch_1)
    network.add_edge(switch_1, server_1)
    network.add_edge(switch_1, pc_1)
    network.add_edge(switch_1, pc_2)
    network.add_edge(switch_1, pc_3)
    network.add_edge(router_1, switch_2)
    network.add_edge(switch_2, server_2)
    network.add_edge(switch_2, pc_4)
    network.add_edge(switch_2, pc_5)
    network.add_edge(switch_2, pc_6)

    with pytest.raises(NetworkError):
        network.reset_random_high_value_nodes()
