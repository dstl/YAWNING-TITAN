import pytest
import numpy as np
from typing import Dict, List, Optional


from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.network_config.network_config import NetworkConfig
from stable_baselines3.common.env_checker import check_env

@pytest.fixture
def init_test_env():
    def _init_test_env(
        settings_path: str,
        adj_matrix: np.array,
        positions,
        entry_nodes: List[str],
        high_value_targets: List[str],
    ) -> GenericNetworkEnv:
        """
        Generate the test GenericEnv() and number of actions for the blue agent.

        Args:
            settings_path: A path to the environment settings file
            adj_matrix: the adjacency matrix used for the network to defend.
            positions: x and y co-ordinates to plot the graph in 2D space
            entry_nodes: list of strings that dictate which nodes are entry nodes
            high_value_targets: list of strings that dictate which nodes are high value targets

        Returns:
            env: An OpenAI gym environment
        """
        if not entry_nodes:
            entry_nodes = ["0", "1", "2"]

        network = NetworkConfig.create(            
            high_value_targets=high_value_targets,
            entry_nodes=entry_nodes,
            vulnerabilities=None,
            matrix=adj_matrix,
            positions=positions            
        )

        game_mode = GameModeConfig.create_from_yaml(settings_path)

        network_interface = NetworkInterface(game_mode=game_mode,network=network)

        red = RedInterface(network_interface)
        blue = BlueInterface(network_interface)

        env = GenericNetworkEnv(red, blue, network_interface)

        check_env(env, warn=True)
        env.reset()

        return env
    return _init_test_env

@pytest.fixture
def generate_generic_env_test_reqs(init_test_env):
    def _generate_generic_env_test_reqs(
        settings_file_path: Optional[str]=default_game_mode_path(),
        net_creator_type="mesh",
        n_nodes: int = 10,
        connectivity: float = 0.7,
        entry_nodes=None,
        high_value_targets=None
    ) -> GenericNetworkEnv:
        """
        Generate test environment requirements.

        Args:
            settings_file_path: A path to the environment settings file
            net_creator_type: The type of net creator to use to generate the underlying network
            n_nodes: The number of nodes to create within the network
            connectivity: The connectivity value for the mesh net creator (Only required for mesh network creator type)
            entry_nodes: list of strings that dictate which nodes are entry nodes
            high_value_targets: list of strings that dictate which nodes are high value targets

        Returns:
            env: An OpenAI gym environment

        """
        valid_net_creator_types = ["18node", "mesh"]
        if net_creator_type not in valid_net_creator_types:
            raise ValueError(
                f"net_creator_type is {net_creator_type}, Must be 18_node or mesh"
            )

        if net_creator_type == "18node":
            adj_matrix, node_positions = network_creator.create_18_node_network()
        if net_creator_type == "mesh":
            adj_matrix, node_positions = network_creator.create_mesh(
                size=n_nodes, connectivity=connectivity
            )

        env = init_test_env(
            settings_file_path, adj_matrix, node_positions, entry_nodes, high_value_targets
        )

        return env
    return _generate_generic_env_test_reqs