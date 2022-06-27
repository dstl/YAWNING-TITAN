import gym
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp

import yawning_titan  # noqa


def test_default_environment_init():
    """Test the environment initialise and check default values."""
    env = gym.make("18-node-env-v0")

    assert env.chance_to_spread
    assert env.chance_to_spread == 0.01
    assert env.chance_to_spread_during_patch == 0.01
    assert env.chance_to_randomly_compromise == 0.15
    assert env.cost_of_isolate == 10
    assert env.cost_of_patch == 5
    assert env.cost_of_nothing == 0
    assert env.end == 1000
    assert env.spread_vs_random_intrusion == 0.5
    assert env.punish_for_isolate is False
    assert env.reward_method == 1
    assert env.duration == 0


def test_environment_reset():
    """Test the environment reset."""
    env = gym.make("18-node-env-v0")
    agent = PPO(PPOMlp, env, verbose=1)
    agent.learn(total_timesteps=10000)

    env.reset()

    assert env.duration == 0
