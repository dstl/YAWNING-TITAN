from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import random

import pytest

from tests import TEST_CONFIG_PATH

REPEATABLE_TEST_CONFIG_PATH = TEST_CONFIG_PATH / "repeatable_threat_config.yaml"

custom_random_setting_1 = {"MISCELLANEOUS":{"random_seed":random.randint(1,1000)}}
custom_random_setting_2 = {"GAME_RULES":{"choose_high_value_targets_placement_at_random":True,"choose_high_value_targets_placement_manually":False}}
custom_random_setting_3 = {"GAME_RULES":{**custom_random_setting_2,"choose_entry_nodes_randomly": True}}


@pytest.mark.parametrize(
    ("episodes","entry_nodes","high_value_targets","custom_settings"),
    [
        (2,                     ["0"],["12"],custom_random_setting_1),
        (2,                     ["0"],["12"],None),
        (random.randint(50,300),["0"],["12"],None),
        (random.randint(50,300),["0"],None,  custom_random_setting_2),
        (1,                     None, None,  custom_random_setting_3)
    ]
)
def test_repeatable_episodic_output_set_random_seed(basic_2_agent_loop:ActionLoop,episodes,entry_nodes,high_value_targets,custom_settings):
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes with a set random_seed value
    """   
    action_loop:ActionLoop = basic_2_agent_loop(
        num_episodes=episodes,
        entry_nodes=entry_nodes,
        high_value_targets=high_value_targets,
        settings_file_path=REPEATABLE_TEST_CONFIG_PATH,
        custom_settings=custom_settings
    )
    results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True) 
    
    assert_frame_equal(results[0],results[-1])


def test_setting_high_value_target_with_random_seeded_randomisation(basic_2_agent_loop:ActionLoop):
    """
    Test that high value node setting is unaffected by random_seeded randomisation
    """   
    action_loop:ActionLoop = basic_2_agent_loop(
        num_episodes=1,
        entry_nodes=["0"],
        settings_file_path=REPEATABLE_TEST_CONFIG_PATH,
        custom_settings=custom_random_setting_2
    )
    target_occurrences = {str(key):0 for key in range(0,18)}
    for i in range(0,100): # run a number of action loops 
        action_loop.standard_action_loop(deterministic=True)   
        target_occurrences[action_loop.env.network_interface.get_high_value_targets()[0]] += 1

    target_occurrences = {key:val for key,val in target_occurrences.items() if val != 0}
    high_value_node_occurrences = list(target_occurrences.values())[0]
    # check that entry nodes cannot be chosen and that all high value node selected are the same
    assert len(target_occurrences) == 1 
    assert high_value_node_occurrences == 100