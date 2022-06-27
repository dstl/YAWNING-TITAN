from pathlib import Path
from typing import List, Tuple

from gym import spaces
from stable_baselines3.common.env_checker import check_env

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.integrations.dcbo.dcbo_agent import DCBOAgent

BASE_DIR = Path(__file__).resolve().parent


def create_env(use_same_net: bool = False) -> GenericNetworkEnv:
    """
    Create a YAWNING TITAN environment.

    Args:
        use_same_net: If true uses a saved network, otherwise creates a new network

    Returns:
        A YAWNING TITAN OpenAI Gym environment

    """
    settings_path = f"{BASE_DIR}/dcbo_config.yaml"

    if use_same_net:
        matrix, node_positions = network_creator.load_network(
            f"{BASE_DIR}/dcbo_base_net.txt"
        )
    else:
        matrix, node_positions = network_creator.create_mesh(size=10)

    network_interface = NetworkInterface(
        matrix, node_positions, settings_path=settings_path
    )

    red = SineWaveRedAgent(network_interface)
    blue = BlueInterface(network_interface)

    number_of_actions = blue.get_number_of_actions()

    env = GenericNetworkEnv(
        red,
        blue,
        network_interface,
        number_of_actions,
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

    Args:
        action_probabs: The initial probabilities for actions (optional)

    Returns:
        A DCBOAgent object
    """
    if action_probabs:
        assert (
            sum(action_probabs) == 1
        ), f"The sum of the probabilities provided must be equal to 1. Was given {action_probabs} which sum to {sum(action_probabs)}"
        agent = DCBOAgent(spaces.Discrete(20), action_probabs)
    else:
        agent = DCBOAgent(spaces.Discrete(20), [0.5, 0.5])

    return agent
