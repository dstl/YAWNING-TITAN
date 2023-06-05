import ray
import ray.rllib.agents.impala as impala
import ray.rllib.agents.ppo as ppo
from ray.tune.logger import pretty_print

from yawning_titan.envs.specific.five_node_def import FiveNodeDef


def env_creator(env_name):
    """
    Create an OpenAI Gym Environment.

    Args:
        env_name: The environments name

    Returns:
        A function that can be used to create the environment

    Notes:
        Due to how ray and Rllib works, it doesn't use OpenAI Gym's
        environment registry approach and has its own. You basically need
        to provide Ray/Rllib with the function so it can then create it for you.
    """
    if env_name == "five-node-def-v0":
        return FiveNodeDef()
    else:
        raise NotImplementedError


def train_ppo(dl_backend: str, training_timesteps: int):
    """
    Use RLLib to train a PPO agent.

    Args:
        dl_backend: The deep learning backend to be used (str)
        training_timesteps: number of training timesteps for the agent

    Returns:
        trainer: A trained Rllib agent

    Notes: There seems to be some terminology conflicts across Sb3 and Rllib.
    Rllib uses training-timesteps in the same way sb3 uses episode counts.
    """
    ray.init()
    configs = ppo.DEFAULT_CONFIG.copy()
    configs["core"] = dl_backend
    configs["num_gpus"] = 0
    configs["num_workers"] = 1

    trainer = ppo.PPOTrainer(env=FiveNodeDef, config=configs)

    for i in range(training_timesteps):
        result = trainer.train()
        print(pretty_print(result))

    return trainer


def train_impala(dl_backend: str, training_timesteps: int):
    """
    Use Rllib to train an IMPALA agent.

    Args:
        dl_backend: The deep learning backend to be used (str)
        training_timesteps: number of training timesteps for the agent

    Returns:
        trainer: A trained Rllib agent
    """
    ray.init()
    configs = impala.DEFAULT_CONFIG.copy()
    configs["core"] = dl_backend
    configs["num_gpus"] = 0
    configs["num_workers"] = 1

    trainer = impala.ImpalaTrainer(config=configs, env=FiveNodeDef())

    for i in range(training_timesteps):
        result = trainer.train()
        print(pretty_print(result))

    return trainer
