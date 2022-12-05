import pytest
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


@pytest.mark.e2e_integration_test
def test_default_game_mode_e2e(generate_generic_env_test_reqs):
    """Tests the default game mode ent-to-end."""
    runs = True
    try:
        entry_nodes = ["0", "1", "2"]
        env: GenericNetworkEnv = generate_generic_env_test_reqs(entry_nodes=entry_nodes)

        check_env(env, warn=True)

        _ = env.reset()

        eval_callback = EvalCallback(
            Monitor(env), eval_freq=1000, deterministic=False, render=False
        )

        agent = PPO(PPOMlp, env, verbose=1)

        agent.learn(total_timesteps=1000, n_eval_episodes=100, callback=eval_callback)

        evaluate_policy(agent, env, n_eval_episodes=100)
    except Exception:
        # TODO: Remove the catch-all exception once we know how to properly
        #  assert that the e2e run has done what it was supposed to do.
        runs = False
    assert runs
