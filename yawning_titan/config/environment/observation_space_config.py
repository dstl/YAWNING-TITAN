from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


@dataclass()
class ObservationSpaceConfig(ConfigGroupABC):
    """
    Class that validates and stores the Observation Space configuration
    """

    obs_compromised_status: bool
    """Is true if the blue agent can see the compromised status of all the nodes"""

    obs_node_vuln_status: bool
    """Is true if the blue agent can see the vulnerability scores of all the nodes"""

    obs_node_connections: bool
    """Is true if blue agent can see what nodes are connected to what other nodes"""

    obs_avg_vuln: bool
    """Is true if the blue agent can see the average vulnerability of all the nodes"""

    obs_graph_connectivity: bool
    """Is true if the blue agent can see a graph connectivity score"""

    obs_attack_sources: bool
    """Is true if the blue agent can see all of the nodes that have recently attacked a safe node"""

    obs_attack_targets: bool
    """Is true if the blue agent can see all the nodes that have recently been attacked"""

    obs_special_nodes: bool
    """Is true if the blue agent can see all of the special nodes (entry nodes, high value nodes)"""

    obs_red_agent_skill: bool
    """Is true if the blue agent can see the skill level of the red agent"""

    @classmethod
    def create(
            cls,
            settings: Dict[str, Any]
    ) -> ObservationSpaceConfig:
        cls._validate(settings)

        observation_space = ObservationSpaceConfig(
            obs_compromised_status=settings[
                "compromised_status"
            ],
            obs_node_vuln_status=settings["vulnerabilities"],
            obs_node_connections=settings["node_connections"],
            obs_avg_vuln=settings["average_vulnerability"],
            obs_graph_connectivity=settings[
                "graph_connectivity"
            ],
            obs_attack_sources=settings["attacking_nodes"],
            obs_attack_targets=settings["attacked_nodes"],
            obs_special_nodes=settings["special_nodes"],
            obs_red_agent_skill=settings["red_agent_skill"]
        )

        return observation_space

    @classmethod
    def _validate(cls, data: dict):
        all_obs = [
            "compromised_status",
            "vulnerabilities",
            "node_connections",
            "average_vulnerability",
            "graph_connectivity",
            "attacking_nodes",
            "attacked_nodes",
            "special_nodes",
            "red_agent_skill",
        ]
        for name in all_obs:
            check_type(data, name, [bool])

        if True not in list(map(lambda x: data[x], all_obs)):
            raise ValueError(
                "At least one option from OBSERVATION_SPACE must be enabled. The observation space must contain at least one item"
            )

