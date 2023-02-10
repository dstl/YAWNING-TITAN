import random
from collections import defaultdict
from typing import List

import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from tests import TEST_CONFIG_PATH_OLD
from yawning_titan.envs.generic.core.action_loops import ActionLoop

REPEATABLE_TEST_CONFIG_PATH = TEST_CONFIG_PATH_OLD / "repeatable_threat_config.yaml"

custom_random_setting_1 = {"MISCELLANEOUS": {"random_seed": random.randint(1, 1000)}}


@pytest.mark.parametrize(
    ("episodes", "entry_node_names", "high_value_node_names", "custom_settings"),
    [
        (2, ["0"], ["12"], custom_random_setting_1),
        (2, ["0"], ["12"], None),
        (random.randint(10, 50), ["0"], ["12"], None),
        (random.randint(10, 50), ["0"], None, None),
        (1, None, None, None),
    ],
)
def test_repeatable_episodic_output_set_random_seed(
    basic_2_agent_loop: ActionLoop,
    episodes,
    entry_node_names,
    high_value_node_names,
    custom_settings,
):
    """Tests that actions undertaken by the red agent are repeatable with a set random_seed value."""
    action_loop: ActionLoop = basic_2_agent_loop(
        num_episodes=episodes,
        entry_node_names=entry_node_names,
        high_value_node_names=high_value_node_names,
        settings_path=REPEATABLE_TEST_CONFIG_PATH,
        custom_settings=custom_settings,
    )
    results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True)

    assert_frame_equal(results[0], results[-1])


def test_setting_high_value_node_with_random_seeded_randomisation(
    basic_2_agent_loop: ActionLoop,
):
    """Test that high value node setting is unaffected by random_seeded randomisation."""
    action_loop: ActionLoop = basic_2_agent_loop(
        num_episodes=1,
        entry_node_names=["0"],
        settings_path=REPEATABLE_TEST_CONFIG_PATH,
    )
    target_occurrences = defaultdict(lambda: 0)
    for _ in range(0, 50):  # run a number of action loops
        action_loop.standard_action_loop(deterministic=True)
        target_occurrences[
            action_loop.env.network_interface.current_graph.high_value_nodes[0]
        ] += 1

    high_value_nodes = list(n for n in target_occurrences.values() if n > 0)

    # check that entry nodes cannot be chosen and that all high value node selected are the same
    assert len(high_value_nodes) == 1
    assert list(high_value_nodes)[0] != "0"
