from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from yawning_titan.config.game_config.config_abc import ConfigABC


# TODO: Update this class as part of AIDT-88.
@dataclass()
class NetworkConfig(ConfigABC):
    """Class that validates and stores Network Configuration."""

    matrix: np.array = field(
        metadata="Stores the matrix dictating how each node is connected to each other"
    )
    """Stores the matrix dictating how each node is connected to each other."""

    positions: Dict = field(
        metadata="Dictionary containing the positions of the nodes in the network ("
        "when displayed as a graph) "
    )
    """Dictionary containing the positions of the nodes in the network (when
    displayed as a graph)."""

    entry_nodes: Optional[List[str]] = field(metadata="List of entry nodes")
    """List of entry nodes"""

    vulnerabilities: Optional[Dict] = field(
        metadata="Dictionary containing the vulnerabilities of the nodes"
    )
    """Dictionary containing the vulnerabilities of the nodes."""

    high_value_nodes: Optional[List[str]] = field(metadata="List of high value nodes")
    """List of high value nodes."""

    @classmethod
    def create(
        cls,
        matrix: np.array,
        positions: Dict[str, List[int]],
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
    ) -> NetworkConfig:
        """
        Create and return an instance of `NetworkConfig`.

        Args:
            matrix: The network matrix as a 2D `np.array`.
            positions: The node positions as  dict.
            entry_nodes: An optional list of entry nodes. Has a default value of `None`.
            vulnerabilities: An optional dict of vulnerabilities. Has a default value of
             `None`.
            high_value_nodes: An optional list of high value nodes. Has a default value
             of `None`.

        Returns:
            An instance of `NetworkConfig`.
        """
        cls._validate(
            matrix=matrix,
            positions=positions,
            entry_nodes=entry_nodes,
            vulnerabilities=vulnerabilities,
            high_value_nodes=high_value_nodes,
        )

        network_config = NetworkConfig(
            matrix=matrix,
            positions=positions,
            entry_nodes=entry_nodes,
            vulnerabilities=vulnerabilities,
            high_value_nodes=high_value_nodes,
        )

        return network_config

    @classmethod
    def _validate(
        cls,
        matrix: np.array,
        positions: Dict,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
    ):
        # check that no entry nodes and high value nodes intersect
        if entry_nodes is not None and high_value_nodes is not None:
            if set(entry_nodes) & set(high_value_nodes):
                warnings.warn(
                    "Provided entry nodes and high value nodes intersect and may "
                    "cause the training to prematurely end."
                )
