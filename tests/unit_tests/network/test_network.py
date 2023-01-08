import warnings

import numpy as np
import pytest

from yawning_titan.exceptions import ConfigGroupValidationError
from yawning_titan.networks import network_creator
from yawning_titan.networks.new_network import (
    EntryNodePlacementGroup,
    HighValueNodePlacementGroup,
    Network,
    NodePlacementGroup,
    NodeVulnerabilityGroup,
)


def test_config_properties():
    """Tests creation of `Network`."""
    matrix, node_positions = network_creator.create_18_node_network()
    network = Network(
        matrix=matrix,
        positions=node_positions,
        entry_nodes=["0"],
        high_value_nodes=["1"],
    )

    assert np.array_equal(network.matrix, matrix) is True
    assert network.positions == node_positions
    assert network.entry_nodes[0] == "0"
    assert network.high_value_nodes[0] == "1"


def test_entry_node_placement_valid_input():
    """Tests validation of :class: `~yawning_titan.networks.new_network.NodePlacementGroup`."""
    node_placement = NodePlacementGroup(use=False, count=2, random=True)
    assert node_placement.validation.passed
    assert node_placement.validation.group_passed


def test_entry_node_placement_multiple_methods():
    """Tests validation of :class: `~yawning_titan.networks.new_network.EntryNodePlacementGroup`."""
    node_placement = EntryNodePlacementGroup(
        use=True, count=2, random=True, place_close_to_center=True
    )
    assert not node_placement.validation.passed
    assert node_placement.validation.elements_passed
    assert (
        "2 methods of choosing node placement have been selected but only 1 can be used"
        in node_placement.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise node_placement.validation.fail_exceptions[0]


def test_high_value_node_placement_multiple_methods():
    """Tests validation of :class: `~yawning_titan.networks.new_network.HighValueNodePlacementGroup`."""
    node_placement = HighValueNodePlacementGroup(
        use=True, count=2, random=True, place_far_from_entry=True
    )
    assert not node_placement.validation.passed
    assert node_placement.validation.elements_passed
    assert (
        "2 methods of choosing node placement have been selected but only 1 can be used"
        in node_placement.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise node_placement.validation.fail_exceptions[0]


def test_node_vulnerability_group_float_value():
    """Tests validation of :class: `~yawning_titan.networks.new_network.NodeVulnerabilityGroup`."""
    node_vulnerability = NodeVulnerabilityGroup(restrict=True, min=1.2, max=2.4)
    assert node_vulnerability.validation.passed
    assert node_vulnerability.validation.group_passed


@pytest.mark.skip(
    reason="Assertion fails due to the emergence of a new warning: 'non-integer"
    " arguments to randrange() have been deprecated since Python 3.10 and "
    "will be removed in a subsequent version'"
)
def test_hvn_entry_node_matching():
    """Tests when high value node is also an entry node."""
    with warnings.catch_warnings(record=True) as w:
        matrix, node_positions = network_creator.create_18_node_network()
        Network(
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
