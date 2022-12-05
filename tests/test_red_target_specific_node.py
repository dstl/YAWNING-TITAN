from itertools import chain
from typing import List

from pandas import DataFrame

from tests import TEST_CONFIG_PATH
from yawning_titan.envs.generic.core.action_loops import ActionLoop


def test_target_specific_node(basic_2_agent_loop: ActionLoop):
    """
    Test target specific node.

    Test to check that with no other actions available
    the RED agent will follow a prescribed path to a target node
    avoiding all other nodes
    """
    TARGET_NODE_CONFIG = TEST_CONFIG_PATH / "settable_target_node.yaml"

    nodes_on_path = ["0", "5", "7", "8", "9"]
    target_nodes = set()

    for i in range(0, 10):
        action_loop: ActionLoop = basic_2_agent_loop(
            num_episodes=1, entry_nodes=["0"], settings_path=TARGET_NODE_CONFIG
        )
        results: List[DataFrame] = action_loop.standard_action_loop()
        x = list(
            chain.from_iterable(
                chain.from_iterable(
                    [
                        [
                            info["red_info"][0]["Target_Nodes"]
                            for info in result["info"].to_list()
                        ]
                        for result in results
                    ]
                )
            )
        )
        target_nodes.update(x)

    assert all(node in nodes_on_path for node in target_nodes)
