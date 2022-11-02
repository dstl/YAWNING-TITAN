from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import random

import pytest

custom_random_setting_1 = {"MISCELLANEOUS":{"random_seed":random.randint(1,1000)}}
custom_random_setting_2 = {"GAME_RULES":{"choose_high_value_nodes_placement_at_random":True}}
custom_random_setting_3 = {"GAME_RULES":{"choose_high_value_nodes_placement_at_random":True,"choose_entry_nodes_randomly":True}}


@pytest.mark.parametrize("episodes,entry_nodes,high_value_nodes,settings_file,custom_settings",
    [
        [2,["0"],["12"],"repeatable_threat_config.yaml",custom_random_setting_1],
        [2,["0"],["12"],"repeatable_threat_config.yaml",None],
        [random.randint(50,300),["0"],["12"],"repeatable_threat_config.yaml",None],
        [random.randint(50,300),["0"],None,"repeatable_threat_config.yaml",custom_random_setting_2],
        [1,None,None,"repeatable_threat_config.yaml",custom_random_setting_3]
    ]
)
def test_repeatable_episodic_output_set_seed(
    basic_2_agent_loop:ActionLoop,
    episodes,
    entry_nodes,
    high_value_nodes,
    settings_file,
    custom_settings
):
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes with a set seed value
    """   
    agent_loop = basic_2_agent_loop(episodes,entry_nodes,high_value_nodes,settings_file,custom_settings)
    results: List[DataFrame] = agent_loop.standard_action_loop(deterministic=True) 

    #print(results[0].compare(results[1]))
    
    assert_frame_equal(results[0],results[-1])


def test_setting_high_value_target_with_seeded_randomisation(basic_2_agent_loop:ActionLoop):
    """
    Test that high value node setting is unaffected by seeded randomisation
    """   
    agent_loop = basic_2_agent_loop(entry_nodes=['0'],settings_file="repeatable_threat_config.yaml",custom_settings=custom_random_setting_2)
    high_value_nodes = set()
    for i in range(0,100): # run a number of action loops 
        agent_loop.standard_action_loop(deterministic=True)   
        high_value_nodes.add(agent_loop.env.network_interface.get_high_value_nodes()[0])

    # check that entry nodes cannot be chosen and that all high value node selected are the same
    assert len(high_value_nodes) == 1 
    assert list(high_value_nodes)[0] != '0'
