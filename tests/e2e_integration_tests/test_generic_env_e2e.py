"""Used to test the GenericEnv() class and the associated agent interfaces."""
import random
from collections import defaultdict
from typing import Dict, List, Tuple, Union

import networkx as nx
import numpy as np
import pytest

from tests.conftest import N_TIME_STEPS
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.networks.node import Node


class RandomGen:
    """Used to ensure that every action is chosen but also that there are random actions chosen."""

    def __init__(self, number_actions):
        self.number_of_actions = number_actions
        self.possible_actions = [i for i in range(0, number_actions)]
        self.test_repeat = False
        self.amount = 5
        self.repeat_action = 0

    def get_action(self):
        """Return an action."""
        if not self.test_repeat:
            if random.randint(0, 20) > 19:
                self.test_repeat = True
                self.repeat_action = random.randint(0, self.number_of_actions)

        if self.test_repeat:
            self.amount -= 1
            if self.amount <= 0:
                self.test_repeat = False
                self.amount = 5
            return self.repeat_action

        chosen_action = random.choice(self.possible_actions)
        self.possible_actions.remove(chosen_action)
        if len(self.possible_actions) == 0:
            self.possible_actions = [i for i in range(0, self.number_of_actions)]
        return chosen_action


@pytest.mark.e2e_integration_test
@pytest.mark.parametrize(
    ("game_mode_name", "network_name"),
    [
        ("Default Game Mode", "Default 18-node network"),
        ("Default Game Mode", "mesh_18"),
        ("Default Game Mode", "mesh_50"),
        ("red_config_test_1", "mesh_50"),
        ("red_config_test_2", "mesh_50"),
        ("red_config_test_3", "mesh_50"),
        ("red_config_test_4", "mesh_5"),
        ("red_config_test_5", "mesh_24"),
    ],
)
def test_generic_env_e2e(
    game_mode_name: str, network_name: str, create_yawning_titan_run
):
    """Test the generic environment end to end."""
    # Counters for later
    counts = {
        "red_action_count": {
            True: defaultdict(lambda: 0),
            False: defaultdict(lambda: 0),
        },
        "multi_attack": {True: defaultdict(lambda: 0), False: defaultdict(lambda: 0)},
        "blue_action_count": defaultdict(lambda: 0),
        "discovered_from_scanning": 0,
        "discovered_immediately_counter": 0,
        "nodes_missed_scan": 0,
        "number_of_resets": 0,
        "deceptive_counter": 0,
        "wins": 0,
        "scan_used": False,
    }

    yt_run = create_yawning_titan_run(game_mode_name, network_name)

    env: GenericNetworkEnv = yt_run.env
    env.reset()

    random_action_generator = RandomGen(env.BLUE.get_number_of_actions())

    prev_high_value = None
    for _ in range(N_TIME_STEPS):
        current_chosen_action = random_action_generator.get_action()
        obs, rew, done, episode = env.step(current_chosen_action)

        counts = calculate_counts(episode, counts, done)

        check_network_characteristics(done, env, episode, prev_high_value)
        check_observation_space(env, obs)
        check_attacks_come_from_connected_node(env, episode)
        check_blue_actions(env, episode, current_chosen_action)

        # Blue actions

        if episode["blue_action"] in ["restore_node", "make_node_safe"]:
            counts = check_blue_restore_node_action(episode, counts)
        elif episode["blue_action"] == "isolate":
            check_blue_isolate_action(env, episode)
        elif episode["blue_action"] == "connect":
            check_blue_connect_action(env, episode)
        elif episode["blue_action"] == "reduce_vulnerability":
            check_blue_reduce_vulnerability_action(episode)
        elif episode["blue_action"] == "scan":
            counts = check_blue_scan_action(env, episode, counts)
        elif episode["blue_action"] == "add_deceptive_node":
            check_blue_add_deceptive_node_action(env, episode)
        elif episode["blue_action"] in ["do_nothing", "failed"]:
            check_blue_do_nothing_or_fail_action(episode)
        else:
            raise AssertionError("Missing blue action:" + episode["blue_action"])

        # Red actions

        for action in episode["red_info"].values():
            if action["Action"] == "basic_attack":
                counts = check_red_basic_attack(env, action, episode, counts)
            elif action["Action"] == "zero_day":
                counts = check_red_zero_day_action(action, episode, counts)
            elif action["Action"] in ["spread", "intrude"]:
                counts = check_red_spread_or_intrude_action(action, episode, counts)
            elif action["Action"] == "random_move":
                check_red_random_move_action(env, action, episode)
            elif action["Action"] == "do_nothing":
                check_red_do_nothing_action(episode)
            elif action["Action"] == "no_possible_targets":
                check_red_no_possible_targets(env, episode)
            elif action["Action"] != "natural_spread":
                raise AssertionError("Missing red action:" + action["Action"])

        if done:
            counts = check_when_done(env, counts)
            env.reset()
        else:
            check_when_not_done(env)

    check_when_complete(env, counts, N_TIME_STEPS)
    env.close()


