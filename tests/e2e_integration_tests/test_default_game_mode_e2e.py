import os.path
import tempfile

import pytest
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import \
    NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator


@pytest.mark.e2e_integration_test 
def test_default_game_mode_e2e():
    runs = True
    try:
        matrix, node_positions = network_creator.create_18_node_network()

        entry_nodes = ["0", "1", "2"]

        network_interface = NetworkInterface(
            matrix, node_positions, entry_nodes=entry_nodes,
        )

        red = RedInterface(network_interface)

        blue = BlueInterface(network_interface)

        env = GenericNetworkEnv(red, blue, network_interface)

        check_env(env, warn=True)

        _ = env.reset()

        eval_callback = EvalCallback(
            Monitor(env), eval_freq=1000, deterministic=False, render=False
        )

        agent = PPO(PPOMlp, env, verbose=1)

        agent.learn(
            total_timesteps=1000, n_eval_episodes=100, callback=eval_callback
        )
        
        evaluate_policy(agent, env, n_eval_episodes=100)
    except Exception:
        # TODO: Remove the catch-all exception once we know how to properly
        #  assert that the e2e run has done what it was supposed to do.
        runs = False
    assert runs
