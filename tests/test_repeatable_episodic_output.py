from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import random

import pytest

custom_random_setting = {"MISCELLANEOUS":{"random_seed":random.randint(1,1000)}}

@pytest.mark.parametrize("basic_2_agent_loop",
    [
        {"episodes":2,"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml","custom_settings":custom_random_setting},
        {"episodes":2,"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml"},
        {"episodes":random.randint(5,12),"entry_nodes":["0"],"high_value_targets":["12"],"settings_file":"repeatable_threat_config.yaml"}
    ], indirect=True
)
def test_repeatable_episodic_output_set_seed(basic_2_agent_loop:ActionLoop):
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes with a set seed value
    """   

    results: List[DataFrame] = basic_2_agent_loop.standard_action_loop(deterministic=True) 

    print(results[0].compare(results[1]))
    
    assert_frame_equal(results[0],results[-1])