def calculate_counts(
    episode: Dict[str, dict], counts: Dict[str, dict], done
) -> Dict[str, dict]:
    """Populate the counts dictionary."""
    # used to calculate number of successes and failures for different actions
    counts["blue_action_count"][episode["blue_action"]] += 1

    if done and not episode["blue_action"] == "failed":
        counts["wins"] += 1

    for action in episode["red_info"].values():
        red_action = action["Action"]
        red_success = action["Successes"]
        if red_action != "natural_spread" and red_action != "no_possible_targets":
            if red_action != "spread" and red_action != "intrude":
                # if a action that targets a single node succeeds or fails
                for i in red_success:
                    counts["red_action_count"][i][red_action] += 1

            else:
                # multi-node target
                overall_success = True in red_success

                # adds one attack action to the red action count (this is so actions can easily be counted to max
                # timesteps)

                counts["red_action_count"][overall_success][red_action] += 1

                # counts all the individual successes and failures against the nodes
                for success in red_success:
                    counts["multi_attack"][success][red_action] += 1
    return counts


def check_network_characteristics(
    done: bool, env: GenericNetworkEnv, episode: Dict, prev_high_value: Node
):
    """Check the attributes of the `Network` in the given episode."""
    red_info: Dict = episode["red_info"]
    initial_edges = env.network_interface.base_graph.number_of_edges()
    post_red_state: Dict[str, Node] = episode["post_red_state"]

    # natural spreading
    ns = list(filter(lambda x: x["Action"] == "natural_spread", red_info.values()))
    assert len(ns) == 1 or len(ns) == 0
    if len(ns) == 1:
        ns = ns[0]
        target_nodes: List[Node] = ns["Target_Nodes"]
        for i in [
            index
            for index, attack_success in enumerate(ns["Successes"])
            if attack_success
        ]:
            assert post_red_state[target_nodes[i].uuid] == 1

    # random high value node placement
    if not done:
        if not env.network_interface.current_graph.set_random_high_value_nodes:
            assert (
                env.network_interface.current_graph.high_value_nodes == prev_high_value
                or prev_high_value is None
            )

    assert (
        env.network_interface.adj_matrix.all()
        == nx.to_numpy_array(env.network_interface.current_graph).all()
    )
    # cannot place too many deceptive nodes
    assert (
        initial_edges
        <= env.network_interface.base_graph.number_of_edges()
        <= (
            initial_edges
            + env.network_interface.game_mode.blue.action_set.deceptive_nodes.max_number.value
        )
    )


def check_attacks_come_from_connected_node(env: GenericNetworkEnv, episode: Dict):
    """Test that attacks come from a connected node."""
    attacks: List[List[Node]] = episode["attacks"]
    initial_state: Dict = episode["initial_state"]
    blue_action = episode["blue_action"]
    blue_node: Node = episode["blue_node"]

    red_info = episode["red_info"]
    initial_graph = episode["initial_graph"]

    prev_attacks = []

    for nodes in attacks:
        assert (
            nodes[0] is None
            or initial_state[nodes[0].uuid] == 1
            or nodes[0] in prev_attacks
        )
        assert initial_state[nodes[1].uuid] == 0
        prev_attacks.append(nodes[1])
        if blue_action != "isolate" and blue_action != "add_deceptive_node":
            if nodes[0] not in env.network_interface.get_current_connected_nodes(
                nodes[1]
            ) + [None]:
                raise AssertionError(
                    nodes,
                    env.network_interface.get_current_connected_nodes(nodes[0]),
                    blue_action,
                    blue_node,
                    red_info,
                )
        elif blue_action == "isolate" and nodes[1] == blue_node:
            if nodes[0] is not None:
                assert nodes[0] in list(nx.Graph(initial_graph).neighbors(blue_node))
        elif blue_action == "add_deceptive_node" and nodes[1] == blue_node[0]:
            if blue_node in nx.Graph(initial_graph):
                assert nodes[0] in list(nx.Graph(initial_graph).neighbors(blue_node[0]))


