import os
from datetime import datetime
from typing import Any, Dict, Optional

import pytest
import yaml
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from yaml import SafeLoader

from yawning_titan.config.game_config.game_mode import GameMode
from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.networks import network_creator


@pytest.fixture
def temp_config_from_base(tmpdir_factory) -> str:
    """Pytest fixture to create temporary config files derived from a base config yaml file."""

    def _temp_config_from_base(
        base_config_path: str, updated_settings: Dict[str, Dict[str, Any]]
    ):
        try:
            with open(base_config_path) as f:
                new_settings: Dict[str, Dict[str, Any]] = yaml.load(
                    f, Loader=SafeLoader
                )
        except FileNotFoundError as e:
            msg = f"Configuration file does not exist: {base_config_path}"
            print(msg)  # TODO: Remove once proper logging is setup
            raise e

        for key, val in updated_settings.items():
            new_settings[key].update(val)

        temp_config_filename = (
            "tmp_config" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".yaml"
        )
        temp_config_path = os.path.join(
            tmpdir_factory.mktemp("tmp_config"), temp_config_filename
        )

        with open(temp_config_path, "w") as file:
            yaml.dump(new_settings, file)

        return temp_config_path

    return _temp_config_from_base


@pytest.fixture(scope="session")
def generate_generic_env_test_reqs():
    """Return a `GenericNetworkEnv`."""

    def _generate_generic_env_test_reqs(
        settings_path: Optional[str] = default_game_mode_path(),
        net_creator_type="mesh",
        n_nodes: int = 10,
        connectivity: float = 0.7,
        entry_nodes=None,
        high_value_nodes=None,
    ) -> GenericNetworkEnv:
        """
        Generate test environment requirements.

        Args:
            settings_path: A path to the environment settings file
            net_creator_type: The type of net creator to use to generate the underlying network
            n_nodes: The number of nodes to create within the network
            connectivity: The connectivity value for the mesh net creator (Only required for mesh network creator type)
            entry_nodes: list of strings that dictate which nodes are entry nodes
            high_value_nodes: list of strings that dictate which nodes are high value nodes

        Returns:
            env: An OpenAI gym environment

        """
        valid_net_creator_types = ["18node", "mesh"]
        with open(settings_path) as f:
            config_dict = yaml.safe_load(f)

        game_mode = GameMode.create(dict=config_dict, legacy=True, raise_errors=True)

        if net_creator_type not in valid_net_creator_types:
            raise ValueError(
                f"net_creator_type is {net_creator_type}, Must be 18_node or mesh"
            )

        if net_creator_type == "18node":
            adj_matrix, node_positions = network_creator.get_18_node_network_mesh()

        elif net_creator_type == "mesh":
            adj_matrix, node_positions = network_creator.create_mesh(
                size=n_nodes, connectivity=connectivity
            )
        network = network_creator.create_network(
            config_dict=config_dict,
            adj_matrix=adj_matrix,
            positions=node_positions,
            entry_node_names=entry_nodes,
            high_value_node_names=high_value_nodes,
            legacy=True,
        )

        # TODO: update the following temp setter for vulnerability range

        network_interface = NetworkInterface(game_mode=game_mode, network=network)

        red = RedInterface(network_interface)
        blue = BlueInterface(network_interface)

        env = GenericNetworkEnv(red, blue, network_interface)

        check_env(env, warn=False)
        env.reset()

        return env

    return _generate_generic_env_test_reqs


@pytest.fixture
def basic_2_agent_loop(
    generate_generic_env_test_reqs, temp_config_from_base
) -> ActionLoop:
    """Return a basic 2-agent `ActionLoop`."""

    def _basic_2_agent_loop(
        settings_path: Optional[str] = default_game_mode_path(),
        entry_nodes=None,
        high_value_nodes=None,
        num_episodes=1,
        custom_settings=None,
    ) -> ActionLoop:
        """Use parameterized settings to return a configured ActionLoop."""
        if custom_settings is not None:
            settings_path = temp_config_from_base(settings_path, custom_settings)

        env: GenericNetworkEnv = generate_generic_env_test_reqs(
            settings_path=settings_path,
            net_creator_type="18node",
            entry_nodes=entry_nodes,
            high_value_nodes=high_value_nodes,
        )

        eval_callback = EvalCallback(
            Monitor(env), eval_freq=1000, deterministic=False, render=False
        )

        agent = PPO(
            PPOMlp, env, verbose=1, seed=env.network_interface.random_seed
        )  # TODO: allow PPO to inherit environment random_seed. Monkey patch additional feature?

        agent.learn(total_timesteps=1000, n_eval_episodes=100, callback=eval_callback)

        return ActionLoop(env, agent, episode_count=num_episodes)

    return _basic_2_agent_loop
