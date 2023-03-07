from itertools import chain
from typing import List, Set

import pytest
from pandas import DataFrame

from yawning_titan.networks.node import Node


@pytest.mark.skip(
    reason="Failing tests. Needs to be looked at. Bug ticket " "raised (AIDT-260)."
)
@pytest.mark.integration_test
def test_target_specific_node(
    basic_2_agent_loop,
    create_yawning_titan_run,
):
    """
    Test target specific node.

    Test to check that with no other actions available the RED agent will
    follow a prescribed path to a target node avoiding all other nodes.
    """
    yt_run = create_yawning_titan_run(
        game_mode_name="settable_target_node",
        network_name="Default 18-node network",
        deterministic=True,
    )

    nodes_on_path = ["0", "5", "7", "8", "9"]
    captured_nodes: Set[Node] = set()

    for _ in range(0, 10):
        action_loop = basic_2_agent_loop(yt_run)
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

    captured_node_names = [node.name for node in captured_nodes]
    print(f"{nodes_on_path=}")
    print(f"{captured_node_names=}")
    assert all(node in nodes_on_path for node in captured_node_names)


@pytest.mark.integration_test
def test_target_node_capture_ends_game(
    basic_2_agent_loop,
    create_yawning_titan_run,
):
    """Test that capturing the target node will end the game when the `lose_when_target_node_lost` option is True."""
    yt_run = create_yawning_titan_run(
        game_mode_name="settable_target_node", network_name="Default 18-node network"
    )

    action_loop = basic_2_agent_loop(yt_run)
    results: List[DataFrame] = action_loop.standard_action_loop()

    result = results[0]
    info = result["info"].to_list()[-1]

    assert info["red_info"][0]["Target_Nodes"][0].to_dict()["name"] == "9"
    assert info["red_info"][0]["Successes"][0]
    assert info["post_red_red_location"].to_dict()["name"] == "9"


@pytest.mark.integration_test
def test_target_node_capture_doesnt_end_game(
    basic_2_agent_loop,
    create_yawning_titan_run,
):
    """Test that capturing the target node will not end the game when the `lose_when_target_node_lost` option is False."""
    yt_run = create_yawning_titan_run(
        game_mode_name="settable_target_game_continue",
        network_name="Default 18-node network",
    )

    action_loop = basic_2_agent_loop(yt_run)
    results: List[DataFrame] = action_loop.standard_action_loop(deterministic=True)

    result = results[0]
    assert (result["info"].to_list()[-1]["safe_nodes"] == 0) or (
        action_loop.env.current_duration
        == action_loop.env.network_interface.game_mode.game_rules.max_steps.value
    )
