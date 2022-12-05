import warnings

import numpy as np

from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.envs.generic.helpers import network_creator


def test_config_properties():
    """Tests creation of `NetworkConfig`."""
    matrix, node_positions = network_creator.create_18_node_network()
    network_config = NetworkConfig.create_from_args(
        matrix=matrix,
        positions=node_positions,
        entry_nodes=["0"],
        high_value_nodes=["1"],
    )

    assert np.array_equal(network_config.matrix, matrix) is True
    assert network_config.positions == node_positions
    assert network_config.entry_nodes[0] == "0"
    assert network_config.high_value_nodes[0] == "1"


def test_hvn_entry_node_matching():
    """Tests when high value node is also an entry node."""
    with warnings.catch_warnings(record=True) as w:
        matrix, node_positions = network_creator.create_18_node_network()
        NetworkConfig.create_from_args(
            matrix=matrix,
            positions=node_positions,
            entry_nodes=["0"],
            high_value_nodes=["0"],
        )

        # check that a warning was raised that the entry nodes and high value nodes intersect
        assert (
            str(w[0].message.args[0])
            == "Provided entry nodes and high value nodes intersect and may cause the training to prematurely end."
        )
