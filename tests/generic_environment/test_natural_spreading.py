import os

from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_natural_spreading(generate_generic_env_test_reqs):
    """Test the natural spreading simulation mechanic works as intended."""
    # generate an env
    n_nodes = 100
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH_OLD, "spreading_config.yaml"),
        net_creator_type="mesh",
        n_nodes=n_nodes,
        entry_nodes=["0", "1", "2"],
    )
    check_env(env, warn=True)
    env.reset()
    total_cum_success = 0
    for _ in range(N_TIME_STEPS):
        # step through the environment and count the number of attacks, red cannot perform any actions so the only
        # attacks are from natural spreading
        env.step(0)
        total_cum_success += len(env.network_interface.true_attacks) / n_nodes
    spreading_success_rate = total_cum_success / N_TIME_STEPS
    # ensure that the number of spreads is within a reasonable degree of accuracy of the set spreading rate
    assert 0.0185 < spreading_success_rate < 0.0215
