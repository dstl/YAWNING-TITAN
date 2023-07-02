"""Tests the built-in reward functions."""

import pytest

import yawning_titan.envs.generic.core.reward_functions as reward_functions


@pytest.mark.integration_test
def test_standard_rewards(create_yawning_titan_run):
    """
    Tests the standard reward function.

    Will raise an error if the function does not return the expected result
    """
    yt_run = create_yawning_titan_run(
        game_mode_name="Default Game Mode", network_name="mesh_5"
    )
    env = yt_run.env

    assert hasattr(reward_functions, "standard_rewards")

    # calculates the reward from the current state of the network
    reward_args = {
        "network_interface": env.network_interface,
        "blue_action": "make_node_safe",
        "blue_node": "2",
        "start_state": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
        "end_state": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
        "start_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
        "end_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
        "start_isolation": {"0": False, "1": False, "2": False, "3": False, "4": False},
        "end_isolation": {"0": False, "1": False, "2": False, "3": False, "4": False},
        "start_blue": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
        "end_blue": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
    }

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == -3.5

    reward_args["end_state"] = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 0}

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == 0.2261

    reward_args["end_vulnerabilities"] = {
        "0": 0.2,
        "1": 0.5,
        "2": 0.5,
        "3": 0.1,
        "4": 0.5,
    }
    reward_args["blue_action"] = "reduce_vulnerability"

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == 2.5261

    reward_args["blue_action"] = "do_nothing"

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == -0.0739

    reward_args["blue_action"] = "make_node_safe"
    reward_args["start_state"] = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}
    reward_args["end_state"] = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == -3.5

    reward_args["blue_action"] = "isolate"
    reward_args["start_state"] = {"0": 1, "1": 0, "2": 1, "3": 0, "4": 0}
    reward_args["end_state"] = {"0": 0, "1": 0, "2": 1, "3": 0, "4": 0}
    reward_args["start_vulnerabilities"] = {
        "0": 0.5,
        "1": 0.5,
        "2": 0.5,
        "3": 0.5,
        "4": 0.5,
    }
    reward_args["end_vulnerabilities"] = {
        "0": 0.1,
        "1": 0.5,
        "2": 0.5,
        "3": 0.5,
        "4": 0.5,
    }
    reward_args["end_isolation"] = {
        "0": True,
        "1": False,
        "2": False,
        "3": False,
        "4": False,
    }

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == -0.0769

    # check that isolating a node punishment applies per node
    reward_args["end_isolation"] = {
        "0": True,
        "1": True,
        "2": False,
        "3": False,
        "4": False,
    }

    reward = reward_functions.standard_rewards(reward_args)

    assert round(reward, 4) == (-0.0769 - 1)


@pytest.mark.integration_test
def test_safe_gives_rewards(create_yawning_titan_run):
    """
    Tests the safe_nodes_give reward function.

    Will raise an error if the function does not return the expected result
    """
    yt_run = create_yawning_titan_run(
        game_mode_name="Default Game Mode", network_name="mesh_5"
    )
    env = yt_run.env

    assert hasattr(reward_functions, "safe_nodes_give_rewards")

    # calculates the reward from the current state of the network
    reward_args = {
        "network_interface": env.network_interface,
        "blue_action": "make_node_safe",
        "blue_node": "2",
        "start_state": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
        "end_state": {"0": 1, "1": 1, "2": 0, "3": 1, "4": 0},
        "start_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
        "end_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
    }

    reward = reward_functions.safe_nodes_give_rewards(reward_args)

    assert round(reward, 4) == 2

    reward_args["end_state"] = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 0}

    reward = reward_functions.safe_nodes_give_rewards(reward_args)

    assert round(reward, 4) == 1

    reward_args["end_state"] = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}

    reward = reward_functions.safe_nodes_give_rewards(reward_args)

    assert round(reward, 4) == 5


@pytest.mark.integration_test
def test_punish_bad_actions(create_yawning_titan_run):
    """
    Tests the punish_bad_actions function.

    Will raise an error if the function does not return the expected result
    """
    yt_run = create_yawning_titan_run(
        game_mode_name="Default Game Mode", network_name="mesh_5"
    )
    env = yt_run.env
    assert hasattr(reward_functions, "punish_bad_actions")

    # calculates the reward from the current state of the network
    reward_args = {
        "network_interface": env.network_interface,
        "blue_action": "make_node_safe",
        "blue_node": "2",
        "start_state": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1},
        "end_state": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 0},
        "start_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
        "end_vulnerabilities": {"0": 0.5, "1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5},
    }

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == 0

    reward_args["end_state"] = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1}

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == -1

    reward_args["blue_action"] = "do_nothing"

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == -2.5

    reward_args["blue_action"] = "reduce_vulnerability"

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == -1

    reward_args["blue_action"] = "add_deceptive_node"

    node_1 = env.network_interface.current_graph.get_node_from_name("1")
    node_2 = env.network_interface.current_graph.get_node_from_name("2")
    node_3 = env.network_interface.current_graph.get_node_from_name("3")
    node_4 = env.network_interface.current_graph.get_node_from_name("4")

    env.network_interface.add_deceptive_node(node_1, node_2)
    env.network_interface.add_deceptive_node(node_3, node_4)

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == -5
