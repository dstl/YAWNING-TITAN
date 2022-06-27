from random import randint


def generate_vulnerability(lower_bound: float, upper_bound: float) -> float:
    """
    Generate a single vulnerability value.

    Args:
        lower_bound: lower bound of random generation
        upper_bound: upper bound of random generation

    Returns:
        A single float representing a vulnerability
    """
    return round(randint((100 * lower_bound), (100 * upper_bound)) / 100, 2)


def generate_vulnerabilities(
    n_nodes: int, lower_bound: float, upper_bound: float
) -> dict:
    """
    Generate vulnerability values for n nodes.

    These values are randomly generated between the upper and lower bounds within the
    settings.

    Args:
        n_nodes: Number of nodes within the environment
        settings_data: The environment settings object

    Returns:
        vulnerabilities: A dictionary containing the vulnerabilities
    """
    vulnerabilities = {}

    for i in range(n_nodes):
        vulnerabilities[str(i)] = generate_vulnerability(lower_bound, upper_bound)

    return vulnerabilities
