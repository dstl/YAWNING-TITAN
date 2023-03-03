import pytest

from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.networks.network import Network
from yawning_titan.networks.node import Node
from yawning_titan.yawning_titan_run import YawningTitanRun

N_TIME_STEPS = 1000


@pytest.fixture()
def corporate_network() -> Network:
    router_1 = Node(high_value_node=False, entry_node=True)
    switch_1 = Node(high_value_node=False, entry_node=False)
    switch_2 = Node(high_value_node=True, entry_node=False)

    pc_1 = Node(high_value_node=False, entry_node=False)
    pc_2 = Node(high_value_node=True, entry_node=False)
    pc_3 = Node(high_value_node=True, entry_node=True)
    pc_4 = Node(high_value_node=True, entry_node=False)
    pc_5 = Node(high_value_node=True, entry_node=False)
    pc_6 = Node(high_value_node=True, entry_node=False)

    server_1 = Node(high_value_node=False, entry_node=False)
    server_2 = Node(high_value_node=True, entry_node=False)

    network = Network(set_random_vulnerabilities=True)

    network.add_node(router_1)
    network.add_node(switch_1)
    network.add_node(server_1)
    network.add_node(pc_1)
    network.add_node(pc_2)
    network.add_node(pc_3)
    network.add_node(switch_2)
    network.add_node(server_2)
    network.add_node(pc_4)
    network.add_node(pc_5)
    network.add_node(pc_6)

    network.add_edge(router_1, switch_1)
    network.add_edge(switch_1, server_1)
    network.add_edge(switch_1, pc_1)
    network.add_edge(switch_1, pc_2)
    network.add_edge(switch_1, pc_3)
    network.add_edge(router_1, switch_2)
    network.add_edge(switch_2, server_2)
    network.add_edge(switch_2, pc_4)
    network.add_edge(switch_2, pc_5)
    network.add_edge(switch_2, pc_6)

    network.reset_random_vulnerabilities()

    return network


def test_yawning_titan_run_with_corporate_network(
        corporate_network: Network
):
    yt_run = YawningTitanRun(
        network=corporate_network,
        total_timesteps=N_TIME_STEPS,
        eval_freq=N_TIME_STEPS,
        collect_additional_per_ts_data=True,
        auto=False
    )

    yt_run.setup()
    yt_run.train()
    yt_run.evaluate()
    loop = ActionLoop(yt_run.env, yt_run.agent, episode_count=1)
    loop.gif_action_loop(save_gif=False, render_network=True)
    assert True