import gym
import pytest
from stable_baselines3.common.env_checker import check_env


@pytest.mark.parametrize(
    "environment", ["five-node-def-v0", "four-node-def-v0", "18-node-env-v0"]
)
def test_environment_sb3_compliance(environment):
    """Tests stable baseline3 environment checker compliance."""
    env = gym.make(environment)
    check_env(env)
    env.close()
