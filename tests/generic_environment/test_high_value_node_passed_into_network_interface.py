import os
import random
from collections import defaultdict

from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS_LONG
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv

# TODO: This test now tests operations handled by Network class and should therefore be moved


def test_high_value_node_passed_into_network_interface(generate_generic_env_test_run):
    """Test the high value node gaol mechanic - manually passed to."""
    env: GenericNetworkEnv = generate_generic_env_test_run(
        os.path.join(TEST_CONFIG_PATH_OLD, "high_value_node_provided.yaml"),
        net_creator_type="mesh",
        n_nodes=30,
        high_value_node_names=["15", "16"],
        entry_node_names=["0", "1", "2"],
    )
    check_env(env, warn=True)
    env.reset()
    targets = defaultdict(lambda: 0)
    for _ in range(0, N_TIME_STEPS_LONG):
        obs, rew, done, notes = env.step(
            random.randint(0, env.BLUE.get_number_of_actions() - 1)
        )
        if done:
            # add 1 to each node that gets chosen as a high value node
            for node in env.network_interface.current_graph.high_value_nodes:
                targets[node.name] += 1

            env.reset()
    # the only 2 targets set are available
    assert len(targets.keys()) == 2

    # check that the keys are the 15 and 16 that was set
    assert set(targets.keys()).intersection(["15", "16"])
