from itertools import chain
from typing import List

from pandas import DataFrame

from tests import TEST_CONFIG_PATH_OLD
from yawning_titan.envs.generic.core.action_loops import ActionLoop


def test_target_specific_node(basic_2_agent_loop: ActionLoop):
    """
    Test target specific node.

    Test to check that with no other actions available
    the RED agent will follow a prescribed path to a target node
    avoiding all other nodes
    """
    TARGET_NODE_CONFIG = TEST_CONFIG_PATH_OLD / "settable_target_node.yaml"

    nodes_on_path = ["0", "5", "7", "8", "9"]
    captured_nodes = set()

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
        captured_nodes.update(x)

    assert all(node in nodes_on_path for node in captured_nodes)


def test_target_node_capture_ends_game(basic_2_agent_loop):
    """Test that capturing the target node will end the game when the `lose_when_target_node_lost` option is True."""
    TARGET_NODE_CONFIG = TEST_CONFIG_PATH_OLD / "settable_target_node.yaml"

    action_loop: ActionLoop = basic_2_agent_loop(
        num_episodes=1, entry_nodes=["0"], settings_path=TARGET_NODE_CONFIG
    )
    results: List[DataFrame] = action_loop.standard_action_loop()

    result = results[0]
    info = result["info"].to_list()[-1]

    assert info["red_info"][0]["Target_Nodes"][0] == "9"
    assert info["red_info"][0]["Successes"][0]
    assert info["post_red_red_location"] == "9"


def test_target_node_capture_doesnt_end_game(basic_2_agent_loop):
    """Test that capturing the target node will not end the game when the `lose_when_target_node_lost` option is False."""
    TARGET_NODE_DONT_END_CONFIG = (
        TEST_CONFIG_PATH_OLD / "settable_target_game_continue.yaml"
    )

    action_loop: ActionLoop = basic_2_agent_loop(
        num_episodes=1, settings_path=TARGET_NODE_DONT_END_CONFIG
    )
    results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True)

    result = results[0]
    assert result["info"].to_list()[-1]["safe_nodes"] == 0
