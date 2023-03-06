import pytest
from stable_baselines3.common.env_checker import check_env

from tests.conftest import N_TIME_STEPS


@pytest.mark.integration_test
def test_natural_spreading(create_yawning_titan_run):
    """Test the natural spreading simulation mechanic works as intended."""
    # generate an env
    yt_run = create_yawning_titan_run(
        game_mode_name="spreading_config",
        network_name="mesh_50"
    )
    env = yt_run.env
    check_env(env, warn=True)
    env.reset()
    total_cum_success = 0
    for _ in range(N_TIME_STEPS):
        # step through the environment and count the number of attacks, red cannot perform any actions so the only
        # attacks are from natural spreading
        env.step(0)
        total_cum_success += len(env.network_interface.true_attacks) / 50
    spreading_success_rate = total_cum_success / N_TIME_STEPS
    # ensure that the number of spreads is within a reasonable degree of accuracy of the set spreading rate
    assert 0.0185 < spreading_success_rate < 0.0215
