import networkx as nx
import numpy as np
import pytest

from yawning_titan.experiment_helpers import graph_metrics


@pytest.mark.integration_test
@pytest.mark.parametrize(
    "input_list, answer",
    [
        ([10, 20, 30, 50, 100], 31.291346445319),
        ([0.33, 0.42, 0.88, 0.41, 0.21], 0.402021991652),
    ],
)
def test_geometric_mean_overflow(input_list, answer):
    """
    Test to check geometric mean with overflow returns correct values.

    :param input_list: The values used to derive a geometric mean.
    :param answer: The geometric mean.
    """
    result = graph_metrics.geometric_mean_overflow(input_list)
    assert np.isclose(result, answer, rtol=1e-7)


@pytest.mark.integration_test
@pytest.mark.parametrize(
    "input_list, expected_len",
    [
        ([[20, 20], [20, 20, 30], [20, 20]], 7),
        ([[20, 10, 30, 40], [0.5, 10, 19999]], 7),
    ],
)
def test_flatten_list(input_list, expected_len):
    """
    Test to check helper function works as intended.

    :param input_list: A ragged list of lists.
    :param expected_len: The expected length once flattened.
    """
    res = graph_metrics.flatten_list(input_list)
    assert len(res) == expected_len


@pytest.mark.integration_test
def test_get_func_summary_statistics(default_network):
    """Test graph summary stats function returns expected number of elements."""
    metrics = graph_metrics.get_func_summary_statistics(
        nx.average_degree_connectivity(default_network)
    )
    assert len(metrics) == 6


@pytest.mark.integration_test
def test_get_graph_metric_bundle(default_network):
    """Test size and number of elements returned by graph metric bundle method."""
    metric_bundle = graph_metrics.get_graph_metric_bundle(default_network)

    assert len(metric_bundle) == 5

    for row in metric_bundle:
        assert len(row) == 7
