from datetime import datetime
import pytest
import os
import yaml
from typing import Dict,Any,List
from yaml import SafeLoader
from tests import TEST_CONFIG_PATH
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.network_interface import NetworkInterface

@pytest.fixture
def temp_config_from_base(tmpdir_factory)->str:
    """
    Pytest fixture to create temporary config files derived from a base config yaml file.
    """
    def _temp_config_from_base(base_config_path:str,updated_settings:Dict[str,Dict[str,Any]]):
        try:
            with open(base_config_path) as f:
                new_settings:Dict[str,Dict[str,Any]] = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {base_config_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            raise e

        for key,val in updated_settings.items():
            new_settings[key].update(val)
            for _key,_val in val.items():
                print(new_settings[key][_key])

        temp_config_filename = "tmp_config" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".yaml"
        temp_config_path = os.path.join(tmpdir_factory.mktemp("tmp_config"),temp_config_filename)
        
        with open(temp_config_path, 'w') as file:
            yaml.dump(new_settings, file)

        return temp_config_path
    return _temp_config_from_base

@pytest.fixture
def basic_2_agent_loop(temp_config_from_base)->ActionLoop:
    def _basic_2_agent_loop(
        episodes:int=1,
        entry_nodes:List[str]=None,
        high_value_nodes:List[str]=None,
        settings_file:str=None,         
        custom_settings:Dict[str,Dict[str,Any]]=None,        
    )->ActionLoop:
        """
        Use parameterized settings to return a configured ActionLoop
        """
        matrix, node_positions = network_creator.create_18_node_network()


        if settings_file is not None:
            settings_path = os.path.join(TEST_CONFIG_PATH, settings_file)
            if custom_settings is not None:
                settings_path = temp_config_from_base(settings_path,custom_settings)
        

        network_interface = NetworkInterface(matrix, node_positions, entry_nodes=entry_nodes, high_value_nodes=high_value_nodes,settings_path=settings_path)

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
