from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np

from yawning_titan.config.config_group_class import ConfigGroupABC,set_prop
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type,check_within_range


@dataclass
class NetworkConfig(ConfigGroupABC):
    """
    Class that validates and stores Game Rules Configuration
    """

    high_value_targets: List[str] = set_prop("high_value_targets","A name of a node that when taken means the red agent instantly wins")
    #"""A name of a node that when taken means the red agent instantly wins"""

    entry_nodes: List[str] = set_prop("entry_nodes","A list of nodes that act as gateways or doors in the network for the red agent. While the red")
    #"""A list of nodes that act as gateways or doors in the network for the red agent. While the red"""

    vulnerabilities: List[Dict] = set_prop("vulnerabilities","A dictionary containing the vulnerabilities of the nodes")
    #"""A dictionary containing the vulnerabilities of the nodes"""

    matrix: np.array = set_prop("matrix","An adjacency matrix containing the connections between nodes in the network")
    #"""An adjacency matrix containing the connections between nodes in the network"""

    positions: dict = set_prop("matrix","A dictionary containing the positions of the nodes in the network (when displayed as a graph")
    #"""A dictionary containing the positions of the nodes in the network (when displayed as a graph)"""


    #topology: str

    @classmethod
    def create(cls, settings: Dict[str, Any]):
        cls._validate(settings)
        network_settings = NetworkConfig(
            high_value_targets = settings["high_value_targets"],
            entry_nodes = settings["entry_nodes"],
            vulnerabilities= settings["vulnerabilities"],
            matrix=settings["matrix"],
            positions=settings["positions"]
            #topology = settings["network_topology"]
        )

        return network_settings

    @classmethod
    def _validate(cls, data: dict):
       #TODO: add validation of network topology file availability
       check_type(data,"high_value_targets",[list,None])
       check_type(data,"entry_nodes",[list,None])
       check_type(data,"vulnerabilities",[Dict,None])