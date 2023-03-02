import random

import numpy as np
import pytest
from stable_baselines3.common.env_checker import check_env


@pytest.mark.integration_test()
def test_new_entry_nodes(create_yawning_titan_run):
    """Test the selection of entry nodes and validate they are correct."""
    yt_run = create_yawning_titan_run(
        game_mode_name="new_entry_nodes",
        network_name="mesh_18"
    )
    env = yt_run.env
    check_env(env, warn=True)
    env.reset()
    entry_nodes = {}
    for i in range(0, 10000):
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
    assert len(entry_nodes.keys()) == 18
    # check that each node is roughly chosen equally
    target_count = (
        10000 / len(entry_nodes.values()) * 3
    )  # num entry nodes = 3
    for i in entry_nodes.values():
        assert np.isclose(i, target_count, atol=(target_count * 0.1))
