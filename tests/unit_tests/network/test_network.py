import pytest

from yawning_titan.networks import network_creator
from yawning_titan.networks.network_db import default_18_node_network


def test_reset_high_value_nodes_randomly():
    """Test the random setting of high value nodes in a network."""
    network = default_18_node_network()
    assert len(network.high_value_nodes) == 0  # starts with no hnv's set

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


def test_reset_entry_nodes_randomly():
    """Test the random setting of high value nodes in a network."""
    network = default_18_node_network()
    assert len(network.entry_nodes) == 0  # starts with no entry nodes set

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


def test_create_network_from_legacy_manual_vulnerability_setting():
    """Test manually setting vulnerability."""
    adj_matrix, node_positions = network_creator.create_mesh(size=3, connectivity=0.7)
    vulnerabilities = {"0": 0.5, "1": 0.5, "2": 0.5}

    network_legacy_config = {
        "GAME_RULES": {
            "choose_entry_nodes_randomly": True,
            "choose_high_value_nodes_placement_at_random": True,
            "number_of_entry_nodes": 1,
            "number_of_high_value_nodes": 1,
            "node_vulnerability_lower_bound": 0.1,
            "node_vulnerability_upper_bound": 1,
            "prefer_central_nodes_for_entry_nodes": False,
            "prefer_edge_nodes_for_entry_nodes": False,
            "choose_high_value_nodes_furthest_away_from_entry": False,
        }
    }

    # Ensure that warning is raised when Entry nodes and HVN's intersect
    network = network_creator.create_network(
        legacy=True,
        config_dict=network_legacy_config,
        adj_matrix=adj_matrix,
        positions=node_positions,
        vulnerabilities=vulnerabilities,
    )
    assert all(n.vulnerability == 0.5 for n in network.nodes)


def test_create_network_from_legacy_random_vulnerability():
    """Test manually setting vulnerability."""
    adj_matrix, node_positions = network_creator.create_mesh(size=3, connectivity=0.7)

    network_legacy_config = {
        "GAME_RULES": {
            "choose_entry_nodes_randomly": True,
            "choose_high_value_nodes_placement_at_random": True,
            "number_of_entry_nodes": 1,
            "number_of_high_value_nodes": 1,
            "node_vulnerability_lower_bound": 0.1,
            "node_vulnerability_upper_bound": 1,
            "prefer_central_nodes_for_entry_nodes": False,
            "prefer_edge_nodes_for_entry_nodes": False,
            "choose_high_value_nodes_furthest_away_from_entry": False,
        }
    }

    # Ensure that warning is raised when Entry nodes and HVN's intersect
    network = network_creator.create_network(
        legacy=True,
        config_dict=network_legacy_config,
        adj_matrix=adj_matrix,
        positions=node_positions,
    )
    assert all(n.vulnerability > 0 and n.vulnerability_score > 0 for n in network.nodes)


def test_create_network_vulnerability_out_of_range():
    """Test that the lower bound of node vulnerability cannot be less than or equal to 0."""
    adj_matrix, node_positions = network_creator.create_mesh(size=3, connectivity=0.7)

    network_legacy_config = {
        "GAME_RULES": {
            "choose_entry_nodes_randomly": True,
            "choose_high_value_nodes_placement_at_random": True,
            "number_of_entry_nodes": 1,
            "number_of_high_value_nodes": 1,
            "node_vulnerability_lower_bound": 0,
            "node_vulnerability_upper_bound": 1,
            "prefer_central_nodes_for_entry_nodes": False,
            "prefer_edge_nodes_for_entry_nodes": False,
            "choose_high_value_nodes_furthest_away_from_entry": False,
        }
    }

    with pytest.raises(ValueError):
        # Ensure that error is raised when out of range
        network_creator.create_network(
            legacy=True,
            config_dict=network_legacy_config,
            adj_matrix=adj_matrix,
            positions=node_positions,
        )


def test_create_network_from_legacy_manual_special_node_setting():
    """Test that creating a network from a legacy configuration can have its special nodes set manually."""
    network_legacy_config = {
        "GAME_RULES": {
            "choose_entry_nodes_randomly": False,
            "choose_high_value_nodes_placement_at_random": False,
            "number_of_entry_nodes": 1,
            "number_of_high_value_nodes": 1,
            "node_vulnerability_lower_bound": 0.1,
            "node_vulnerability_upper_bound": 1,
            "prefer_central_nodes_for_entry_nodes": False,
            "prefer_edge_nodes_for_entry_nodes": False,
            "choose_high_value_nodes_furthest_away_from_entry": False,
        }
    }

    adj_matrix, node_positions = network_creator.create_mesh(size=25, connectivity=0.7)

    # Ensure that warning is raised when Entry nodes and HVN's intersect
    with pytest.warns(
        UserWarning,
        match="Entry nodes and high value nodes intersect at node "
        "'2', and may cause the training to end "
        "prematurely.",
    ):
        network = network_creator.create_network(
            legacy=True,
            config_dict=network_legacy_config,
            adj_matrix=adj_matrix,
            positions=node_positions,
            high_value_node_names=["0", "1", "2"],
            entry_node_names=["2", "5", "6"],
        )

    assert set([n.name for n in network.high_value_nodes]) == set(["0", "1", "2"])
    assert set([n.name for n in network.entry_nodes]) == set(["2", "5", "6"])
