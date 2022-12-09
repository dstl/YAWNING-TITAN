"""
Generates a Reinforcement Learning (RL) baseline agent.

Uses the same network and scenario config as used to generated DCBO data and saves training metrics to tensorboard.
"""
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.networks import network_creator

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = f"{BASE_DIR}/dcbo_config.yaml"

matrix, node_positions = network_creator.load_network(f"{BASE_DIR}/base_net.txt")

network_interface = NetworkInterface(
    matrix, node_positions, settings_path=SETTINGS_PATH
)

red = SineWaveRedAgent(network_interface)
blue = BlueInterface(network_interface)

number_of_actions = blue.get_number_of_actions()
number_of_actions = 2

env = GenericNetworkEnv(
    red,
    blue,
    network_interface,
    number_of_actions,
    print_metrics=True,
    show_metrics_every=10,
    collect_additional_per_ts_data=False,
)

check_env(env, warn=True)

env.reset()

agent = PPO(PPOMlp, env, verbose=1, tensorboard_log="logs/ppo-tensorboard/")

eval_callback = EvalCallback(
    Monitor(env), eval_freq=20000, deterministic=False, render=False
)

agent.learn(total_timesteps=350000, n_eval_episodes=1, callback=eval_callback)
