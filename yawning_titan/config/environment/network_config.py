from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np


from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type,check_within_range


@dataclass
class NetworkConfig(ConfigGroupABC):
    """
    Class that validates and stores Game Rules Configuration
    """

    high_value_targets: List[str]
    entry_nodes: List[str]
    vulnerabilities: List[Dict] 
    matrix: np.array = None
    #network_topology: str

    @classmethod
    def create(cls, settings: Dict[str, Any]):
        cls._validate(settings)
        network_settings = NetworkConfig(
            high_value_targets = settings["high_value_targets"],
            entry_nodes = settings["entry_nodes"],
            vulnerabilities= settings["vulnerabilities"],
            #network_topology = settings["network_topology"]
        )

        return network_settings

    @classmethod
    def _validate(cls, data: dict):
       #TODO: add validation of network topology file availability
       check_type(data,"high_value_targets",[list,None])
       check_type(data,"entry_nodes",[list,None])
       check_type(data,"vulnerabilities",[Dict,None])