from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from yawning_titan.config.game_config.config_abc import ConfigABC


@dataclass()
class NetworkConfig(ConfigABC):
    """Class that validates and stores Network Configuration."""

    _matrix: np.array
    """The matrix as a 2D Numpy Array dictating how each node is connected to each other."""

    _positions: Dict[str, List[str]]
    """Dictionary containing the positions of the nodes in the network (when displayed as a graph)."""

    _entry_nodes: Optional[List[str]] = None
    """List of entry nodes. Has a default value on `None`."""

    _vulnerabilities: Optional[Dict] = None
    """Dictionary containing the vulnerabilities of the nodes. Has a default value on `None`."""

    _high_value_nodes: Optional[List[str]] = None
    """List of high value nodes. Has a default value on `None`."""

    # region Getters
    @property
    def matrix(self) -> np.array:
        """The matrix as a 2D Numpy Array dictating how each node is connected to each other."""
        return self._matrix

    @property
    def positions(self) -> Dict[str, List[str]]:
        """Dictionary containing the positions of the nodes in the network (when displayed as a graph)."""
        return self._positions

    @property
    def entry_nodes(self) -> Optional[List[str]]:
        """List of entry nodes. Has a default value on `None`."""
        return self._entry_nodes

    @property
    def vulnerabilities(self) -> Optional[Dict]:
        """Dictionary containing the vulnerabilities of the nodes. Has a default value on `None`."""
        return self._vulnerabilities

    @property
    def high_value_nodes(self) -> Optional[List[str]]:
        """List of high value nodes. Has a default value on `None`."""
        return self._high_value_nodes

    # endregion

    # region Setters
    @matrix.setter
    def matrix(self, val: np.array):
        self._matrix = val

    @positions.setter
    def positions(self, val: Dict[str, List[str]]):
        self._positions = val

    @entry_nodes.setter
    def entry_nodes(self, val: List[str]):
        self._entry_nodes = val

    @vulnerabilities.setter
    def vulnerabilities(self, val: Dict):
        self._vulnerabilities = val

    @high_value_nodes.setter
    def high_value_nodes(self, val: List[str]):
        self._high_value_nodes = val

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]):
        """
        Create and return an instance of :class:`NetworkConfig`.

        Args:
            config_dict: The network config dict.
        Returns:
            An instance of `NetworkConfig`.

        Examples:
            >>> from yawning_titan.envs.generic.helpers.network_creator import create_18_node_network
            >>> from yawning_titan.config.network_config.network_config import NetworkConfig
            >>> network_config = NetworkConfig.create(create_18_node_network())
        """
        cls.validate(config_dict)

        matrix = config_dict["matrix"]
        positions = config_dict["positions"]
        entry_nodes = config_dict["entry_nodes"]
        vulnerabilities = config_dict["vulnerabilities"]
        high_value_nodes = config_dict["high_value_nodes"]

        network_config = NetworkConfig(
            _matrix=matrix,
            _positions=positions,
            _entry_nodes=entry_nodes,
            _vulnerabilities=vulnerabilities,
            _high_value_nodes=high_value_nodes,
        )

        return network_config

    @classmethod
    def create_from_args(
        cls,
        matrix: np.array,
        positions: Dict[str, List[str]],
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
    ):
        """
        Create and return an instance of `NetworkConfig`.

        Args:
            matrix: The matrix as a 2D Numpy Array dictating how each node is connected to each other.
            positions: Dictionary containing the positions of the nodes in the network (when displayed as a graph).
            entry_nodes: List of entry nodes. Has a default value on `None`.
            vulnerabilities: Dictionary containing the vulnerabilities of the nodes. Has a default value on `None`.
            high_value_nodes: List of high value nodes. Has a default value on `None`.

        Returns:
            An instance of `NetworkConfig`.
        """
        network_config_dict = {
            "matrix": matrix,
            "positions": positions,
            "entry_nodes": entry_nodes,
            "vulnerabilities": vulnerabilities,
            "high_value_nodes": high_value_nodes,
        }

        return NetworkConfig.create(network_config_dict)

    @classmethod
    def validate(cls, config_dict: Dict[str, Any]):
        """Validates the network config dict."""
        entry_nodes = config_dict["entry_nodes"]
        high_value_nodes = config_dict["high_value_nodes"]

        # check that no entry nodes and high value nodes intersect
        if entry_nodes is not None and high_value_nodes is not None:
            if set(entry_nodes) & set(high_value_nodes):
                warnings.warn(
                    "Provided entry nodes and high value nodes intersect and may cause the training to prematurely end."
                )
