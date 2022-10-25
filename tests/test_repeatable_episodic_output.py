from typing import List

from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from stable_baselines3.common.env_checker import check_env

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.helpers import network_creator
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from pandas import DataFrame
from pandas.testing import assert_frame_equal


def test_repeatable_episodic_output():
    """
    Test to check that actions undertaken by the red attacking agent
    are repeatable across all episodes
    """
    matrix, node_positions = network_creator.create_18_node_network()

    settings_path = "D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\game_modes\default_game_mode.yaml" # remove absolute path and utilise pathlib relative paths

    entry_nodes = ["0"]


    network_interface = NetworkInterface(matrix, node_positions, entry_nodes=entry_nodes, settings_path=settings_path, high_value_target='12')

    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(red, blue, network_interface, seed=666)

    check_env(env, warn=True)

    _ = env.reset()

    agent = PPO(PPOMlp, env, verbose=1, seed=666) #TODO: allow PPO to inherit environment seed. Monkey patch additional feature?

    agent = agent.learn(total_timesteps=1000)


    loop = ActionLoop(env,agent,episode_count=2)

    results: List[DataFrame] = loop.standard_action_loop() 

    print(results[0].compare(results[1]))
    
    assert_frame_equal(results[0],results[1])