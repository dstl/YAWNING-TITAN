import os

from tests import TEST_CONFIG_PATH_OLD
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_network_interface(generate_generic_env_test_reqs):
    """Test the network interface class and associated methods work as intended."""
    env: GenericNetworkEnv = generate_generic_env_test_reqs(
        os.path.join(TEST_CONFIG_PATH_OLD, "everything_guaranteed.yaml"),
        net_creator_type="mesh",
        n_nodes=15,
        entry_nodes=["0", "1", "2"],
    )
    for node in env.network_interface.current_graph.nodes:
        node = env.network_interface.current_graph.get_node_from_uuid(
            node.uuid
        )  # reset node reference as network graph has been reset
        node_name_lookup = env.network_interface.current_graph.get_nodes_by_name()
        assert env.network_interface.adj_matrix.all() == 0
        assert (
            env.network_interface.current_graph.get_nodes(filter_true_compromised=True)
            == []
        )
        assert set(
            env.network_interface.current_graph.get_nodes(filter_true_safe=True)
        ) == set(env.network_interface.current_graph.get_nodes())
        env.network_interface.attack_node(node=node, skill=0.5, guarantee=True)
        assert node.true_compromised_status == 1
        assert (
            sum(env.network_interface.get_all_node_compromised_states().values()) == 1
        )
        assert (
            sum(
                env.network_interface.get_all_node_blue_view_compromised_states().values()
            )
            == 1
        )
        assert env.network_interface.current_graph.get_nodes(
            filter_true_compromised=True
        ) == [node]
        assert env.network_interface.current_graph.get_nodes(
            filter_blue_view_compromised=True
        ) == [node]
        node.vulnerability_score = 2
        assert node.vulnerability_score == 2
        node.reset_vulnerability()
        target_nodes = [node_name_lookup[name] for name in ["2", "3", "9"]]
        env.network_interface.update_stored_attacks(
            [node, node, node_name_lookup["5"]], target_nodes, [True, False, True]
        )
        assert env.network_interface.true_attacks == [
            [node, node_name_lookup["2"]],
            [node, node_name_lookup["3"]],
            [node_name_lookup["5"], node_name_lookup["9"]],
        ]

        observation_size = env.calculate_observation_space_size(with_feather=False)
        # assert the observation space is the correct size
        assert env.network_interface.get_observation_size() == observation_size

        env.network_interface.reset_stored_attacks()
        assert env.network_interface.true_attacks == []
        assert env.network_interface.detected_attacks == []
        env.network_interface.isolate_node(node)
        assert env.network_interface.current_graph.get_nodes(filter_isolated=True) == [
            node
        ]
        assert env.network_interface.current_graph.get_nodes(
            filter_isolated=True, filter_true_compromised=True
        ) == [node]
        env.network_interface.reconnect_node(node)
        assert env.network_interface.current_graph.get_nodes(filter_isolated=True) == []
        env.network_interface.make_node_safe(node)
        assert (
            env.network_interface.current_graph.get_nodes(filter_true_compromised=True)
            == []
        )
        assert (
            env.network_interface.current_graph.get_nodes(
                filter_blue_view_compromised=True
            )
            == []
        )
        env.reset()
