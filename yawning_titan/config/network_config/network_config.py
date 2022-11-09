from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

import numpy as np

from yawning_titan.config.game_config.config_abc import ConfigABC

# TODO: Update this class as part of AIDT-88.
@dataclass()
class NetworkConfig(ConfigABC):
    """
    Class that validates and stores Network Configuration
    """

    matrix: np.array = field(
        metadata="Stores the matrix dictating how each node is connected to each other"
    )
    """Stores the matrix dictating how each node is connected to each other"""

    positions: Dict = field(
        metadata="Dictionary containing the positions of the nodes in the network (when displayed as a graph)"
    )
    """Dictionary containing the positions of the nodes in the network (when displayed as a graph)"""

    entry_nodes: Optional[List[str]] = field(metadata="List of entry nodes")
    """List of entry nodes"""

    vulnerabilities: Optional[Dict] = field(
        metadata="Dictionary containing the vulnerabilities of the nodes"
    )
    """Dictionary containing the vulnerabilities of the nodes"""

    high_value_targets: Optional[List[str]] = field(metadata="List of high value nodes")
    """List of high value nodes"""

    @classmethod
    def create(
        cls,
        matrix: np.array,
        positions: Dict,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_targets: Optional[List[str]] = None,
    ):
        cls._validate(
            matrix=matrix,
            positions=positions,
            entry_nodes=entry_nodes,
            vulnerabilities=vulnerabilities,
            high_value_targets=high_value_targets,
        )

        network_config = NetworkConfig(
            matrix=matrix,
            positions=positions,
            entry_nodes=entry_nodes,
            vulnerabilities=vulnerabilities,
            high_value_targets=high_value_targets,
        )

        return network_config

    @classmethod
    def _validate(
        cls,
        matrix: np.array,
        positions: Dict,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_targets: Optional[List[str]] = None,
    ):
        # check that no entry nodes and high value nodes intersect
        if set(entry_nodes) & set(high_value_targets):
            warnings.warn(
                "Provided entry nodes and high value targets intersect and may cause the training to prematurely end"
            )
