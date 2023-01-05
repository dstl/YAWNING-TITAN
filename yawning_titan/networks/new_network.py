from __future__ import annotations

from typing import Optional

from yawning_titan.config.toolbox.core import ConfigGroup
from typing import Dict, List, Optional
from logging import getLogger
from numpy import ndarray

from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup

_LOGGER = getLogger(__name__)

# --- Tier 0 groups

class NodePlacementGroup(ConfigGroup):
    """The pseudo random placement of the nodes in the network"""

    def __init__(
        self, 
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        random: Optional[bool] = False,
        place_close_to_edge: Optional[bool] = False,
        place_close_to_center: Optional[bool] = False
    ):
        self.use = BoolItem(
            value=use,
            doc="Whether to place the node type randomly",
            properties=BoolProperties(allow_null=False,default=False)
        )
        self.count = IntItem(
            value=count,
            doc="The number of nodes to place within the network",
            properties=IntProperties(allow_null=True, min_val=0, inclusive_min=True, default=0)
        )
        self.random = BoolItem(
            value=random,
            doc="Choose nodes completely randomly.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        self.place_close_to_edge = BoolItem(
            value=place_close_to_edge,
            doc="Choose nodes closer to the edge of the network.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        self.place_close_to_center = BoolItem(
            value=place_close_to_center,
            doc="Choose nodes closer to the center of the network.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        super().__init__(doc)

# --- Tier 1 groups

class EntryNodePlacementGroup(ConfigGroup):
    """The pseudo random placement of the nodes in the network"""

    def __init__(
        self, 
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        random: Optional[bool] = False,
        place_close_to_edge: Optional[bool] = False,
        place_close_to_center: Optional[bool] = False
    ):
        self.use = BoolItem(
            value=use,
            doc="Whether to place the node type randomly",
            properties=BoolProperties(allow_null=False,default=False)
        )
        self.count = IntItem(
            value=count,
            doc="The number of nodes to place within the network",
            properties=IntProperties(allow_null=True, min_val=0, inclusive_min=True, default=0)
        )
        self.random = BoolItem(
            value=random,
            doc="Choose nodes completely randomly.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        self.place_close_to_edge = BoolItem(
            value=place_close_to_edge,
            doc="Choose nodes closer to the edge of the network.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        self.place_close_to_center = BoolItem(
            value=place_close_to_center,
            doc="Choose nodes closer to the center of the network.",
            properties=BoolProperties(allow_null=True,default=False)
        )
        super().__init__(doc)

# --- Tier 2 groups

class Network(ConfigGroup):
    """A set of optional restrictions that collectively constrain the types of network a game mode can be used upon."""

    def __init__(
        self, 
        doc: Optional[str] = None,
        matrix: ndarray = None,
        positions: Dict[str, List[str]] = None,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
        _doc_metadata: Optional[DocMetadata] = None,
        entry_node_random_placement: Optional[NodePlacementGroup] = None,
        high_value_node_random_placement: Optional[NodePlacementGroup] = None,
        node_vulnerabilities: Optional[RestrictRangeGroup] = None
    ):
        self._doc_metadata = _doc_metadata
        self.matrix = matrix
        self.positions = positions
        self.entry_nodes = entry_nodes
        self.vulnerabilities = vulnerabilities
        self.high_value_nodes = high_value_nodes
        self.entry_node_random_placement = entry_node_random_placement if entry_node_random_placement else NodePlacementGroup(
            doc="The pseudo random placement of the entry nodes in the network."
        )
        self.high_value_node_random_placement = high_value_node_random_placement if high_value_node_random_placement else NodePlacementGroup(
            doc="The pseudo random placement of the high value nodes in the network."
        )
        self.node_vulnerabilities = node_vulnerabilities if node_vulnerabilities else RestrictRangeGroup(
            doc="The range of vulnerabilities for the nodes in the network used when vulnerability is set randomly."
        )
        super().__init__(doc)

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

    def to_dict(
        self, json_serializable: bool = False, include_none: bool = True
    ) -> Dict:
        """
        Serialize the :class:`~yawning_titan.networks.network.Network` as a :py:class:`dict`.

        :param json_serializable: If ``True``, the :attr:`~yawning_titan.networks.network.Network`
            "d numpy array is converted to a list."
        :param include_none: Determines whether to include empty fields in the dict. Has a default
            value of ``True``.
        :return: The :class:`~yawning_titan.networks.network.Network` as a :py:class:`dict`.
        """
        config_dict = super().to_dict(include_none=include_none)
        if json_serializable:
            config_dict["matrix"] = config_dict["matrix"].tolist()
        if self.doc_metadata is not None:
            config_dict["_doc_metadata"] = self.doc_metadata.to_dict()
        return config_dict
