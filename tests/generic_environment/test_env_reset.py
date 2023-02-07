# check to make sure than when an env is reset all of the proper values are reset too
import os
import random

import networkx as nx
from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_env_reset(generate_generic_env_test_reqs):
    """Test environment resets clean up properly."""
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH_OLD, "base_config.yaml"),
        net_creator_type="mesh",
        n_nodes=15,
        entry_nodes=["0", "1", "2"],
    )

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
