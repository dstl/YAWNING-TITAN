import random
import warnings

import pytest
from stable_baselines3.common.env_checker import check_env

from tests.conftest import create_yawning_titan_run
from tests.generic_environment import N_TIME_STEPS_LONG

# Dummy line to 'use' demo_db_docs so flake8 doesn't throw F401 or F811
_ = create_yawning_titan_run


@pytest.mark.integration_test
@pytest.mark.skip(
    reason="Assertion fails due to the emergence of a new warning: 'non-integer"
    " arguments to randrange() have been deprecated since Python 3.10 and "
    "will be removed in a subsequent version'"
)
def test_high_value_node_and_entry_nodes_matching(create_yawning_titan_run):
    """
    Test the high value node gaol mechanic - manually passed to.

    .. todo::
        Needs a custom network creating for this specific test and adding to
        tests/_package_data/networks.json.
    """
    with warnings.catch_warnings(record=True) as w:
        yt_run = create_yawning_titan_run(
            game_mode_name="high_value_node_provided",
            network_name="mesh_18"
        )
        env = yt_run.env
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
