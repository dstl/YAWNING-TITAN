from logging import getLogger
from typing import List, Tuple

from gym import spaces
from stable_baselines3.common.env_checker import check_env

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import dcbo_game_mode_path
from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.integrations.dcbo.dcbo_agent import DCBOAgent

_LOGGER = getLogger(__name__)


def create_env(use_same_net: bool = False) -> GenericNetworkEnv:
    """
    Create a YAWNING TITAN environment.

    :param use_same_net: If true uses a saved network, otherwise creates a new
        network.

    :returns: A YAWNING TITAN OpenAI Gym environment.

    """
    game_mode = GameModeConfig.create_from_yaml(dcbo_game_mode_path())

    if use_same_net:
        matrix, positions = network_creator.dcbo_base_network()
        network = NetworkConfig.create_from_args(matrix=matrix, positions=positions)
    else:
        matrix, positions = network_creator.create_mesh(size=10)
        network = NetworkConfig.create_from_args(matrix=matrix, positions=positions)

    network_interface = NetworkInterface(game_mode, network)

    red = SineWaveRedAgent(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(
        red_agent=red,
        blue_agent=blue,
        network_interface=network_interface,
        print_metrics=True,
        show_metrics_every=10,
        collect_additional_per_ts_data=True,
    )

    check_env(env, warn=True)

    env.reset()

    return env


def init_dcbo_agent(action_probabs: Tuple[None, List[float]]) -> DCBOAgent:
    """
    Create a DCBOAgent object with a set of initial action probabilities.

    :param action_probabs: The initial probabilities for actions (optional).

    :returns: A DCBOAgent object.
    """
    if action_probabs:
        if sum(action_probabs) != 1:
            msg = (
                f"The sum of the probabilities provided must be equal to 1. "
                f"Was given {action_probabs} which sum to {sum(action_probabs)}"
            )
            try:
                raise ValueError(msg)
            except ValueError as e:
                _LOGGER.error(msg, exc_info=True)
                raise e

        agent = DCBOAgent(spaces.Discrete(20), action_probabs)
    else:
        agent = DCBOAgent(spaces.Discrete(20), [0.5, 0.5])

    return agent
