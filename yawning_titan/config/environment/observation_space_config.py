from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


@dataclass()
class ObservationSpaceConfig(ConfigABC):
    """Class that validates and stores the Observation Space configuration."""

    _compromised_status: bool
    _vulnerabilities: bool
    _node_connections: bool
    _average_vulnerability: bool
    _graph_connectivity: bool
    _attacking_nodes: bool
    _attacked_nodes: bool
    _special_nodes: bool
    _red_agent_skill: bool

    # region Getters
    @property
    def compromised_status(self) -> bool:
        """The blue agent can see the compromised status of all the nodes."""
        return self._compromised_status

    @property
    def vulnerabilities(self) -> bool:
        """The blue agent can see the vulnerability scores of all the nodes."""
        return self._vulnerabilities

    @property
    def node_connections(self) -> bool:
        """The blue agent can see what nodes are connected to what other nodes."""
        return self._node_connections

    @property
    def average_vulnerability(self) -> bool:
        """The blue agent can see the average vulnerability of all the nodes."""
        return self._average_vulnerability

    @property
    def graph_connectivity(self) -> bool:
        """The blue agent can see a graph connectivity score."""
        return self._graph_connectivity

    @property
    def attacking_nodes(self) -> bool:
        """The blue agent can see all the nodes that have recently attacked a safe node."""
        return self._attacking_nodes

    @property
    def attacked_nodes(self) -> bool:
        """The blue agent can see all the nodes that have recently been attacked."""
        return self._attacked_nodes

    @property
    def special_nodes(self) -> bool:
        """The blue agent can see all the special nodes (entry nodes,high value nodes)."""
        return self._special_nodes

    @property
    def red_agent_skill(self) -> bool:
        """The blue agent can see the skill level of the red agent."""
        return self._red_agent_skill

    # endregion

    # region Setters
    @compromised_status.setter
    def compromised_status(self, value):
        self._compromised_status = value

    @vulnerabilities.setter
    def vulnerabilities(self, value):
        self._vulnerabilities = value

    @node_connections.setter
    def node_connections(self, value):
        self._node_connections = value

    @average_vulnerability.setter
    def average_vulnerability(self, value):
        self._average_vulnerability = value

    @graph_connectivity.setter
    def graph_connectivity(self, value):
        self._graph_connectivity = value

    @attacking_nodes.setter
    def attacking_nodes(self, value):
        self._attacking_nodes = value

    @attacked_nodes.setter
    def attacked_nodes(self, value):
        self._attacked_nodes = value

    @special_nodes.setter
    def special_nodes(self, value):
        self._special_nodes = value

    @red_agent_skill.setter
    def red_agent_skill(self, value):
        self._red_agent_skill = value

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> ObservationSpaceConfig:
        """
        Creates an instance of `ObservationSpaceConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        cls.validate(config_dict)

        observation_space_config = ObservationSpaceConfig(
            _compromised_status=config_dict["compromised_status"],
            _vulnerabilities=config_dict["vulnerabilities"],
            _node_connections=config_dict["node_connections"],
            _average_vulnerability=config_dict["average_vulnerability"],
            _graph_connectivity=config_dict["graph_connectivity"],
            _attacking_nodes=config_dict["attacking_nodes"],
            _attacked_nodes=config_dict["attacked_nodes"],
            _special_nodes=config_dict["special_nodes"],
            _red_agent_skill=config_dict["red_agent_skill"],
        )

        return observation_space_config

    @classmethod
    def validate(cls, config_dict: dict):
        """
        Validates the bservation space config dict.

        :param: config_dict: A config dict with the required key/values pairs.
        """
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
            check_type(config_dict, name, [bool])

        if True not in list(map(lambda x: config_dict[x], all_obs)):
            raise ValueError(
                "At least one option from OBSERVATION_SPACE must be enabled. The observation space must contain at "
                "least one item "
            )
