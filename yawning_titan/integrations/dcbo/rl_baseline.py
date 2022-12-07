"""
Generates a Reinforcement Learning (RL) baseline agent.

Uses the same network and scenario config as used to generated DCBO data and
saves training metrics to tensorboard.

.. warning::

    This module is being deprecated in a future release. This release will see
    the introduction of a Yawning-Titan runner module. This specific
    'Reinforcement Learning (RL) baseline agent' example will be available as a
    pre-defined configurable run.
"""

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import dcbo_game_mode_path
from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator

game_mode = GameModeConfig.create_from_yaml(dcbo_game_mode_path())

matrix, positions = network_creator.dcbo_base_network()
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
    collect_additional_per_ts_data=False,
)

check_env(env, warn=True)

env.reset()

agent = PPO(PPOMlp, env, verbose=1, tensorboard_log="logs/ppo-tensorboard/")

eval_callback = EvalCallback(
    Monitor(env), eval_freq=20000, deterministic=False, render=False
)

agent.learn(total_timesteps=350000, n_eval_episodes=1, callback=eval_callback)
