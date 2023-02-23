import os
import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional

import pytest
import yaml
from yaml import SafeLoader

from yawning_titan.config.toolbox.core import (
    ConfigGroup,
    ConfigGroupValidation,
    ConfigGroupValidationError,
)
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem
from yawning_titan.config.toolbox.item_types.float_item import FloatItem
from yawning_titan.config.toolbox.item_types.int_item import IntItem
from yawning_titan.config.toolbox.item_types.str_item import StrItem
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_modes import default_game_mode_path
from yawning_titan.networks import network_creator
from yawning_titan.networks.network import (
    Network,
    RandomEntryNodePreference,
    RandomHighValueNodePreference,
)
from yawning_titan.networks.network_db import default_18_node_network
from yawning_titan.yawning_titan_run import YawningTitanRun


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

        network = network_creator.create_mesh(size=n_nodes, connectivity=connectivity)

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
def generate_generic_env_test_run(create_test_network):
    """Return a `GenericNetworkEnv`."""

    def _generate_generic_env_test_run(
        settings_path: Optional[str] = default_game_mode_path(),
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
        settings_path: Optional[str] = default_game_mode_path(),
        entry_node_names=None,
        high_value_node_names=None,
        num_episodes=1,
        custom_settings=None,
        raise_errors=True,
        deterministic=False,
    ) -> ActionLoop:
        """Use parameterized settings to return a configured ActionLoop."""
        if custom_settings is not None:
            settings_path = temp_config_from_base(settings_path, custom_settings)

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


class Group(ConfigGroup):
    """Basic implementation of a :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.a: BoolItem = BoolItem(value=False, alias="legacy_a")
        self.b: FloatItem = FloatItem(value=1, alias="legacy_b")
        self.c: StrItem = StrItem(value="test", alias="legacy_c")
        super().__init__(doc)


class GroupTier1(ConfigGroup):
    """Basic implementation of a nested :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.bool: BoolItem = BoolItem(value=False)
        self.float: FloatItem = FloatItem(value=1)
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()
        try:
            if self.bool.value and self.float.value > 1:
                msg = "test error tier 1"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        try:
            if self.bool.value and self.float.value < 0:
                msg = "test error tier 1 b"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class GroupTier2(ConfigGroup):
    """Basic implementation of a nested :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.bool: BoolItem = BoolItem(value=False)
        self.int: IntItem = IntItem(value=1)
        self.tier_1: GroupTier1 = GroupTier1()
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()
        try:
            if self.bool.value and self.int.value != 1:
                msg = "test error tier 2"
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


@pytest.fixture
def test_group() -> Group:
    """A test instance of :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
    return Group()


@pytest.fixture
def multi_tier_test_group() -> GroupTier2:
    """A nested test instance of :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
    return GroupTier2()
