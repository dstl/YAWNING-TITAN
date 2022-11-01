from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import random

import pytest

custom_random_setting_1 = {"MISCELLANEOUS":{"random_seed":random.randint(1,1000)}}
custom_random_setting_2 = {"GAME_RULES":{"choose_high_value_targets_placement_at_random":True}}
custom_random_setting_3 = {"GAME_RULES":{"choose_high_value_targets_placement_at_random":True,"choose_entry_nodes_randomly": False}}


@pytest.mark.parametrize("basic_2_agent_loop",
    [
        {"episodes":2,"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml","custom_settings":custom_random_setting_1},
        {"episodes":2,"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml"},
        {"episodes":random.randint(50,300),"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml"},
        {"episodes":random.randint(50,300),"entry_nodes":["0"],"settings_file":"repeatable_threat_config.yaml","custom_settings":custom_random_setting_2},
        {"episodes":1,"settings_file":"repeatable_threat_config.yaml","custom_settings":custom_random_setting_3}
    ], indirect=True
)
def test_repeatable_episodic_output_set_seed(basic_2_agent_loop:ActionLoop):
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes with a set seed value
    """   

    results: List[DataFrame] = basic_2_agent_loop.standard_action_loop(deterministic=True) 

    #print(results[0].compare(results[1]))
    
    assert_frame_equal(results[0],results[-1])

@pytest.mark.parametrize("basic_2_agent_loop",
    [
        {"episodes":1,"entry_nodes":["0"],"settings_file":"repeatable_threat_config.yaml"}
    ], indirect=True
)
def test_setting_high_value_target_with_seeded_randomisation(basic_2_agent_loop:ActionLoop):
    """
    Test that high value node setting is unaffected by seeded randomisation
    """   
    target_occurrences = {str(key):0 for key in range(0,18)}
    for i in range(0,100): # run a number of action loops 
        basic_2_agent_loop.standard_action_loop(deterministic=True)   
        target_occurrences[basic_2_agent_loop.env.network_interface.get_high_value_targets()[0]] += 1

    target_occurrences = {key:val for key,val in target_occurrences.items() if val != 0}
    high_value_node_occurrences = list(target_occurrences.values())[0]
    # check that entry nodes cannot be chosen and that all high value node selected are the same
    assert len(target_occurrences) == 1 
    assert high_value_node_occurrences == 100