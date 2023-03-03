import os
import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional, Final
from unittest.mock import patch

import pytest
import yaml
from yaml import SafeLoader

from tests import TEST_PACKAGE_DATA_PATH
from tests.mock_and_patch.game_mode_db_patch import game_mode_db_init_patch
from tests.mock_and_patch.network_db_patch import network_db_init_patch
from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks import network_creator
from yawning_titan.networks.network import (
    Network,
    RandomEntryNodePreference,
    RandomHighValueNodePreference,
)
from yawning_titan.networks.network_db import default_18_node_network, \
    NetworkDB
from yawning_titan.networks.node import Node
from yawning_titan.yawning_titan_run import YawningTitanRun

TOLERANCE: Final[float] = 0.1
N_TIME_STEPS: Final[int] = 1000
N_TIME_STEPS_LONG: Final[int] = 10000


@pytest.fixture(scope="session")
def game_mode_db() -> GameModeDB:
    """A patched GameModeDB that uses tests/_package_data/game_modes.json."""
    with patch.object(GameModeDB, "__init__", game_mode_db_init_patch):
        return GameModeDB()


@pytest.fixture(scope="session")
def network_db() -> NetworkDB:
    """A patched NetworkDB that uses tests/_package_data/networks.json."""
    with patch.object(NetworkDB, "__init__", network_db_init_patch):
        return NetworkDB()


@pytest.fixture
def default_game_mode(game_mode_db) -> GameMode:
    """Create a game mode instance using the default config."""
    game_mode = game_mode_db.search(DocMetadataSchema.NAME == "base_config")[0]
    return game_mode


@pytest.fixture()
def corporate_network() -> Network:
    """An example network with components akin to that of a basic corporate network."""
    router_1 = Node()
    switch_1 = Node()
    switch_2 = Node()
    pc_1 = Node()
    pc_2 = Node()
    pc_3 = Node()
    pc_4 = Node()
    pc_5 = Node()
    pc_6 = Node()
    server_1 = Node()
    server_2 = Node()
    network = Network(
        set_random_entry_nodes=True,
        num_of_random_entry_nodes=3,
        set_random_high_value_nodes=True,
        num_of_random_high_value_nodes=3,
        set_random_vulnerabilities=True,
    )
    network.add_node(router_1)
    network.add_node(switch_1)
    network.add_node(switch_2)
    network.add_node(pc_1)
    network.add_node(pc_2)
    network.add_node(pc_3)
    network.add_node(pc_4)
    network.add_node(pc_5)
    network.add_node(pc_6)
    network.add_node(server_1)
    network.add_node(server_2)
    network.add_edge(router_1, switch_1)
    network.add_edge(switch_1, server_1)
    network.add_edge(switch_1, pc_1)
    network.add_edge(switch_1, pc_2)
    network.add_edge(switch_1, pc_3)
    network.add_edge(router_1, switch_2)
    network.add_edge(switch_2, server_2)
    network.add_edge(switch_2, pc_4)
    network.add_edge(switch_2, pc_5)
    network.add_edge(switch_2, pc_6)
    network.reset_random_entry_nodes()
    network.reset_random_high_value_nodes()
    network.reset_random_vulnerabilities()
    network.set_node_positions()
    return network


@pytest.fixture()
def legacy_default_game_mode_dict() -> Dict:
    """
    The legacy default game mode yaml file.

    :returns: The path to the legacy_default_game_mode.yaml as an instance of
        pathlib.Path.
    """
    filepath = TEST_PACKAGE_DATA_PATH / "legacy_default_game_mode.yaml"
    with open(filepath, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="function")
def create_yawning_titan_run(network_db, game_mode_db):
    def _create_yawning_titan_run(
            game_mode_name: str,
            network_name: str,
            timesteps: int = 1000,
            eval_freq: int = 1000,
            deterministic: bool = False
    ) -> YawningTitanRun:
        network = network_db.search(DocMetadataSchema.NAME == network_name)[0]
        game_mode = \
            game_mode_db.search(DocMetadataSchema.NAME == game_mode_name)[0]

        yt_run = YawningTitanRun(
            network=network,
            game_mode=game_mode,
            collect_additional_per_ts_data=True,
            auto=False,
            total_timesteps=timesteps,
            eval_freq=eval_freq,
            deterministic=deterministic
        )

        yt_run.setup()

        return yt_run

    return _create_yawning_titan_run


