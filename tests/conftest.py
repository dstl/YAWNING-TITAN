import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pytest
import yaml
from yaml import SafeLoader

from yawning_titan.config.game_config.game_mode import GameMode
from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.networks import network_creator
from yawning_titan.networks.network import Network
from yawning_titan.yawning_titan_run import YawningTitanRun


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


@pytest.fixture
def init_test_run():
    """Return a `YawningTitanRun`."""

    def _init_test_run(
        settings_path: str,
        adj_matrix: np.array,
        positions,
        entry_nodes: List[str],
        high_value_nodes: List[str],
    ) -> YawningTitanRun:
        """
        Generate the test GenericEnv() and number of actions for the blue agent.

        Args:
            settings_path: A path to the environment settings file
            adj_matrix: the adjacency matrix used for the network to defend.
            positions: x and y co-ordinates to plot the graph in 2D space
            entry_nodes: list of strings that dictate which nodes are entry nodes
            high_value_nodes: list of strings that dictate which nodes are high value nodes

        Returns:
            env: An OpenAI gym environment
        """
        with open(settings_path) as f:
            config_dict = yaml.safe_load(f)

        network = Network(
            matrix=adj_matrix,
            positions=positions,
            entry_nodes=entry_nodes,
            high_value_nodes=high_value_nodes,
        )
        network.set_from_dict(config_dict["GAME_RULES"], legacy=True)

        game_mode = GameMode()
        game_mode.set_from_dict(config_dict, legacy=True)

        yt_run = YawningTitanRun(
            network=network,
            game_mode=game_mode,
            collect_additional_per_ts_data=True,
            auto=False,
            total_timesteps=1000,
            eval_freq=1000,
        )
        yt_run.setup()
        return yt_run

    return _init_test_run


@pytest.fixture
def generate_generic_env_test_run(init_test_run):
    """Return a `GenericNetworkEnv`."""

    def _generate_generic_env_test_run(
        settings_path: Optional[str] = default_game_mode_path(),
        net_creator_type="mesh",
        n_nodes: int = 10,
        connectivity: float = 0.7,
        entry_nodes=None,
        high_value_nodes=None,
        env_only: bool = True,
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

        yt_run: YawningTitanRun = init_test_run(
            settings_path, adj_matrix, node_positions, entry_nodes, high_value_nodes
        )
        if env_only:
            return yt_run.env

        yt_run.train()
        yt_run.evaluate()
        return yt_run

    return _generate_generic_env_test_run


@pytest.fixture
def basic_2_agent_loop(
    generate_generic_env_test_run, temp_config_from_base
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

        yt_run: YawningTitanRun = generate_generic_env_test_run(
            settings_path=settings_path,
            net_creator_type="18node",
            entry_nodes=entry_nodes,
            high_value_nodes=high_value_nodes,
            env_only=False,
        )

        return ActionLoop(yt_run.env, yt_run.agent, episode_count=num_episodes)

    return _basic_2_agent_loop
