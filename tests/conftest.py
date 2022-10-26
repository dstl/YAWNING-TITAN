import pytest
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from stable_baselines3.common.env_checker import check_env

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.network_interface import NetworkInterface

@pytest.fixture
def basic_2_agent_loop(request)->ActionLoop:
    matrix, node_positions = network_creator.create_18_node_network()

    entry_nodes = ["0"]

    settings_path = Path(__file__).parent / "test_configs/repeatable_threat_config.yaml"

    network_interface = NetworkInterface(matrix, node_positions, entry_nodes=entry_nodes, high_value_target='12',settings_path=settings_path.as_posix())

    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(red, blue, network_interface, seed=request.param["seed"])

    check_env(env, warn=True)

    _ = env.reset()

    agent = PPO(PPOMlp, env, verbose=1, seed=request.param["seed"]) #TODO: allow PPO to inherit environment seed. Monkey patch additional feature?

    agent = agent.learn(total_timesteps=1000)


    return ActionLoop(env,agent,episode_count=request.param["episodes"])