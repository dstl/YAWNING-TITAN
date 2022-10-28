import pytest
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.network_interface import NetworkInterface

@pytest.fixture
def basic_2_agent_loop(request)->ActionLoop:
    matrix, node_positions = network_creator.create_18_node_network()

    entry_nodes = None
    settings_path = None
    seed = None
    num_episodes = 1

    if "entry_nodes" in request.param:
        entry_nodes = request.param["entry_nodes"]

    if "settings_file" in request.param:
        settings_path = (Path(__file__).parent / "test_configs" / request.param["settings_file"]).as_posix()

    if "seed" in request.param:
        seed = request.param["seed"]

    if "episodes" in request.param:
        num_episodes = request.param["episodes"]    
    

    network_interface = NetworkInterface(matrix, node_positions, entry_nodes=entry_nodes, high_value_target='12',settings_path=settings_path)

    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(red, blue, network_interface, seed=seed)

    check_env(env, warn=True)

    _ = env.reset()

    eval_callback = EvalCallback(
            Monitor(env), eval_freq=1000, deterministic=False, render=False
        )

    agent = PPO(PPOMlp, env, verbose=1, seed=seed) #TODO: allow PPO to inherit environment seed. Monkey patch additional feature?

    agent.learn(
            total_timesteps=1000, n_eval_episodes=100, callback=eval_callback
    )

    return ActionLoop(env,agent,episode_count=num_episodes)