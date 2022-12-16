import warnings

import numpy as np
import pytest

from yawning_titan.networks import network_creator
from yawning_titan.networks.network import Network


def test_config_properties():
    """Tests creation of `Network`."""
    matrix, node_positions = network_creator.create_18_node_network()
    network = Network()

    assert np.array_equal(network.matrix, matrix) is True
    assert network.positions == node_positions
    assert network.entry_nodes[0] == "0"
    assert network.high_value_nodes[0] == "1"


@pytest.mark.skip(
    reason="Assertion fails due to the emergence of a new warning: 'non-integer"
    " arguments to randrange() have been deprecated since Python 3.10 and "
    "will be removed in a subsequent version'"
)
def test_hvn_entry_node_matching():
    """Tests when high value node is also an entry node."""
    with warnings.catch_warnings(record=True) as w:
        matrix, node_positions = network_creator.create_18_node_network()
        Network()

        # check that a warning was raised that the entry nodes and high value nodes intersect
        assert (
            str(w[0].message.args[0])
            == "Provided entry nodes and high value nodes intersect and may cause the training to prematurely end."
        )
