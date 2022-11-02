from typing import List
from yawning_titan.envs.generic.core.action_loops import ActionLoop

from pandas import DataFrame
from itertools import chain


def test_target_specific_node(basic_2_agent_loop:ActionLoop):
    """
    Test to check that with no other actions available
    the RED agent will follow a prescribed path to a target node
    avoiding all other nodes
    """
    
    nodes_on_path = ['0','5','7','8','9']
    target_nodes = set()

    for i in range(0,10):   
        action_loop = basic_2_agent_loop(episodes=1,entry_nodes=["0"],settings_file="settable_target_node.yaml")
        results: List[DataFrame] = action_loop.standard_action_loop()
        x = list(chain.from_iterable(chain.from_iterable([[info['red_info'][0]['Target_Nodes'] for info in result['info'].to_list()] for result in results])))
        target_nodes.update(x)
    

    assert all(node in nodes_on_path for node in target_nodes)


    