"""
A new node network that can be configured for multiple different configurations.

Paper:
https://www.nsa.gov.Portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf

Currently suppports:
    - 18 node network from the research paper.
    - a network creator that allows you to use multiple topologies and change the connectivity of the network.

Red agent actions:
    Spread:
        Tries to spread to each node connected to a compromised node.
    Randomly infect:
        Tries to randomly infect every currently un-compromised node.

Configurable parameters:
    chance_to_spread
        This is the chance for the red agent to spread between nodes
    chance_to_spread_during_patch
        There is a chance that when a compromised node is patched the red agent "escapes" to neaby nodes and compromises
        them.
    chance_to_randomly_compromise
        This is the chance that the red agent randomly infects a un-compromised node.
    cost_of_isolate
        The cost (negative reward) associated with performing the isolate action (initially set to 10 based on data
        from the paper).
    cost_of_patch
        The cost (negative reward) associated with performing the patch action (initially set to 5 based on data from
        the paper).
    cost_of_nothing
        The cost (negative reward) associated with performing the do nothing action (initially set to 0
        based on data from the paper).
    end
        The number of steps that the blue agent must survive for to win.
    spread_vs_random_intrusio
        The chance that the red agent will choose the spread action on its turn as apposed to the random intrusion
        action.
    punish_for_isolate
        Either True or False. If True then each step the agent is punished based on the number of isolated nodes there
        are.
    reward_method
        Either 0, 1 or 2. Each constitutes a different method of rewarding the agent:
            - 0 is the papers reward system.
            - 1 is my reward system rewarding based on number of un-compromised nodes.
            - 2 is the minimal reward system. The agent gets 1 for a win or -1 for a loss.

"""

import logging
from typing import Tuple

import gym
import numpy as np
from gym import spaces

from yawning_titan.agents.nsa_red import NSARed
from yawning_titan.envs.generic.helpers.graph2plot import CustomEnvGraph
from yawning_titan.envs.generic.helpers.network_creator import create_18_node_network
from yawning_titan.envs.specific.core.nsa_node_collection import NodeCollection

logger = logging.getLogger(__name__)