def check_observation_space(env: GenericNetworkEnv, obs):
    """Check the observation space in the environments current episode."""
    # observation space is correct
    adj_matrix = nx.to_numpy_array(env.network_interface.current_graph)
    open_spaces = env.network_interface.get_number_unused_deceptive_nodes()
    adj_matrix = np.pad(adj_matrix, (0, open_spaces), "constant").flatten()
    if env.network_interface.game_mode.observation_space.node_connections.value:
        assert np.array_equal(obs[: len(adj_matrix)], adj_matrix)

    observation_size = env.calculate_observation_space_size(with_feather=False)

    # assert the observation space is the correct size
    assert env.network_interface.get_observation_size() == observation_size


def check_when_done(env: GenericNetworkEnv, counts: dict):
    """Check that the state of the environment is correct when the game mode is done."""
    if (
        env.current_duration > 500
        and env.network_interface.current_graph.number_of_nodes() < 15
    ):
        if (
            env.network_interface.game_mode.blue.action_set.make_node_safe.use.value
            or env.network_interface.game_mode.blue.action_set.restore_node.value
        ):
            if any(
                n.deceptive_node
                for n in env.network_interface.current_graph.get_nodes()
            ):
                assert counts["deceptive_counter"] != 0
    if (
        env.current_duration
        != env.network_interface.game_mode.game_rules.max_steps.value
    ):
        if (
            env.network_interface.game_mode.game_rules.blue_loss_condition.all_nodes_lost.value
        ):
            assert (
                len(
                    env.network_interface.current_graph.get_nodes(filter_true_safe=True)
                )
                == 0
            )
        if (
            env.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.use.value
        ):
            assert (
                (
                    len(
                        env.network_interface.current_graph.get_nodes(
                            filter_true_compromised=True
                        )
                    )
                    / len(env.network_interface.current_graph.get_nodes())
                )
                >= env.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.value.value
            )
        if (
            env.network_interface.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value
        ):
            # the game ends when a high value node is compromised, this needs to be checked
            compromised_hvn = False

            for node in env.network_interface.current_graph.high_value_nodes:
                if node.true_compromised_status == 1:
                    compromised_hvn = True
                    break

            assert compromised_hvn is True
    counts["number_of_resets"] += 1
    return counts


def check_when_not_done(env: GenericNetworkEnv):
    """Check that the state of the environment is correct when the game mode is not done."""
    if (
        env.network_interface.game_mode.game_rules.blue_loss_condition.all_nodes_lost.value
    ):
        assert (
            len(env.network_interface.current_graph.get_nodes(filter_true_safe=True))
            != 0
        )
    if (
        env.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.use.value
    ):
        assert (
            (
                len(
                    env.network_interface.current_graph.get_nodes(
                        filter_true_compromised=True
                    )
                )
                / len(env.network_interface.current_graph.get_nodes())
            )
            < env.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.value.value
        )
    if (
        env.network_interface.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value
    ):
        # the game would end if a high value node was compromised, this needs to be checked
        compromised_hvn = False

        # check that none of the high value nodes are compromised
        for node in env.network_interface.current_graph.high_value_nodes:
            # get_single_node_state returns 1 if compromised
            if node.true_compromised_status == 1:
                compromised_hvn = True

        assert compromised_hvn is False


def check_when_complete(env: GenericNetworkEnv, counts: dict, timesteps: int):
    """Check that the state of the environment is correct when the game mode is complete."""
    if (
        not env.network_interface.game_mode.blue.action_set.deceptive_nodes.use.value
        and counts["scan_used"]
        and (counts["nodes_missed_scan"] + counts["discovered_from_scanning"]) > 0
    ):
        assert (
            (
                0.95
                * env.network_interface.game_mode.blue.intrusion_discovery_chance.on_scan.standard_node.value
            )
            < (
                counts["discovered_from_scanning"]
                / (counts["nodes_missed_scan"] + counts["discovered_from_scanning"])
            )
            < (
                1.05
                * env.network_interface.game_mode.blue.intrusion_discovery_chance.on_scan.standard_node.value
            )
        )

    assert (
        sum(counts["red_action_count"][True].values())
        + sum(counts["red_action_count"][False].values())
        == timesteps
    )
    assert sum(counts["blue_action_count"].values()) == timesteps

    if "failed" in counts["blue_action_count"]:
        assert (
            counts["number_of_resets"]
            == counts["blue_action_count"]["failed"] + counts["wins"]
        )
    else:
        assert counts["wins"] == counts["number_of_resets"]


