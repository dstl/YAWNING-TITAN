"""
A custom config runner module.

This module is used simple as a playground/testbed for custom configurations of
Yawning-Titan.

.. warning::

    This module is being deprecated in a future release to make way for
    Yawning-Titan runner module in the main package.
"""
import time

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator

game_mode = GameModeConfig.create_from_yaml(default_game_mode_path())

matrix, positions = network_creator.gnp_random_connected_graph(
    n_nodes=15, probability_of_edge=0.02
)
network = NetworkConfig.create_from_args(matrix=matrix, positions=positions)

network_interface = NetworkInterface(game_mode=game_mode, network=network)

red = SineWaveRedAgent(network_interface)
blue = BlueInterface(network_interface)

env = GenericNetworkEnv(
    red,
    blue,
    network_interface,
    print_metrics=True,
    show_metrics_every=10,
    collect_additional_per_ts_data=True,
    print_per_ts_data=False,
)

check_env(env, warn=True)

env.reset()


ENABLE_PROFILER = False
CREATE_TENSORBOARD = False
RENDER_FINAL_AGENT = True
DURING_TRAIN_EVAL = False

if CREATE_TENSORBOARD:
    agent = PPO(PPOMlp, env, verbose=1, tensorboard_log="logs/ppo-tensorboard/")
else:
    agent = PPO(PPOMlp, env, verbose=1)


eval_callback = EvalCallback(
    Monitor(env), eval_freq=1000, deterministic=False, render=True
)

if ENABLE_PROFILER:
    import cProfile
    import pstats

    profiler = cProfile.Profile()

    profiler.enable()
    if DURING_TRAIN_EVAL:
        agent.learn(total_timesteps=5000, n_eval_episodes=1, callback=eval_callback)
    else:
        agent.learn(total_timesteps=5000)

    profiler.disable()

    stats = pstats.Stats(profiler)

    stats.sort_stats("tottime")

    stats.print_stats()
else:
    if DURING_TRAIN_EVAL:
        agent.learn(total_timesteps=5000, n_eval_episodes=1, callback=eval_callback)
    else:
        agent.learn(total_timesteps=5000)


if RENDER_FINAL_AGENT:
    filename = f"ppo_18-node-env-v0_{round(time.time())}"

    loop = ActionLoop(env, agent, filename, episode_count=100)
    loop.gif_action_loop()
