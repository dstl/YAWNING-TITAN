import os
import random
from collections import defaultdict

import numpy as np
from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS_LONG, TOLERANCE
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_new_high_value_node(generate_generic_env_test_run):
    """Test the high value node gaol mechanic - focus on selection."""
    # check that a new high value node is being chosen
    env: GenericNetworkEnv = generate_generic_env_test_run(
        os.path.join(TEST_CONFIG_PATH_OLD, "new_high_value_node.yaml"),
        net_creator_type="mesh",
        n_nodes=15,
        entry_nodes=["0", "1", "2"],
    )
    check_env(env, warn=True)
    env.reset()
    nodes = defaultdict(lambda: 0)
    for i in range(0, N_TIME_STEPS_LONG):
        obs, rew, done, notes = env.step(
            random.randint(0, env.BLUE.get_number_of_actions() - 1)
        )
        if done:
            # add 1 to each node that gets chosen as a high value node
            for node in env.network_interface.current_graph.high_value_nodes:
                nodes[node] += 1

            env.reset()
    # check that entry nodes cannot be chosen
    # 3 entry nodes are configured in new_high_value_node.yaml, so n_nodes - number_of_entry_nodes = 12
    assert len(nodes.keys()) == 12
    # check that each node is roughly chosen equally
    target_count = N_TIME_STEPS_LONG / len(nodes.values())
    for i in nodes.values():
        assert np.isclose(i, target_count, atol=(target_count * TOLERANCE))
