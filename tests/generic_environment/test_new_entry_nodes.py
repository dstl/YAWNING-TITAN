import os
import random

import numpy as np
from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS_LONG, TOLERANCE
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_new_entry_nodes(generate_generic_env_test_reqs):
    """Test the selection of entry nodes and validate they are correct."""
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH_OLD, "new_entry_nodes.yaml"),
        net_creator_type="mesh",
        n_nodes=15,
        entry_nodes=["0", "1", "2"],
    )
    check_env(env, warn=True)
    env.reset()
    entry_nodes = {}
    for i in range(0, N_TIME_STEPS_LONG):
        obs, rew, done, notes = env.step(
            random.randint(0, env.BLUE.get_number_of_actions() - 1)
        )
        if done:
            for node in env.network_interface.current_graph.entry_nodes:
                if node.uuid not in entry_nodes:
                    entry_nodes[node.uuid] = 1
                else:
                    entry_nodes[node.uuid] += 1
            env.reset()
    # check that entry nodes cannot be chosen
    assert len(entry_nodes.keys()) == 15
    # check that each node is roughly chosen equally
    target_count = (
        N_TIME_STEPS_LONG / len(entry_nodes.values()) * 3
    )  # num entry nodes = 3
    for i in entry_nodes.values():
        assert np.isclose(i, target_count, atol=(target_count * TOLERANCE))
