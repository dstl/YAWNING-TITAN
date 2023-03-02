import random

import networkx as nx
import pytest
from stable_baselines3.common.env_checker import check_env

from tests.generic_environment import N_TIME_STEPS


@pytest.mark.integration_test
def test_env_reset(create_yawning_titan_run):
    """Checks that the env reset is performed properly."""
    yt_run = create_yawning_titan_run(
        game_mode_name="base_config",
        network_name="mesh_18"
    )
    env = yt_run.env

    env.reset()

    check_env(env, warn=True)
    env.reset()
    for i in range(0, N_TIME_STEPS):
        obs, rew, done, notes = env.step(
            random.randint(0, env.BLUE.get_number_of_actions() - 1)
        )
        if done:
            env.reset()
            # check no deceptive nodes left in the environment
            assert (
                len(
                    env.network_interface.current_graph.get_nodes(filter_deceptive=True)
                )
                == 0
            )

            # check red agent is reset
            assert env.network_interface.red_current_location is None
            # check all nodes are set back to their initial state
            assert (
                1
                not in env.network_interface.get_all_node_blue_view_compromised_states().values()
            )
            assert (
                1
                not in env.network_interface.get_all_node_compromised_states().values()
            )
            assert (
                env.network_interface.current_graph.get_nodes(
                    filter_true_compromised=True
                )
                == []
            )
            # check deceptive node pointers are reset
            assert env.network_interface.deceptive_node_pointer == 0
            assert env.network_interface.current_deceptive_nodes == 0
            assert env.network_interface.reached_max_deceptive_nodes is False
            # check the network is the same as the base
            assert nx.is_isomorphic(
                env.network_interface.base_graph, env.network_interface.current_graph
            )
            # check all previous attacks are removed
            assert env.network_interface.true_attacks == []
            assert env.network_interface.detected_attacks == []