@pytest.fixture(scope="session")
def create_test_network():
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
        set_random_vulnerabilities = False

        entry_node_placement_preference = RandomEntryNodePreference.NONE
        if legacy_config_dict["GAME_RULES"][
            "prefer_central_nodes_for_entry_nodes"]:
            entry_node_placement_preference = RandomEntryNodePreference.CENTRAL
        elif legacy_config_dict["GAME_RULES"][
            "prefer_edge_nodes_for_entry_nodes"]:
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

        network = network_creator.create_mesh(size=n_nodes,
                                              connectivity=connectivity)

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
        network.num_of_random_high_value_nodes = \
            legacy_config_dict["GAME_RULES"][
                "number_of_high_value_nodes"
            ]
        network.node_vulnerability_lower_bound = \
            legacy_config_dict["GAME_RULES"][
                "node_vulnerability_lower_bound"
            ]
        network.node_vulnerability_upper_bound = \
            legacy_config_dict["GAME_RULES"][
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
                "tmp_config" + datetime.now().strftime(
            "%Y%m%d_%H%M%S") + ".yaml"
        )
        temp_config_path = os.path.join(
            tmpdir_factory.mktemp("tmp_config"), temp_config_filename
        )

        with open(temp_config_path, "w") as file:
            yaml.dump(new_settings, file)

        return temp_config_path

    return _temp_config_from_base


@pytest.fixture(scope="session")
def generate_generic_env_test_run(create_test_network):
    """Return a `GenericNetworkEnv`."""

    def _generate_generic_env_test_run(
            settings_path: Optional[str] = legacy_default_game_mode_path(),
            net_creator_type="mesh",
            n_nodes: int = 10,
            connectivity: float = 0.7,
            entry_node_names=None,
            high_value_node_names=None,
            env_only: bool = True,
            raise_errors: bool = True,
            deterministic: bool = False,
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
        with open(settings_path) as f:
            config_dict = yaml.safe_load(f)

        game_mode = GameMode()
        game_mode.set_from_dict(config_dict, legacy=True)

        valid_net_creator_types = ["18node", "mesh"]
        with open(settings_path) as f:
            config_dict = yaml.safe_load(f)

        game_mode = GameMode.create(
            dict=config_dict, legacy=True, raise_errors=raise_errors
        )

        if net_creator_type not in valid_net_creator_types:
            raise ValueError(
                f"net_creator_type is {net_creator_type}, Must be 18_node or mesh"
            )

        if net_creator_type == "18node":
            network = default_18_node_network()
            if entry_node_names:
                network.set_entry_nodes(names=entry_node_names)
            if high_value_node_names:
                network.set_high_value_nodes(names=high_value_node_names)

        elif net_creator_type == "mesh":
            network = create_test_network(
                legacy_config_dict=config_dict,
                n_nodes=n_nodes,
                connectivity=connectivity,
                entry_node_names=entry_node_names,
                high_value_node_names=high_value_node_names,
            )

        yt_run = YawningTitanRun(
            network=network,
            game_mode=game_mode,
            collect_additional_per_ts_data=True,
            auto=False,
            total_timesteps=1000,
            eval_freq=1000,
            deterministic=deterministic,
        )
        yt_run.setup()

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
            settings_path: Optional[str] = legacy_default_game_mode_path(),
            entry_node_names=None,
            high_value_node_names=None,
            num_episodes=1,
            custom_settings=None,
            raise_errors=True,
            deterministic=False,
    ) -> ActionLoop:
        """Use parameterized settings to return a configured ActionLoop."""
        if custom_settings is not None:
            settings_path = temp_config_from_base(settings_path,
                                                  custom_settings)

        yt_run: YawningTitanRun = generate_generic_env_test_run(
            settings_path=settings_path,
            net_creator_type="18node",
            entry_node_names=entry_node_names,
            high_value_node_names=high_value_node_names,
            raise_errors=raise_errors,
            env_only=False,
            deterministic=deterministic,
        )

        return ActionLoop(yt_run.env, yt_run.agent, episode_count=num_episodes)

    return _basic_2_agent_loop
