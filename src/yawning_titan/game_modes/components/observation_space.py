from __future__ import annotations

from typing import Optional

from yawning_titan.config.groups.validation import AnyTrueGroup
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties

# --- Tier 0 groups


class ObservationSpace(AnyTrueGroup):
    """The characteristics of the network and the red agent that the blue agent can observe."""

    def __init__(
        self,
        compromised_status: Optional[bool] = False,
        vulnerabilities: Optional[bool] = False,
        node_connections: Optional[bool] = False,
        average_vulnerability: Optional[bool] = False,
        graph_connectivity: Optional[bool] = False,
        attacking_nodes: Optional[bool] = False,
        attacked_nodes: Optional[bool] = False,
        special_nodes: Optional[bool] = False,
        red_agent_skill: Optional[bool] = False,
    ):
        doc = "The characteristics of the network and the red agent that the blue agent can observe"
        self.compromised_status = BoolItem(
            value=compromised_status,
            doc="The blue agent can see the compromised status of all the nodes",
            properties=BoolProperties(allow_null=True, default=False),
            alias="compromised_status",
        )
        self.vulnerabilities = BoolItem(
            value=vulnerabilities,
            doc="The blue agent can see the vulnerability scores of all the nodes",
            properties=BoolProperties(allow_null=True, default=False),
            alias="vulnerabilities",
        )
        self.node_connections = BoolItem(
            value=node_connections,
            doc="The blue agent can see what nodes are connected to what other nodes",
            properties=BoolProperties(allow_null=True, default=False),
            alias="node_connections",
        )
        self.average_vulnerability = BoolItem(
            value=average_vulnerability,
            doc="The blue agent can see the average vulnerability of all the nodes",
            properties=BoolProperties(allow_null=True, default=False),
            alias="average_vulnerability",
        )
        self.graph_connectivity = BoolItem(
            value=graph_connectivity,
            doc="The blue agent can see a graph connectivity score",
            properties=BoolProperties(allow_null=True, default=False),
            alias="graph_connectivity",
        )
        self.attacking_nodes = BoolItem(
            value=attacking_nodes,
            doc="The blue agent can see all of the nodes that have recently attacked a safe node",
            properties=BoolProperties(allow_null=True, default=False),
            alias="attacking_nodes",
        )
        self.attacked_nodes = BoolItem(
            value=attacked_nodes,
            doc="The blue agent can see all the nodes that have recently been attacked",
            properties=BoolProperties(allow_null=True, default=False),
            alias="attacked_nodes",
        )
        self.special_nodes = BoolItem(
            value=special_nodes,
            doc="The blue agent can see all of the special nodes (entry nodes, high value nodes)",
            properties=BoolProperties(allow_null=True, default=False),
            alias="special_nodes",
        )
        self.red_agent_skill = BoolItem(
            value=red_agent_skill,
            doc="The blue agent can see the skill level of the red agent",
            properties=BoolProperties(allow_null=True, default=False),
            alias="red_agent_skill",
        )
        super().__init__(doc)
