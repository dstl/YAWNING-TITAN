from __future__ import annotations

from logging import getLogger
from typing import Dict, List, Optional, Union

import numpy as np

from yawning_titan.config.toolbox.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.float_item import (
    FloatItem,
    FloatProperties,
)
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.db.doc_metadata import DocMetadata, DocMetaDataObject
from yawning_titan.exceptions import ConfigGroupValidationError

_LOGGER = getLogger(__name__)

# --- Tier 0 groups


class RandomNodePlacementGroup(ConfigGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
    ):
        self.count = IntItem(
            value=count,
            doc="The number of nodes to place within the network",
            properties=IntProperties(
                allow_null=True, min_val=0, inclusive_min=True, default=0
            ),
        )
        self.use = BoolItem(
            value=use,
            doc="Choose nodes completely randomly",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc)


class NodeVulnerabilityGroup(RestrictRangeGroup):
    """Implementation of :class: `~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` using float values as min and max."""

    def __init__(
        self,
        doc: Optional[str] = None,
        restrict: Optional[bool] = False,
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        node_vulnerabilities: Optional[Dict[str, int]] = None,
    ):
        self.node_vulnerabilities = node_vulnerabilities
        self.restrict = BoolItem(
            value=restrict,
            doc="Whether to restrict this attribute.",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.min: FloatItem = FloatItem(
            value=min,
            doc="The minimum value of the attribute to restrict.",
            properties=FloatProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        self.max: FloatItem = FloatItem(
            value=max,
            doc="The maximum value of the attribute to restrict.",
            properties=FloatProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        self.doc: Optional[str] = doc
        self.validation = self.validate()

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        if self.node_vulnerabilities is None:
            return super().validate()


# --- Tier 1 groups


class RandomEntryNodeGroup(RandomNodePlacementGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        place_close_to_edge: Optional[bool] = False,
        place_close_to_center: Optional[bool] = False,
    ):
        self.place_close_to_edge = BoolItem(
            value=place_close_to_edge,
            doc="Choose nodes closer to the edge of the network.",
            alias="prefer_edge_nodes_for_entry_nodes",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.place_close_to_center = BoolItem(
            value=place_close_to_center,
            doc="Choose nodes closer to the center of the network.",
            alias="prefer_central_nodes_for_entry_nodes",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc, use, count)


class RandomHighValueNodeGroup(RandomNodePlacementGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        place_far_from_entry: Optional[bool] = False,
    ):
        self.place_far_from_entry = BoolItem(
            value=place_far_from_entry,
            doc="Choose nodes far away from entry nodes.",
            alias="choose_high_value_nodes_furthest_away_from_entry",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc, use, count)


# --- Tier 2 groups


class NodeGroup(ConfigGroup):
    """A group of nodes and their associated random placement settings."""

    def __init__(
        self,
        doc: Optional[str] = None,
        nodes: Optional[List[str]] = None,
        random_placement: Optional[
            Union[RandomEntryNodeGroup, RandomHighValueNodeGroup]
        ] = None,
    ):
        self.nodes = nodes
        self.random_placement = random_placement
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()
        try:
            if not self.nodes and not self.random_placement:
                msg = "Nodes must be placed in the network randomly if a set placement is not defined"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
            return self.validation

        if not self.nodes:
            n = sum(
                1 if e.value else 0
                for k, e in self.random_placement.get_config_elements().items()
                if k not in ["use", "count"]
            )
            try:
                if n == 0:
                    msg = "If the user does not set the placement of nodes then a method of setting them randomly must be chosen"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)

            try:
                if n > 1:
                    msg = f"{n} methods of choosing node placement have been selected but only 1 can be used"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation


class Network(ConfigGroup, DocMetaDataObject):
    """A set of optional restrictions that collectively constrain the types of network a game mode can be used upon."""

    def __init__(
        self,
        doc: Optional[str] = None,
        matrix: np.ndarray = None,
        positions: Dict[str, List[str]] = None,
        entry_nodes: Optional[Union[NodeGroup, List[str]]] = None,
        high_value_nodes: Optional[Union[NodeGroup, List[str]]] = None,
        vulnerabilities: Optional[Union[NodeVulnerabilityGroup, Dict[str, int]]] = None,
        _doc_metadata: Optional[DocMetadata] = None,
    ):
        self._doc_metadata = _doc_metadata if _doc_metadata else DocMetadata()
        self.matrix = matrix
        self.positions = positions
        self.vulnerabilities = vulnerabilities

        self.entry_nodes = NodeGroup(
            nodes=entry_nodes,
            random_placement=RandomEntryNodeGroup(
                doc="The pseudo random placement of the entry nodes in the network."
            ),
        )
        self.high_value_nodes = NodeGroup(
            nodes=high_value_nodes,
            random_placement=RandomHighValueNodeGroup(
                doc="The pseudo random placement of the high value nodes in the network."
            ),
        )
        self.vulnerabilities = NodeVulnerabilityGroup(
            node_vulnerabilities=vulnerabilities
        )

        if isinstance(entry_nodes, NodeGroup):
            self.entry_nodes = entry_nodes
        elif isinstance(entry_nodes, dict):
            self.entry_nodes.set_from_dict(entry_nodes)

        if isinstance(high_value_nodes, NodeGroup):
            self.high_value_nodes = high_value_nodes
        elif isinstance(high_value_nodes, dict):
            self.high_value_nodes.set_from_dict(high_value_nodes)

        if isinstance(vulnerabilities, NodeVulnerabilityGroup):
            self.vulnerabilities = vulnerabilities
        elif isinstance(vulnerabilities, dict):
            self.vulnerabilities.set_from_dict(vulnerabilities)

        self.entry_nodes.random_placement.count.alias = "number_of_entry_nodes"
        self.entry_nodes.random_placement.use.alias = "choose_entry_nodes_randomly"

        self.high_value_nodes.random_placement.count.alias = (
            "number_of_high_value_nodes"
        )
        self.high_value_nodes.random_placement.use.alias = (
            "choose_high_value_nodes_placement_at_random"
        )

        self.vulnerabilities.max.alias = "node_vulnerability_upper_bound"
        self.vulnerabilities.min.alias = "node_vulnerability_lower_bound"

        super().__init__(doc)

    def to_dict(
        self,
        json_serializable: bool = False,
        include_none: bool = True,
        values_only: bool = False,
    ) -> dict:
        """
        Serialize the :class:`~yawning_titan.networks.network.Network` as a :class:`dict`.

        :param json_serializable: If ``True``, the :attr:`~yawning_titan.networks.network.Network`
            "d numpy array is converted to a list."
        :param include_none: Determines whether to include empty fields in the dict. Has a default
            value of ``True``.
        :return: The :class:`~yawning_titan.networks.network.Network` as a :class:`dict`.
        """
        if json_serializable:
            values_only = True

        config_dict = super().to_dict(
            values_only=values_only, include_none=include_none
        )

        config_dict["matrix"] = self.matrix
        config_dict["positions"] = self.positions
        config_dict["entry_nodes"]["nodes"] = self.entry_nodes.nodes
        config_dict["high_value_nodes"]["nodes"] = self.high_value_nodes.nodes
        config_dict["vulnerabilities"][
            "node_vulnerabilities"
        ] = self.vulnerabilities.node_vulnerabilities

        if json_serializable:
            config_dict["matrix"] = config_dict["matrix"].tolist()
            if self.doc_metadata is not None:
                config_dict["_doc_metadata"] = self.doc_metadata.to_dict(
                    include_none=True
                )

        return config_dict

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, other) -> bool:
        """Check the equality of any 2 instances of class.

        :param other: Another potential instance of the class to be compared against.

        :return: A boolean True if the elements holds the same data otherwise False.
        """
        if isinstance(other, self.__class__):
            return (hash(self) == hash(other)) and np.array_equal(
                self.matrix, other.matrix
            )
        return False
