from itertools import chain
from typing import List, Set

from pandas import DataFrame

from tests import TEST_CONFIG_PATH_OLD
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.networks.node import Node


def test_target_specific_node(basic_2_agent_loop: ActionLoop):
    """
    Test target specific node.

    Test to check that with no other actions available
    the RED agent will follow a prescribed path to a target node
    avoiding all other nodes
    """
    TARGET_NODE_CONFIG = TEST_CONFIG_PATH_OLD / "settable_target_node.yaml"

    nodes_on_path = ["0", "5", "7", "8", "9"]
    target_nodes: Set[Node] = set()

    for _ in range(4):
        action_loop: ActionLoop = basic_2_agent_loop(
            num_episodes=1,
            entry_nodes=["0"],
            settings_path=TARGET_NODE_CONFIG,
            raise_errors=False,
            deterministic=True,
        )
        results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True)
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
    assert all(node.name in nodes_on_path for node in target_nodes)
