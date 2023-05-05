from contextlib import contextmanager
from typing import Dict, Final, List, Optional, Type
from unittest.mock import patch

import pytest
import yaml

from tests import TEST_PACKAGE_DATA_PATH
from tests.game_mode_db_patch import game_mode_db_init_patch
from tests.network_db_patch import network_db_init_patch
from tests.yawning_titan_db_patch import yawning_titan_db_init_patch
from yawning_titan.config.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.item_types.bool_item import BoolItem
from yawning_titan.config.item_types.float_item import FloatItem
from yawning_titan.config.item_types.int_item import IntItem
from yawning_titan.config.item_types.str_item import StrItem
from yawning_titan.db.doc_metadata import DocMetadata, DocMetadataSchema
from yawning_titan.db.yawning_titan_db import YawningTitanDB
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.exceptions import ConfigGroupValidationError
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB
from yawning_titan.networks.node import Node
from yawning_titan.yawning_titan_run import YawningTitanRun
from yawning_titan_gui.views.utils.helpers import GameModeManager, NetworkManager

TOLERANCE: Final[float] = 0.1
N_TIME_STEPS: Final[int] = 1000
N_TIME_STEPS_LONG: Final[int] = 10000


@contextmanager
def not_raises(expected_exception: Type[Exception]):
    """
    Function to test whether a function does not raise an exception.

    A 'good' function test.

    Example of a 'good' test:

    .. code::python::

        a_list = ['This is a good test']
        with not_raises(IndexError):
            print(a_list[0])

    Example of a 'bad' test:

    .. code::python::

        a_list = ['This is a bad test']
        with not_raises(IndexError):
            print(a_list[1])

    :param expected_exception: The type of Exception being tested for.
    :raise AssertionError: When the exception is raised expectedly.
    """
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


@pytest.fixture(scope="session")
def game_mode_db() -> GameModeDB:
    """A patched GameModeDB that uses tests/_package_data/game_modes.json."""
    with patch.object(GameModeDB, "__init__", game_mode_db_init_patch):
        return GameModeDB()


@pytest.fixture(scope="session")
def game_mode_manager() -> GameModeManager:
    """A patched GameModeManager that uses tests/_package_data/game_modes.json."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        GameModeManager.db = GameModeDB()
        return GameModeManager


@pytest.fixture(scope="session")
def network_manager() -> NetworkManager:
    """A patched NetworkManager that uses tests/_package_data/networks.json."""
    with patch.object(YawningTitanDB, "__init__", yawning_titan_db_init_patch):
        NetworkManager.db = NetworkDB()
        return NetworkManager


@pytest.fixture()
def default_game_mode(game_mode_db) -> GameMode:
    """Return the default game mode."""
    return game_mode_db.search(DocMetadataSchema.NAME == "Default Game Mode")[0]


@pytest.fixture(scope="session")
def network_db() -> NetworkDB:
    """A patched NetworkDB that uses tests/_package_data/networks.json."""
    with patch.object(NetworkDB, "__init__", network_db_init_patch):
        return NetworkDB()


@pytest.fixture()
def default_network(network_db) -> Network:
    """Return the default network."""
    network = network_db.search(DocMetadataSchema.NAME == "Default 18-node network")[0]
    network.set_node_positions()
    return network


@pytest.fixture
def temp_networks(network_manager: NetworkManager) -> List[str]:
    """Create a number of temporary networks as copies of an existing network.

    :param source_network: The network id to copy
    :param n: The number of networks to create

    :return: a list of created network Ids.
    """

    def _temp_networks(source_network_id: str, n: int = 1):
        ids = []
        for _ in range(n):
            network = network_manager.db.get(source_network_id)
            meta = network.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            network._doc_metadata = DocMetadata(**meta)
            network_manager.db.insert(network=network, name="temp")
            ids.append(network.doc_metadata.uuid)
        return ids

    return _temp_networks


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
def create_yawning_titan_run(network_db: NetworkDB, game_mode_db: GameModeDB):
    """Create an initialised and setup YawningTitanRun."""

    def _create_yawning_titan_run(
        game_mode_name: str,
        network_name: str,
        timesteps: int = 1000,
        eval_freq: int = 1000,
        deterministic: bool = False,
    ) -> YawningTitanRun:
        network = network_db.search(DocMetadataSchema.NAME == network_name)[0]
        game_mode = game_mode_db.search(DocMetadataSchema.NAME == game_mode_name)[0]

        yt_run = YawningTitanRun(
            network=network,
            game_mode=game_mode,
            collect_additional_per_ts_data=True,
            auto=False,
            total_timesteps=timesteps,
            eval_freq=eval_freq,
            deterministic=deterministic,
        )

        yt_run.setup()

        return yt_run

    return _create_yawning_titan_run


@pytest.fixture
def basic_2_agent_loop(create_yawning_titan_run):
    """Return a basic 2-agent `ActionLoop`."""

    def _basic_2_agent_loop(
        yt_run: YawningTitanRun = None,
        num_episodes=1,
    ) -> ActionLoop:
        """Use parameterized settings to return a configured ActionLoop."""
        if not yt_run:
            yt_run = create_yawning_titan_run(
                game_mode_name="Default Game Mode",
                network_name="Default 18-node network",
            )

        return ActionLoop(yt_run.env, yt_run.agent, episode_count=num_episodes)

    return _basic_2_agent_loop


class Group(ConfigGroup):
    """Basic implementation of a :class: `~yawning_titan.config.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.a: BoolItem = BoolItem(value=False, alias="legacy_a")
        self.b: FloatItem = FloatItem(value=1, alias="legacy_b")
        self.c: StrItem = StrItem(value="test", alias="legacy_c")
        super().__init__(doc)


class GroupTier1(ConfigGroup):
    """Basic implementation of a nested :class: `~yawning_titan.config.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.bool: BoolItem = BoolItem(value=False)
        self.float: FloatItem = FloatItem(value=1)
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
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
    """Basic implementation of a nested :class: `~yawning_titan.config.core.ConfigGroup`."""

    def __init__(self, doc: Optional[str] = None):
        self.bool: BoolItem = BoolItem(value=False)
        self.int: IntItem = IntItem(value=1)
        self.tier_1: GroupTier1 = GroupTier1()
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.core.ConfigGroup`."""
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
    """A test instance of :class: `~yawning_titan.config.core.ConfigGroup`."""
    return Group()


@pytest.fixture
def multi_tier_test_group() -> GroupTier2:
    """A nested test instance of :class: `~yawning_titan.config.core.ConfigGroup`."""
    return GroupTier2()
