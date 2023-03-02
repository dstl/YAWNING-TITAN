import random
from collections import defaultdict

import numpy as np
import pytest
from stable_baselines3.common.env_checker import check_env

from tests.conftest import N_TIME_STEPS_LONG, TOLERANCE


@pytest.mark.integration_test
def test_new_high_value_node(create_yawning_titan_run):
    """Test the high value node gaol mechanic - focus on selection."""
    # check that a new high value node is being chosen
    yt_run = create_yawning_titan_run(
        game_mode_name="new_high_value_node",
        network_name="mesh_15"
    )
    env = yt_run.env
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
