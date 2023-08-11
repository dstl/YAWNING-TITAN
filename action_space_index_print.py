import time
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.networks.network_db import default_18_node_network
from yawning_titan.game_modes.game_mode_db import default_game_mode
from yawning_titan.envs.generic.core.action_loops import ActionLoop

game_mode = default_game_mode()
network = default_18_node_network()
network_interface = NetworkInterface(game_mode=game_mode, network=network)
red = RedInterface(network_interface)
blue = BlueInterface(network_interface)

print("Create new GenericNetworkEnv as env")
env = GenericNetworkEnv(red, blue, network_interface)

print()
print("Performing the check env")
check_env(env, warn=True)

print()
print("Performing the post check env reset")
# reset anything changed during the check
_ = env.reset()

print()
print("Creating a new PPO agent")
agent = PPO(PPOMlp, env, verbose=1)
print(env.action_space.n)

print()
print("Loop over the action space range and call step on each action")
for action in range(env.action_space.n):
  env.step(action)

print()
print("Save the agent to ./agent.zip")
# save agent
agent.save("./agent.zip")

print()
print("Create new GenericNetworkEnv as env2")
env2 = GenericNetworkEnv(red, blue, network_interface)

print()
print("Performing the check env")
check_env(env2, warn=True)

print()
print("Performing the post check env reset")
# reset anything changed during the check
_ = env2.reset()

print()
print("Creating load the Saved PPO agent from ./agent.zip")
# loading the agent again
agent = PPO.load("./agent.zip", env=env2)
print(env2.action_space.n)

print()
print("Loop over the action space range and call step on each action")
for action in range(env2.action_space.n):
  env2.step(action)