import os

import yawning_titan.envs.generic.core.reward_functions as reward_functions
from tests import TEST_CONFIG_PATH
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv

"""
Used to test the built in reward functions
"""


def test_standard_rewards(generate_generic_env_test_reqs):
    """
    Tests the standard reward function.

    Will raise an error if the function does not return the expected result
    """
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH, "base_config.yaml"),
        net_creator_type="mesh",
        n_nodes=5,
        entry_nodes=["0", "1", "2"],
    )

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

    reward = reward_functions.standard_rewards(reward_args)

    assert reward == -9.0769


def test_safe_gives_rewards(generate_generic_env_test_reqs):
    """
    Tests the safe_nodes_give reward function.

    Will raise an error if the function does not return the expected result
    """
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH, "base_config.yaml"),
        net_creator_type="mesh",
        n_nodes=5,
        entry_nodes=["0", "1", "2"],
    )

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


def test_punish_bad_actions(generate_generic_env_test_reqs):
    """
    Tests the punish_bad_actions function.

    Will raise an error if the function does not return the expected result
    """
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH, "base_config.yaml"),
        net_creator_type="mesh",
        n_nodes=5,
        connectivity=1,
        entry_nodes=["0", "1", "2"],
    )

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
    s = [env.network_interface.current_deceptive_nodes, 0, 0]
    env.network_interface.add_deceptive_node("1", "2")
    s[1] = env.network_interface.current_deceptive_nodes
    env.network_interface.add_deceptive_node("3", "4")
    s[2] = env.network_interface.current_deceptive_nodes

    reward = reward_functions.punish_bad_actions(reward_args)

    assert round(reward, 4) == -5
