import logging
from statistics import mean

import gym
from scipy.stats import describe, iqr
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.a2c import MlpPolicy as A2CMlp
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn import MlpPolicy as DQNMlp
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from tabulate import tabulate

from yawning_titan.agents.random import RandomAgent

logger = logging.getLogger(__name__)


def init_env(env: str, experiment_id: str):
    """
    Use the Stable Baselines 3 Monitor wrappper to wrap an environment in order to enable monitoring.

    Args:
        env: the registered name of an OpenAI gym environment (str)
        experiment_id: a UID for the experiment (str)

    Returns:
        A Stable Baselines 3 Monitor Wrapped Gym Environment
    """
    wrapped_env = Monitor(
        gym.make(env), filename=f"./logs/{experiment_id}", allow_early_resets=True
    )

    return wrapped_env


def train_and_eval(
    agent_name: str, environment, training_timesteps: int, n_eval_episodes: int
):
    """
    Train and Evaluate an agent.

    Args:
        agent_name: the algorithm name (str)
        environment: An initlaised Open AI Gym environment
        training_timesteps: total no. of training timesteps (int)

    Returns:
        chosen_agent: a trained Stable Baselines 3 agent
        eval_pol: the output from the Stable Baselines 3 'evaluate_policy' function

    """
    agent_dic = {"ppo": 0, "a2c": 1, "random": 2, "dqn": 3}

    agent_list = [
        PPO(PPOMlp, environment, verbose=1, tensorboard_log="./logs/ppo-tensorboard"),
        A2C(A2CMlp, environment, verbose=1, tensorboard_log="./logs/a2c-tensorboard"),
        RandomAgent(environment.action_space),
        DQN(DQNMlp, environment, verbose=1, tensorboard_log="./logs/dqn-tensorboard"),
    ]

    chosen_agent = agent_list[agent_dic[agent_name]]
    logger.debug(f"{agent_name} Agent Initialised")
    chosen_agent.learn(total_timesteps=training_timesteps)
    logger.debug(f"Completed Training {agent_name}")
    print("Training Complete - Entering Evaluation")
    eval_pol = evaluate_policy(
        chosen_agent,
        environment,
        return_episode_rewards=True,
        n_eval_episodes=n_eval_episodes,
    )

    return chosen_agent, eval_pol


def print_metric_stats(metric_name, metrics: list, raw_metrics=False) -> None:
    """
    Take a metric name and a list of values and prints associated stats.

    Args:
        metric_name: The metric name (str)
        metrics: A list of ints/float metric readings(list)
    """
    print(f"---- {metric_name} ----")
    descriptive_stats = describe(metrics)
    tabular_metrics = [
        ["No. of Obs", descriptive_stats[0]],
        ["Mean", mean(metrics)],
        ["IQR", iqr(metrics)],
        ["Min", descriptive_stats[1][0]],
        ["Max", descriptive_stats[1][1]],
        ["Variance", descriptive_stats[3]],
        ["Skewness", descriptive_stats[4]],
        ["Kurtosis", descriptive_stats[5]],
    ]
    print(tabulate(tabular_metrics))

    if raw_metrics:
        print(f"Per {metric_name}: {metrics}")


def print_policy_eval_metrics(agents: list, evals: list, raw_metrics=False) -> None:
    """
    Output policy evaluation metrics and summary statistics.

    Args:
        agents: An index of the agents that were evaluated(list)
        evals: The output from Stable Baselines 3 'evaluate_policy'
               for each of the agents trained

    """
    for i in range(len(evals)):
        rewards = evals[i][0]
        lengths = evals[i][1]

        print(f"Agent: {agents[i]}")
        print_metric_stats("Episode Reward", rewards, raw_metrics)
        print_metric_stats("Episode Length", lengths, raw_metrics)
        print("\n")
