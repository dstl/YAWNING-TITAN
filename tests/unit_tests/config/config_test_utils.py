from pathlib import Path

import yaml
from yaml.loader import SafeLoader


def read_yaml_file(yaml_location: Path):
    try:
        with open(yaml_location) as f:
            return yaml.load(f, Loader=SafeLoader)
    except FileNotFoundError as e:
        raise e
