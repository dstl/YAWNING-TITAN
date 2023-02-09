import os
import random

from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_new_vulnerabilities(generate_generic_run_test_reqs):
    """Test that new vulnerabilities are chosen at each reset if activated within configuration."""
    # check that new vulnerabilities are being chosen (randomly)
    env: GenericNetworkEnv = generate_generic_run_test_reqs(
        os.path.join(TEST_CONFIG_PATH_OLD, "new_high_value_node.yaml"),
        net_creator_type="mesh",
        n_nodes=15,
        entry_nodes=["0", "1", "2"],
    )
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
