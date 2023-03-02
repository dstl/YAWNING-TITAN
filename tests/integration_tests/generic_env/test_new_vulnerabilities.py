import random

import pytest
from stable_baselines3.common.env_checker import check_env

from tests.conftest import N_TIME_STEPS


@pytest.mark.integration_test
def test_new_vulnerabilities(create_yawning_titan_run):
    """Test that new vulnerabilities are chosen at each reset if activated within configuration."""
    # check that new vulnerabilities are being chosen (randomly)
    yt_run = create_yawning_titan_run(
        game_mode_name="new_high_value_node",
        network_name="mesh_15"
    )
    env = yt_run.env
    check_env(env, warn=True)
    env.reset()
    vulnerabilities = 0
    resets = 0
    for i in range(0, N_TIME_STEPS):
        obs, rew, done, notes = env.step(
            random.randint(0, env.BLUE.get_number_of_actions() - 1)
        )
        if done:
            vulnerabilities += sum(
                env.network_interface.get_all_vulnerabilities().values()
            )
            resets += 1
            env.reset()
    # calculate the average vulnerability
    vulnerabilities = (vulnerabilities / 15) / resets
    vuln_aim = (
        env.network_interface.current_graph.node_vulnerability_lower_bound
        + 0.5
        * (
            env.network_interface.current_graph.node_vulnerability_upper_bound
            - env.network_interface.current_graph.node_vulnerability_lower_bound
        )
    )
    # ensure the average vulnerability is half way between the upper and lower range
    assert (vuln_aim - 0.01 * vuln_aim) < vulnerabilities < (vuln_aim + 0.01 * vuln_aim)
