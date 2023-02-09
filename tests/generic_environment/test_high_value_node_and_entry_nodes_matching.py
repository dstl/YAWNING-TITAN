import os
import random
import warnings

import pytest
from stable_baselines3.common.env_checker import check_env

from tests import TEST_CONFIG_PATH_OLD
from tests.generic_environment import N_TIME_STEPS_LONG
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


@pytest.mark.skip(
    reason="Assertion fails due to the emergence of a new warning: 'non-integer"
    " arguments to randrange() have been deprecated since Python 3.10 and "
    "will be removed in a subsequent version'"
)
def test_high_value_node_and_entry_nodes_matching(generate_generic_env_test_run):
    """Test the high value node gaol mechanic - manually passed to ."""
    with warnings.catch_warnings(record=True) as w:
        env: GenericNetworkEnv = generate_generic_env_test_run(
            os.path.join(TEST_CONFIG_PATH_OLD, "high_value_node_provided.yaml"),
            net_creator_type="mesh",
            n_nodes=30,
            entry_nodes=["0", "15"],
            high_value_nodes=["15", "16"],
        )
        check_env(env, warn=True)
        env.reset()

        targets = {}
        for i in range(0, N_TIME_STEPS_LONG):
            obs, rew, done, notes = env.step(
                random.randint(0, env.BLUE.get_number_of_actions() - 1)
            )
            if done:
                # add 1 to each node that gets chosen as a high value node
                for node in env.network_interface.current_graph.high_value_nodes:
                    if node not in targets:
                        targets[node] = 1
                    else:
                        targets[node] += 1

                env.reset()
        # the only 2 targets set are available
        assert len(targets.keys()) == 2

        # check that the keys are the 15 and 16 that was set
        assert set(targets.keys()).intersection(["15", "16"])

        # check that a warning was raised that the entry nodes and high value nodes intersect
        assert (
            str(w[0].message.args[0])
            == "Provided entry nodes and high value nodes intersect and may cause the training to prematurely end."
        )
