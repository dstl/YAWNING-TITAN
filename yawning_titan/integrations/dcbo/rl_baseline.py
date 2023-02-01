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
from __future__ import annotations

from stable_baselines3 import PPO

from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import dcbo_game_mode_path
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.networks import network_creator
from yawning_titan.networks.network import Network
from yawning_titan.yawning_titan_run import YawningTitanRun


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
    save: bool = True,
) -> tuple[PPO | None, str | None] | tuple[PPO | None, None]:
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
    :param save: If True, saves the trained agent using the stable_baselines3 save as zip functionality.
    :return: A trained agent as an instance of
        :class:`stable_baselines3.ppo.ppo.PPO`.
    """
    matrix, positions = network_creator.dcbo_base_network()

    yt_run = YawningTitanRun(
        network=Network(matrix=matrix, positions=positions),
        game_mode=GameModeConfig.create_from_yaml(dcbo_game_mode_path()),
        red_agent_class=SineWaveRedAgent,
        blue_agent_class=BlueInterface,
        eval_freq=eval_freq,
        total_timesteps=total_timesteps,
        n_eval_episodes=n_eval_episodes,
        deterministic=deterministic,
        print_metrics=print_metrics,
        show_metrics_every=show_metrics_every,
        collect_additional_per_ts_data=collect_additional_per_ts_data,
        warn=warn,
        render=render,
        verbose=verbose,
    )

    if save:
        path = yt_run.save()
        return yt_run.agent, path
    else:
        return yt_run.agent, None
