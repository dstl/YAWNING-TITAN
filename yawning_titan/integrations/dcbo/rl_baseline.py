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

from yawning_titan import PPO_TENSORBOARD_LOGS_DIR
from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import dcbo_game_mode_path
from yawning_titan.config.network_config.network_config import NetworkConfig
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator


def generate(
    eval_freq: int = 20000,
    total_timesteps: int = 350000,
    n_eval_episodes: int = 1,
    deterministic: bool = False,
    print_metrics: bool = True,
    show_metrics_every: int = 10,
    collect_additional_per_ts_data: bool = False,
    warn: bool = True,
    render: bool = False,
    verbose: int = 1,
) -> PPO:
    """
    Generate a Reinforcement Learning (RL) baseline agent.

    :param eval_freq: Evaluate the agent every ``eval_freq`` call of the
        callback. Default value = 20,000.
    :param total_timesteps: The number of samples (env steps) to train on.
        Default value = 350,000.
    :param n_eval_episodes: The number of episodes to evaluate the agent.
        Default value = 1.
    :param deterministic: Whether the evaluation should use stochastic or
        deterministic actions. Default value = False.
    :param print_metrics: Print the metrics if True. Default value = True.
    :param show_metrics_every: Prints the metrics every ``show_metrics_every``
        timesteps. Default value = 10.
    :param collect_additional_per_ts_data: Collects additional per-timestep
        data if True.Default value = False.
    :param warn: Output additional warnings mainly related to the
        interaction with stable_baselines if True. Default value = True.
    :param render: Renders the environment during evaluation if True. Default
        value = False.
    :param verbose: Verbosity level: 0 for no output, 1 for info messages
        (such as device or wrappers used), 2 for debug messages. Default
        value = 1.
    :return: A trained agent as an instance of
        :class:`stable_baselines3.ppo.ppo.PPO`.
    """
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
        print_metrics=print_metrics,
        show_metrics_every=show_metrics_every,
        collect_additional_per_ts_data=collect_additional_per_ts_data,
    )

    check_env(env, warn=warn)

    env.reset()

    agent = PPO(
        PPOMlp,
        env,
        verbose=verbose,
        tensorboard_log=str(PPO_TENSORBOARD_LOGS_DIR),
        seed=env.network_interface.random_seed,
    )

    eval_callback = EvalCallback(
        Monitor(env), eval_freq=eval_freq, deterministic=deterministic, render=render
    )

    agent.learn(
        total_timesteps=total_timesteps,
        n_eval_episodes=n_eval_episodes,
        callback=eval_callback,
    )

    return agent
