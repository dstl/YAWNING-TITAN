"""Collection of functions to help generating metrics and summary statistics for networkx graphs."""
import statistics as stats
from typing import Callable, List

import networkx as nx
import numpy as np
from tabulate import tabulate

from yawning_titan.experiment_helpers.constants import STANDARD_GRAPH_METRIC_HEADERS


def geometric_mean_overflow(input_list: List) -> float:
    """
    Calculate the geometric mean accounting for the potential of overflow through using logs.

    Args:
        input_list: A list of values

    Returns:
        Geometric mean as a float

    Note: There is actually a function included in the 'statistics'
    python module that does this but is only available in python 3.8 onwards
    """
    a = np.log(input_list)
    return np.exp(a.mean())


def flatten_list(list_input: list) -> list:
    """
    Take a list of lists and flattens them into a single list.

    Args:
        list_input: The input list of lists to be processed

    Returns:
        A single list containing all elements
    """
    return [item for sublist in list_input for item in sublist]


def get_assortativity_metrics(graph: nx.Graph):
    """
    Get assortativity metrics for an input graph using networkx's in-built algorithms.

    Args:
        graph: A networkx graph

    Returns:
        A two-tuple with the metrics
    """
    degree_assortativity_coef = nx.degree_assortativity_coefficient(graph)
    degree_pearson_coef = nx.degree_pearson_correlation_coefficient(graph)

    return (degree_assortativity_coef, degree_pearson_coef)


def get_func_summary_statistics(func: Callable) -> list:
    """
    Generate a list of summary statistics based on the output of a networkx in-build algorithm.

    Args:
        func: A networkx algorithm function

    Returns:
        A list containing:
            - Arithmetic Mean
            - Geometric Mean
            - Harmonic Mean
            - Standard Deviation
            - Variance
            - Median

    Example:

        > generate_summary_statistics(nx.degree_centrality(graph))
        > (3.3095238095238098, 2.5333333333333337, 2.9015675801088014, 1.9824913893491538, 2.620181405895692, 3.0)
    """
    metric_dict = func

    if isinstance(metric_dict, dict):
        metrics = list(metric_dict.values())
    else:
        raise TypeError(f"Expected an input type of dict. Got {type(metric_dict)}")

    mean = stats.mean(metrics)
    geomean = geometric_mean_overflow(metrics)
    harmonic_mean = stats.harmonic_mean(metrics)
    stdev = stats.stdev(metrics)
    variance = stats.pvariance(metrics)
    median = stats.median(metrics)

    return [mean, harmonic_mean, geomean, stdev, variance, median]


def get_graph_metric_bundle(graph: nx.Graph) -> List[List]:
    """
    Generate a graph metric bundle.

    A graph metric bundle includes the summary statistics for a
    collection of networkx in-built algorithms.

    Algorithms used:
        - Average Degree Connectivity
        - Closeness Centrality
        - Degree Centrality
        - Eigenvector Centrality
        - Communicability Between-ness Centrality

    Args:
        graph: A networkx graph

    Returns:
        A list of lists containing the metrics
    """
    funcs_to_process = [
        nx.average_degree_connectivity(graph),
        nx.closeness_centrality(graph),
        nx.degree_centrality(graph),
        nx.eigenvector_centrality(graph),
        nx.communicability_betweenness_centrality(graph),
    ]

    func_names = [
        "Avg Degree Connectivity",
        "Closeness Centrality",
        "Degree Centrality",
        "Eigenvector Centrality",
        "Communicability Between-ness Centrality",
    ]

    metric_outputs = []
    for func, name in zip(funcs_to_process, func_names):
        output = get_func_summary_statistics(func)
        output.insert(0, name)
        metric_outputs.append(output)

    return metric_outputs


def pprint_metric_table(metric_output: List[List], headers=None):
    """
    Pretty prints graph metrics to the terminal using the tabulate module.

    Args:
        metric_output: A list of lists containing the values to be printed.
        headers: A list of heading names (optional)

    Returns:
        A formatted table to terminal
    """
    if headers:
        print(tabulate(metric_output, headers))
    else:
        print(tabulate(metric_output, headers=STANDARD_GRAPH_METRIC_HEADERS))