class NodeEnv(gym.Env):
    """Class that creates a similar environments to that presented in Ridley 17 (Ref above)."""

    def __init__(
        self,
        chance_to_spread: float = 0.01,
        chance_to_spread_during_patch: float = 0.01,
        chance_to_randomly_compromise: float = 0.15,
        cost_of_isolate: float = 10,
        cost_of_patch: float = 5,
        cost_of_nothing: float = 0,
        end: int = 1000,
        spread_vs_random_intrusion: float = 0.5,
        punish_for_isolate: bool = False,
        reward_method: int = 1,
        network: Tuple[np.array, dict] = create_18_node_network(),
    ):
        super(NodeEnv, self).__init__()

        # sets up the configuration for the env
        self.chance_to_spread = chance_to_spread
        self.chance_to_spread_during_patch = chance_to_spread_during_patch
        self.chance_to_randomly_compromise = chance_to_randomly_compromise
        self.cost_of_isolate = cost_of_isolate
        self.cost_of_patch = cost_of_patch
        self.cost_of_nothing = cost_of_nothing
        self.end = end
        self.spread_vs_random_intrusion = spread_vs_random_intrusion
        self.punish_for_isolate = punish_for_isolate
        self.reward_method = reward_method
        self.network = network
        self.duration = 0

        self.graph_plotter = None

        self.state = NodeCollection(self.network, self.chance_to_spread_during_patch)
        # skill, action_set, action_probabilities, node_set
        self.RED = NSARed(
            1,
            [3, 4],
            [self.spread_vs_random_intrusion, 1 - self.spread_vs_random_intrusion],
            [str(i) for i in range(self.state.get_number_of_nodes())],
        )

        self.action_space = spaces.Discrete(self.state.get_number_of_nodes() * 2 + 1)
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(
                self.state.get_number_of_nodes()
                * (self.state.get_number_of_nodes() + 2),
            ),
        )

        self.env_observation = self.state.get_observation().flatten()

        logger.debug("Experiment Started")
        logger.debug(f"Starting State: {self.state.get_observation()}")

    def reset(self) -> np.array:
        """
        Reset the environment to the default state.

        Returns:
            A new starting observation (numpy array)
        """
        self.state = NodeCollection(self.network, self.chance_to_spread_during_patch)
        self.duration = 0
        self.env_observation = self.state.get_observation().flatten()
        self.RED = NSARed(
            1,
            ["10", "11"],
            [self.spread_vs_random_intrusion, 1 - self.spread_vs_random_intrusion],
            [str(i) for i in range(self.state.get_number_of_nodes())],
        )

        logger.debug("Environment Reset")
        logger.debug(f"Starting State: {self.state.get_observation()}")

        return self.env_observation

    def step(self, action: int) -> Tuple[np.array, float, bool, dict]:
        """
        Take one timestep within the environment.

        Execute the actions for both Blue RL agent and
        hard-hard coded Red agent.

        Args:
            action: The action value generated from the Blue RL agent (int)

        Returns:
            observation: The next environment observation (numpy array)
            reward: The reward value for that timestep (int)
            done: Whether the epsiode is done (bool)
            info: a dictionary containing info about the current state
        """
        logger.debug(f"Timestep: {self.duration}")

        """RED AGENTS TURN"""
        red_action = self.RED.choose_action()
        self.RED.do_action(
            self.state,
            red_action,
            [self.chance_to_spread, self.chance_to_randomly_compromise],
        )

        number_uncompromised = self.state.get_number_of_un_compromised()
        reward = 0

        """BLUE AGENTS TURN"""
        # checks if there are no safe nodes left --> blue agent loss
        if number_uncompromised == 0:
            logger.debug("All states taken - Game Over")
            done = True
            if self.reward_method == 0 or self.reward_method == 1:
                reward = -500
            else:
                reward = -1
        else:
            done = False
            # if there are still some safe nodes then the blue agent takes their go
            if action == 0:
                # blue agent does nothing
                logger.debug("Blue Action: DO NOTHING")
                if self.reward_method == 0:
                    reward = -self.cost_of_nothing
                else:
                    reward = 0
            else:
                # converts the single number for the action into a node and action value
                action = action - 1
                action_node = int(action / 2)
                action_taken = int(action % 2)

                if action_taken == 0:
                    # blue agent changes the isolation status on a node (if true then makes it false ect)
                    logger.debug(f"Blue Action: ISOLATE NODE {action_node}")
                    self.state.modify_node(action_node, (True, 0))

                    # rewards for the action
                    if self.reward_method == 0:
                        reward = -self.cost_of_isolate
                    else:
                        reward = 0

                elif action_taken == 1:
                    # blue patches a node
                    logger.debug(f"Blue Action: PATCH NODE {action_node}")
                    self.state.modify_node(action_node, (False, 1))
                    # if a node is infected and patched then the red agent can spread to connected nodes
                    self.state.spread(action_node)

                    # rewards for the action
                    if self.reward_method == 0:
                        reward = -self.cost_of_patch
                    else:
                        reward = 0
            # rewards for the current step
            if self.reward_method == 0:
                reward = reward + 3 * self.state.calculate_reward()
            elif self.reward_method == 1:
                reward = reward + self.state.calculate_reward()

        # gets the current observation from the environment
        self.env_observation = self.state.get_observation().flatten()
        self.duration += 1

        # if the total number of steps reaches the set end then the blue agent wins and is rewarded accordingly
        if self.duration == self.end:
            done = True
            if self.reward_method == 0 or self.reward_method == 1:
                reward = 500
            else:
                reward = 1

        # If turned on then the agent is punished for keeping nodes isolated
        if self.punish_for_isolate:
            reward = reward - 0.5 * self.state.get_number_of_isolated()

        logger.debug(
            f"Total Reward: {reward} Total No. of Steps : {reward} "
            f"No. of Compromised Machines: {len(self.state.get_compromised_nodes())} "
        )

        return (
            self.env_observation,
            reward,
            done,
            {"nodes": self.state.get_number_of_un_compromised()},
        )

    def render(self, mode: str = "human"):
        """
        Render the network using the graph2plot class.

        This uses a networkx representation of the network.

        Args:
            mode: the mode of the rendering
        """
        if self.graph_plotter is None:
            self.graph_plotter = CustomEnvGraph()
        comp = list(map(str, self.state.get_compromised_nodes()))
        safe = list(map(str, self.state.get_un_compromised_nodes()))
        main_graph = self.state.get_netx_graph()
        main_graph_pos = self.state.get_netx_pos()
        reward = round(self.state.calculate_reward(), 2)

        self.graph_plotter.render(
            self.duration,
            main_graph,
            main_graph_pos,
            {i: 1 for i in comp},
            safe,
            [],
            reward,
            None,
            {i: 0.5 for i in main_graph.nodes},
            [],
            "",
        )
