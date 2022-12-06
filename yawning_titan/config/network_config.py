from __future__ import annotations

import warnings
from dataclasses import dataclass
from logging import getLogger
from typing import Any, Dict, List, Optional

from numpy import ndarray

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.db.doc_metadata import DocMetadata

_LOGGER = getLogger(__name__)


@dataclass()
class NetworkConfig(ConfigABC):
    """Class that validates and stores Network Configuration."""

    matrix: ndarray
    """The matrix as a 2D Numpy Array dictating how each node is connected to each other."""

    positions: Dict[str, List[str]]
    """Dictionary containing the positions of the nodes in the network (when displayed as a graph)."""

    entry_nodes: Optional[List[str]] = None
    """List of entry nodes. Has a default value on `None`."""

    vulnerabilities: Optional[Dict] = None
    """Dictionary containing the vulnerabilities of the nodes. Has a default value on `None`."""

    high_value_nodes: Optional[List[str]] = None
    """List of high value nodes. Has a default value on `None`."""

    _doc_metadata: Optional[DocMetadata] = None
    """The associated instance of :class:`~yawning_titan.db.doc_metadata.DocMetadata`."""

    def __post_init__(self):
        if self._doc_metadata is None:
            self._doc_metadata = DocMetadata()

    @property
    def doc_metadata(self) -> DocMetadata:
        """The configs document metadata."""
        return self._doc_metadata

    @doc_metadata.setter
    def doc_metadata(self, doc_metadata: DocMetadata):
        if self._doc_metadata is None:
            self._doc_metadata = doc_metadata
        else:
            msg = "Cannot set doc_metadata as it has already been set."
            _LOGGER.error(msg)

    def to_dict(self, json_serializable: bool = False) -> Dict:
        """
        Serialize the :class:`~yawning_titan.config.network_config.NetworkConfig` as a :py:class:`dict`.

        :param json_serializable: If ``True``, the :attr:`~yawning_titan.config.network_config.NetworkConfig`
            "d numpy array is converted to a list."
        :return: The :class:`~yawning_titan.config.network_config.NetworkConfig` as a :py:class:`dict`.
        """
        config_dict = super().to_dict()
        if json_serializable:
            config_dict["matrix"] = config_dict["matrix"].tolist()
        if self.doc_metadata is not None:
            config_dict["_doc_metadata"] = self.doc_metadata.to_dict()
        return config_dict

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> NetworkConfig:
        """
        Create and return an instance of :class:`~yawning_titan.config.network_config.NetworkConfig`.

        :param config_dict: The network config dict.
        :returns: An instance of :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        cls.validate(config_dict)

        network_config = NetworkConfig(**config_dict)

        return network_config

    @classmethod
    def create_from_args(
        cls,
        matrix: ndarray,
        positions: Dict[str, List[str]],
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
        _doc_metadata: Optional[DocMetadata] = None,
    ):
        """
        Create and return an instance of :class:`~yawning_titan.config.network_config.NetworkConfig`.

        :param matrix: The matrix as a 2D Numpy Array dictating how each node is connected to each other.
        :param positions: Dictionary containing the positions of the nodes in the network (when displayed as a graph).
        :param entry_nodes: List of entry nodes. Has a default value on `None`.
        :param vulnerabilities: Dictionary containing the vulnerabilities of the nodes. Has a default value on `None`.
        :param high_value_nodes: List of high value nodes. Has a default value on `None`.
        :param _doc_metadata: The associated instance of :class:`~yawning_titan.db.doc_metadata.DocMetadata`.

        :returns: An instance of :class:`~yawning_titan.config.network_config.NetworkConfig`.
        """
        args = {
            "matrix": matrix,
            "positions": positions,
            "entry_nodes": entry_nodes,
            "vulnerabilities": vulnerabilities,
            "high_value_nodes": high_value_nodes,
            "_doc_metadata": _doc_metadata,
        }

        return NetworkConfig(**args)

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
