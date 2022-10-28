from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import random

import pytest

@pytest.mark.parametrize("basic_2_agent_loop",
    [
        {"seed":666,"episodes":2,"settings_path":"settable_target_node.yaml"},
    ], indirect=True
)
def test_target_specific_node(basic_2_agent_loop:ActionLoop):
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes with a set seed value
    """

    results: List[DataFrame] = basic_2_agent_loop.standard_action_loop(deterministic=True) #basic_2_agent_loop.gif_action_loop(save_gif=True) #

    print(results[0].compare(results[1]))
    
    assert_frame_equal(results[0],results[-1])

    