# Blue action checks


def check_blue_actions(
    env: GenericNetworkEnv, episode: Dict, current_chosen_action: int
):
    """Check that the state of the environment is correct for an episode after a generic Blue agent action."""
    blue_action = episode["blue_action"]
    blue_node: Node = episode["blue_node"]  # TODO: return blue_node uuid
    initial_state: Dict[str, dict] = episode["initial_state"]
    initial_red_location = episode["initial_red_location"]
    post_red_red_location = episode["post_red_red_location"]
    final_red_location = episode["final_red_location"]

    if current_chosen_action > env.action_space.n:
        assert blue_action == "do_nothing"

        # red location (if using the red can only attack from central red node)
        if initial_red_location is None:
            assert (
                post_red_red_location in env.network_interface.current_graph.entry_nodes
                or post_red_red_location is None
            )
        elif post_red_red_location is None:
            assert final_red_location is None
        else:
            if blue_action != "add_deceptive_node":
                connected = env.network_interface.get_current_connected_nodes(
                    post_red_red_location
                )
                connected = [n for n in connected if n.true_compromised_status == 1]
                if len(connected) == 0:
                    assert final_red_location == post_red_red_location or (
                        (
                            blue_action == "restore_node"
                            or blue_action == "make_node_safe"
                        )
                        and blue_node == post_red_red_location
                        and final_red_location is None
                    )
                else:
                    if blue_action == "restore_node" or blue_action == "make_node_safe":
                        if blue_node == post_red_red_location:
                            assert final_red_location in connected
                    else:
                        assert post_red_red_location == final_red_location
        if initial_red_location is None:
            connected = env.network_interface.current_graph.entry_nodes
        else:
            connected = env.network_interface.get_current_connected_nodes(
                initial_red_location
            )
        if blue_action != "isolate" or (
            blue_node != post_red_red_location and blue_node != initial_red_location
        ):
            if blue_action != "add_deceptive_node":
                assert (
                    post_red_red_location in connected
                    or post_red_red_location == initial_red_location
                )

        assert 0 in initial_state.values()


def check_blue_restore_node_action(episode: Dict[str, dict], counts: dict) -> int:
    """Check that the state of the environment is correct for an episode where the Blue agent restores a nodes vulnerability state."""
    blue_node: Node = episode["blue_node"]
    assert episode["end_state"][blue_node.uuid] != 1
    if blue_node.deceptive_node:
        counts["deceptive_counter"] += 1
    return counts


