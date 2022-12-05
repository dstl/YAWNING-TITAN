from pathlib import Path
from typing import Dict

import yaml
from yaml.loader import SafeLoader


def read_yaml_file(yaml_location: Path) -> Dict:
    """
    Reads and laods a `.yaml` filepath and returns it as a dict.

    Args:
        yaml_location:
            A `.yaml` filepath.
    Returns:
        The `.yaml` file as a dict.
    """
    try:
        with open(yaml_location) as f:
            return yaml.load(f, Loader=SafeLoader)
    except FileNotFoundError as e:
        raise e
