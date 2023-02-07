import os
import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional

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
from yawning_titan.networks.network import (
    Network,
    RandomEntryNodePreference,
    RandomHighValueNodePreference,
)
from yawning_titan.networks.network_db import default_18_node_network


@pytest.fixture(scope="session")
def create_test_network() -> Network:
    """Create an instance of :class: `~yawning_titan.networks.network.Network` from a dictionary.

    If the dictionary is in legacy format then perform preprocessing, otherwise utilise the :method:
    `~yawning_titan.networks.network.Network.create` method.
    """

    def _create_test_network(
        legacy_config_dict: Dict[str, Any],
        n_nodes: int = 18,
        connectivity: float = 0.7,
        vulnerabilities: Optional[Dict[str, float]] = None,
        high_value_node_names: Optional[List[str]] = None,
        entry_node_names: Optional[List[str]] = None,
    ) -> Network:
        adj_matrix, positions = network_creator.get_mesh_matrix_and_positions(
            size=n_nodes, connectivity=connectivity
        )
        set_random_vulnerabilities = False

        entry_node_placement_preference = RandomEntryNodePreference.NONE
        if legacy_config_dict["GAME_RULES"]["prefer_central_nodes_for_entry_nodes"]:
            entry_node_placement_preference = RandomEntryNodePreference.CENTRAL
        elif legacy_config_dict["GAME_RULES"]["prefer_edge_nodes_for_entry_nodes"]:
            entry_node_placement_preference = RandomEntryNodePreference.EDGE

        high_value_node_placement_preference = RandomHighValueNodePreference.NONE
        if legacy_config_dict["GAME_RULES"][
            "choose_high_value_nodes_furthest_away_from_entry"
        ]:
            high_value_node_placement_preference = (
                RandomHighValueNodePreference.FURTHEST_AWAY_FROM_ENTRY
            )

        if vulnerabilities is None:
            set_random_vulnerabilities = True

        network = network_creator.get_network_from_matrix_and_positions(
            adj_matrix=adj_matrix, positions=positions
        )

        network.set_random_vulnerabilities = set_random_vulnerabilities
        network.set_random_entry_nodes = legacy_config_dict["GAME_RULES"][
            "choose_entry_nodes_randomly"
        ]
        network.random_entry_node_preference = entry_node_placement_preference
        network.num_of_random_entry_nodes = legacy_config_dict["GAME_RULES"][
            "number_of_entry_nodes"
        ]
        network.set_random_high_value_nodes = legacy_config_dict["GAME_RULES"][
            "choose_high_value_nodes_placement_at_random"
        ]
        network.random_high_value_node_preference = high_value_node_placement_preference
        network.num_of_random_high_value_nodes = legacy_config_dict["GAME_RULES"][
            "number_of_high_value_nodes"
        ]
        network.node_vulnerability_lower_bound = legacy_config_dict["GAME_RULES"][
            "node_vulnerability_lower_bound"
        ]
        network.node_vulnerability_upper_bound = legacy_config_dict["GAME_RULES"][
            "node_vulnerability_upper_bound"
        ]

        # Entry nodes must be set before high value nodes
        if entry_node_names is None:
            network.reset_random_entry_nodes()
        else:
            if any(
                legacy_config_dict["GAME_RULES"][x]
                for x in [
                    "choose_entry_nodes_randomly",
                    "prefer_edge_nodes_for_entry_nodes",
                    "prefer_central_nodes_for_entry_nodes",
                ]
            ):
                warnings.warn(
                    UserWarning(
                        "High value node names have been specified therefore settings for random high value nodes will be ignored."
                    )
                )
            for node_name in entry_node_names:
                node = network.get_node_from_name(node_name)
                node.entry_node = True
                network._check_intersect(node)

        if high_value_node_names is None:
            network.reset_random_high_value_nodes()
        else:
            if any(
                legacy_config_dict["GAME_RULES"][x]
                for x in [
                    "choose_high_value_nodes_placement_at_random",
                    "choose_high_value_nodes_furthest_away_from_entry",
                ]
            ):
                warnings.warn(
                    UserWarning(
                        "High value node names have been specified therefore settings for random high value nodes will be ignored."
                    )
                )
            for node_name in high_value_node_names:
                node = network.get_node_from_name(node_name)
                node.high_value_node = True
                network._check_intersect(node)

        if network.set_random_vulnerabilities:
            network.reset_random_vulnerabilities()
        else:
            for node in network.nodes:
                node.vulnerability = vulnerabilities[node.name]

        return network

    return _create_test_network


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
def generate_generic_env_test_reqs(create_test_network):
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
            network = default_18_node_network()

        elif net_creator_type == "mesh":

            network = create_test_network(
                legacy_config_dict=config_dict,
                n_nodes=n_nodes,
                connectivity=connectivity,
                entry_node_names=entry_nodes,
                high_value_node_names=high_value_nodes,
            )

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