def check_blue_isolate_action(env: GenericNetworkEnv, episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Blue agent isolates a node."""
    blue_node: Node = episode["blue_node"]
    assert len(env.network_interface.get_current_connected_nodes(blue_node)) == 0
    assert blue_node.isolated


def check_blue_connect_action(env: GenericNetworkEnv, episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Blue agent reconnects 2 nodes."""
    blue_node: Node = episode["blue_node"]

    for cn in env.network_interface.get_current_connected_nodes(blue_node):
        assert not cn.isolated
    for bn in env.network_interface.get_base_connected_nodes(blue_node):
        cn = env.network_interface.current_graph.get_node_from_uuid(bn.uuid)
        if not cn.isolated:  # check corresponding node on current graph
            assert cn in env.network_interface.get_current_connected_nodes(blue_node)
        assert not blue_node.isolated


def check_blue_reduce_vulnerability_action(episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Blue agent reduces a nodes vulnerability."""
    blue_node: Node = episode["blue_node"]
    assert 0 < episode["final_vulnerabilities"][blue_node.uuid] < 1
    assert (
        episode["final_vulnerabilities"][blue_node.uuid]
        <= episode["final_vulnerabilities"][blue_node.uuid]
    )


def check_blue_scan_action(
    env: GenericNetworkEnv, episode: Dict[str, dict], counts: dict
):
    """Check that the state of the environment is correct for an episode where the Blue agent scans."""
    counts["scan_used"] = True
    for node in env.network_interface.current_graph.get_nodes():
        if episode["initial_blue_view"][node.uuid] == 1:
            assert episode["end_blue_view"][node.uuid] == 1

        if (
            episode["post_red_blue_view"][node.uuid] == 0
            and episode["end_blue_view"][node.uuid] == 1
        ):
            counts["discovered_from_scanning"] += 1

        if episode["end_state"][node.uuid] != episode["end_blue_view"][node.uuid]:
            counts["nodes_missed_scan"] += 1
        if not node.deceptive_node:
            if (
                env.network_interface.game_mode.blue.intrusion_discovery_chance.on_scan.standard_node.value
                == 1
            ):
                if episode["end_state"][node.uuid] == 1:
                    assert episode["end_blue_view"][node.uuid] == 1
        else:
            if (
                env.network_interface.game_mode.blue.intrusion_discovery_chance.on_scan.deceptive_node.value
                == 1
            ):
                if episode["end_state"][node.uuid] == 1:
                    assert episode["end_blue_view"][node.uuid] == 1

    return counts


def check_blue_add_deceptive_node_action(
    env: GenericNetworkEnv, episode: Dict[str, dict]
):
    """Check that the state of the environment is correct for an episode where the Blue uses a deceptive node."""
    blue_nodes: List[Union[Node, Tuple[Node]]] = episode["blue_node"]
    deceptive_node = env.network_interface.current_graph.get_node_from_uuid(
        blue_nodes[0].uuid
    )
    node1 = blue_nodes[1][0]
    node2 = blue_nodes[1][1]
    assert node2 not in env.network_interface.get_base_connected_nodes(node1)
    assert [
        i
        for i in env.network_interface.get_base_connected_nodes(deceptive_node)
        if i != node1 and i != node2
    ] == []
    for n in env.network_interface.current_graph.get_nodes():
        if n != node1 and n != node2:
            assert deceptive_node not in env.network_interface.get_base_connected_nodes(
                n
            )
    assert env.network_interface.current_deceptive_nodes != 0
    assert deceptive_node.vulnerability_score is not None
    assert deceptive_node.true_compromised_status is not None

    if deceptive_node.uuid in episode["post_red_state"]:
        if (
            env.network_interface.game_mode.blue.action_set.deceptive_nodes.new_node_on_relocate.value
        ):
            if episode["post_red_state"][deceptive_node.uuid] == 1:
                assert episode["end_state"][deceptive_node.uuid] == 0
                assert not deceptive_node.isolated
        else:
            assert (
                episode["end_state"][deceptive_node.uuid]
                == episode["post_red_state"][deceptive_node.uuid]
            )
            assert (
                episode["final_vulnerabilities"][deceptive_node.uuid]
                == episode["post_red_vulnerabilities"][deceptive_node.uuid]
            )
            assert (
                episode["end_blue_view"][deceptive_node.uuid]
                == episode["post_red_blue_view"][deceptive_node.uuid]
            )
    else:
        assert episode["end_state"][deceptive_node.uuid] == 0
        assert not deceptive_node.isolated
    assert deceptive_node.node_position != 0


def check_blue_do_nothing_or_fail_action(episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Blue agent does nothing."""
    assert episode["post_red_state"] == episode["end_state"]
    assert episode["post_red_blue_view"] == episode["end_blue_view"]
    assert episode["post_red_vulnerabilities"] == episode["final_vulnerabilities"]
    assert episode["post_red_red_location"] == episode["final_red_location"]


# Red action checks


def check_red_basic_attack(
    env: GenericNetworkEnv,
    action: Dict[str, dict],
    episode: Dict[str, dict],
    counts: dict,
) -> int:
    """Check that the state of the environment is correct for an episode where the Red agent performs a basic attack."""
    red_success = action["Successes"]
    red_target_nodes: List[Node] = action["Target_Nodes"]
    red_attacking_node = action["Attacking_Nodes"]
    blue_action = episode["blue_action"]
    blue_node: Node = episode["blue_node"]
    post_red_state = episode["post_red_state"]
    post_red_blue_view = episode["post_red_blue_view"]

    for counter, current_success in enumerate(red_success):
        target_node = red_target_nodes[counter]
        attacking_node = red_attacking_node[counter]
        if (
            env.network_interface.game_mode.red.natural_spreading.chance.to_unconnected_node.value
            == 0
        ):
            assert not target_node.isolated
        if current_success:
            if blue_action != "isolate" or (
                blue_action == "isolate"
                and blue_node != attacking_node
                and blue_node != target_node
            ):
                if blue_action != "add_deceptive_node" or (
                    blue_action == "add_deceptive_node"
                    and target_node != blue_node[0]
                    and attacking_node != blue_node[0]
                    and not (
                        target_node in blue_node[1] and attacking_node in blue_node[1]
                    )
                ):
                    if (
                        target_node
                        not in env.network_interface.current_graph.entry_nodes
                    ):
                        assert red_target_nodes[
                            counter
                        ] in env.network_interface.get_current_connected_nodes(
                            attacking_node
                        )
            assert post_red_state[target_node.uuid] == 1
            if post_red_blue_view[target_node.uuid] == 1:
                counts["discovered_immediately_counter"] += 1
            if (
                target_node.deceptive_node
                and env.network_interface.game_mode.blue.intrusion_discovery_chance.immediate.deceptive_node.value
                == 1
            ):
                assert post_red_blue_view[target_node.uuid] == 1
            if (
                env.network_interface.game_mode.blue.intrusion_discovery_chance.immediate.standard_node.value
                == 0
                and not target_node.deceptive_node
            ):
                assert post_red_blue_view[target_node.uuid] == 0
            if (
                env.network_interface.game_mode.blue.intrusion_discovery_chance.immediate.standard_node.value
                == 1
                and not target_node.deceptive_node
            ):
                assert post_red_blue_view[target_node.uuid] == 1

    return counts


def check_red_zero_day_action(
    action: Dict[str, dict], episode: Dict[str, dict], counts: dict
) -> int:
    """Check that the state of the environment is correct for an episode where the Red agent performs a zero day attack."""
    for i in action["Successes"]:
        assert i
    target_nodes: List[Node] = action["Target_Nodes"]
    for n in target_nodes:
        assert episode["post_red_state"][n.uuid] == 1
        if episode["post_red_blue_view"][n.uuid] == 1:
            counts["discovered_immediately_counter"] += 1
    return counts


def check_red_spread_or_intrude_action(
    action: Dict[str, dict], episode: Dict[str, dict], counts: dict
) -> int:
    """Check that the state of the environment is correct for an episode where the Red agent spreads."""
    for counter, success in enumerate(action["Successes"]):
        target_node: Node = action["Target_Nodes"][counter]
        if success:
            assert episode["post_red_state"][target_node.uuid] == 1
            if episode["post_red_blue_view"][target_node.uuid] == 1:
                counts["discovered_immediately_counter"] += 1
    return counts


def check_red_random_move_action(
    env: GenericNetworkEnv, action: Dict[str, dict], episode: Dict[str, dict]
):
    """Check that the state of the environment is correct for an episode where the Red agent moves randomly."""
    for counter, current_success in enumerate(action["Successes"]):
        target_node: Node = action["Target_Nodes"][counter]
        if current_success:
            if episode["blue_action"] != "isolate" or (
                episode["blue_action"] == "isolate"
                and episode["blue_node"] != action["Attacking_Nodes"][counter]
                and episode["blue_node"] != target_node
            ):
                if episode["blue_action"] != "add_deceptive_node" or (
                    episode["blue_action"] == "add_deceptive_node"
                    and target_node != episode["blue_node"][0]
                    and action["Attacking_Nodes"][counter] != episode["blue_node"][0]
                    and not (
                        target_node in episode["blue_node"][1]
                        and action["Attacking_Nodes"][counter]
                        in episode["blue_node"][1]
                    )
                ):
                    if action["Attacking_Nodes"][counter] is None:
                        assert (
                            target_node
                            in env.network_interface.current_graph.entry_nodes
                        )
                    else:
                        assert action["Target_Nodes"][
                            counter
                        ] in env.network_interface.get_current_connected_nodes(
                            action["Attacking_Nodes"][counter]
                        )


def check_red_do_nothing_action(episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Red agent does nothing."""
    assert episode["initial_red_location"] == episode["post_red_red_location"]
    assert episode["initial_vulnerabilities"] == episode["post_red_vulnerabilities"]
    if len(episode["red_info"]) == 1:
        assert episode["initial_state"] == episode["post_red_state"]
        assert episode["initial_blue_view"] == episode["post_red_blue_view"]


def check_red_no_possible_targets(env: GenericNetworkEnv, episode: Dict[str, dict]):
    """Check that the state of the environment is correct for an episode where the Red agent has no possible targets."""
    if (
        env.network_interface.game_mode.red.agent_attack.attack_from.any_red_node.value
        and not env.network_interface.game_mode.blue.action_set.isolate_node.value
    ):
        assert (
            len(env.network_interface.current_graph.get_nodes(filter_true_safe=True))
            == 0
        )
    assert episode["initial_vulnerabilities"] == episode["post_red_vulnerabilities"]
