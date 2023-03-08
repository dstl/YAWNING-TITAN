import random
from collections import defaultdict
from typing import List

import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from yawning_titan.db.doc_metadata import DocMetadataSchema
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.yawning_titan_run import YawningTitanRun


@pytest.mark.integration_test()
@pytest.mark.parametrize(
    ("episodes", "use_custom_settings"),
    [
        (2, True),
        (2, False),
        (1, False),
    ],
)
def test_repeatable_episodic_output_set_random_seed(
    basic_2_agent_loop, episodes, use_custom_settings, game_mode_db, default_network
):
    """Tests that actions undertaken by the red agent are repeatable with a set random_seed value."""
    game_mode = game_mode_db.search(
        DocMetadataSchema.NAME == "repeatable_threat_config"
    )[0]

    if use_custom_settings:
        game_mode.miscellaneous.random_seed = random.randint(1, 1000)

    yt_run = YawningTitanRun(
        network=default_network,
        game_mode=game_mode,
        collect_additional_per_ts_data=True,
        total_timesteps=1000,
        eval_freq=1000,
        deterministic=True,
    )
    action_loop: ActionLoop = basic_2_agent_loop(
        yt_run=yt_run,
        num_episodes=episodes,
    )
    results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True)

    assert_frame_equal(results[0], results[-1])


@pytest.mark.integration_test
def test_setting_high_value_node_with_random_seeded_randomisation(
    basic_2_agent_loop,
    create_yawning_titan_run,
):
    """Test that high value node setting is unaffected by random_seeded randomisation."""
    yt_run = create_yawning_titan_run(
        game_mode_name="repeatable_threat_config",
        network_name="Default 18-node network",
    )
    action_loop: ActionLoop = basic_2_agent_loop(
        yt_run=yt_run,
        num_episodes=1,
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
