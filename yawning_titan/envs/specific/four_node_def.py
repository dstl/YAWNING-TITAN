"""
NOTE: This environment is deprecated but has been included as an example of how to create a specific environment.

Four Node Connected Environment
------------------------------------

This environment is made up of four nodes in the following topology:
                        +-------------------+
                        |                   |
                        |                   |
         +--------------+   Node 1 - UAD    +---------------+
         |              |     Red Start     |               |
         |              |                   |     +---------+---------+
+--------+----------+   |                   |     |                   |
|                   |   +-------------------+     |                   |
|                   |                             |    Node 3 - UAD   |
|  Node 2 - UAD     |                             |                   |
|                   |   +-------------------+     |                   |
|                   |   |                   |     +---------+---------+
+-------+-----------+   |   Node 4 - UAD    |               |
        |               |    Objective      |               |
        +---------------+                   +---------------+
                        |                   |
                        |                   |
                        +-------------------+

The aim of this environment is for a blue team agent, which has full observability of the
environment, to successfully stop the hard code red agent from getting to the objective.

Inspired by:
- https://github.com/panlybero/MARL-POMDP-CYBERSECURITY
- https://www.scitepress.org/Link.aspx?doi=10.5220%2f0006197105590566
"""
import logging
from typing import Tuple

import gym
import networkx as nx
import numpy as np

from yawning_titan.agents.fixed_red import FixedRedAgent
from yawning_titan.agents.simple_blue import SimpleBlue
from yawning_titan.envs.generic.helpers.graph2plot import CustomEnvGraph
from yawning_titan.envs.specific.core import node_states as nodes
from yawning_titan.envs.specific.core.machines import Machines

logger = logging.getLogger(__name__)


class FourNodeDef(gym.Env):
    """Class that represents a simple four node connected network."""

    def __init__(
        self,
        attacker_skill: float = 90,
        red_start_node: int = 0,
        objective_node: int = 3,
        n_machines: int = 4,
        attack_success_threshold: float = 0.6,
    ):
        # Setting up the network
        self.n_machines = n_machines
        self.graph_adj_matrix = np.array(
            [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        ).reshape(4, 4)
        self.network = nx.from_numpy_array(self.graph_adj_matrix)
        assert len(self.network) == self.n_machines
        logger.debug("Assert Pass: Length of network is equal to number of machines")
        self.pos = nx.spring_layout(self.network)

        # Setting up the environment spaces
        self.action_space = gym.spaces.Discrete(self.n_machines * 2)
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(self.n_machines, 2)
        )

        # Setting up Episode Settings
        self.reward_range = [-50, 50]
        self.total_rewards = 0
        self.total_no_of_steps = 0
        self.done = False

        # Setting up Machine States
        machines = Machines(n_machines=self.n_machines)
        self.machine_states = machines.machine_states
        self.initial_states = machines.initial_states
        self.uncompromised_nodes = None
        self.compromised_nodes = None

        # Setting up blue agents actions
        self.blue = SimpleBlue(n_machines=self.n_machines)

        # Setting up the objective for Red
        self.objective_node = objective_node

        # Setting up the red agent settings
        self.red_start_node = red_start_node
        self.red_previous_node = None
        self.red_current_node = self.red_start_node
        self.attacker_skill = attacker_skill
        self.attack_success_threshold = attack_success_threshold
        self.red_objective_accomplished = False
        self.RED = FixedRedAgent(skill=self.attacker_skill)
        self.target = None

        self.graph_plotter = None

        logger.debug("Experiment Started")
        logger.debug(f"Starting State: {self.initial_states}")

    def reset(self) -> np.array:
        """
        Reset the environment to the default state.

        Returns:
            A new starting observation (numpy array)
        """
        # Reset Machine States
        machines = Machines(n_machines=self.n_machines)
        self.machine_states = machines.machine_states
        self.initial_states = machines.get_initial_state()

        # Reset Episode Settings
        self.total_rewards = 0
        self.total_no_of_steps = 0
        self.done = False

        # Reset Red Agent
        self.red_objective_accomplished = False
        self.red_current_node = self.red_start_node
        self.RED = FixedRedAgent(skill=self.attacker_skill)

        logger.debug("Environment Reset")
        logger.debug(f"Starting State: {self.initial_states}")

        return self._observe()

    def step(self, action: int) -> Tuple[np.array, float, bool, dict]:
        """
        Take a time step and execute the actions for both Blue RL agent and hard-hard coded Red agent.

        Args:
            action: The action value generated from the Blue RL agent (int)

        Returns:
            observation: The next environment observation (numpy array)
            reward: The reward value for that timestep (int)
            done: Whether the epsiode is done (bool)
            notes: An empty notes dictionary
        """
        logger.debug(f"Timestep - {self.total_no_of_steps}")
        logger.debug(
            f"Red Current: {self.red_current_node} Uncomp Node: {self.uncompromised_nodes} Comp Nodes: {self.compromised_nodes}"
        )

        self.uncompromised_nodes = nodes.get_linked_uncompromised_nodes(
            self.red_current_node, self.network, self.machine_states
        )
        self.compromised_nodes = nodes.get_linked_compromised_nodes(
            self.red_current_node, self.network, self.machine_states
        )

        red_action, self.target = self.RED.select_action(
            self.uncompromised_nodes, self.compromised_nodes
        )
        skill_level = self.RED.skill

        assert (self.red_current_node == 0 and self.target == 3) is False

        if red_action == 0:
            self.machine_states[self.target][1] = 1
            logger.debug(f"Red Team: Zero Day Used on {self.target + 1}")
            self.red_previous_node = self.red_current_node
            self.red_current_node = self.target

        elif red_action == 1:
            # Calculate Attack power based on skill level and target vulnerability score
            attack = (skill_level * self.machine_states[self.target][0]) / 100
            logger.debug(f"Red Attack Power: {attack}")
            # If Attack Power greater than ATTACK_SUCCESS_THRESHOLD, compromise machine
            if attack >= self.attack_success_threshold:
                # Compromised
                self.machine_states[self.target][1] = 1
                self.red_previous_node = self.red_current_node
                self.red_current_node = self.target
                logger.debug(f"Red Team: {attack} on target {self.target} - SUCCESS")
            else:
                logger.debug(f"Red Team: {attack} on target {self.target} - FAILED")

        elif red_action == 2:
            self.red_previous_node = self.red_current_node
            self.red_current_node = self.target
            logger.debug(f"Red Team: Moved to {self.target}")

        # BLUE TEAM AGENT
        self.blue.do_blue_action(action, self.machine_states, self.initial_states)

        if self.machine_states[3][1] == 1:
            self.red_objective_accomplished = True

        if self.machine_states[self.red_current_node][1] == 0:
            self.red_current_node = self.red_previous_node
            logger.debug("Blue Team pushed Red Team back")

        # Calculate Timestep Reward
        reward = self._get_reward()
        self.total_rewards += reward

        # Add to timestep counter
        self.total_no_of_steps += 1

        # Check if Episode is complete
        # is_done check before reward
        self._is_done()

        # Get next observation
        observation = self._observe()

        logger.debug(
            f"Total Reward: {self.total_rewards} Total No. of Steps : {self.total_no_of_steps}"
        )

        return observation, reward, self.done, {"action": action}

    def render(self, mode: str = "human"):
        """Render the environment to the screen so that it can be played in realtime."""
        if self.graph_plotter is None:
            self.graph_plotter = CustomEnvGraph()

        comp = {i: True for i in self.compromised_nodes}
        safe = self.uncompromised_nodes
        main_graph = self.network
        main_graph_pos = self.pos
        states = self.machine_states
        vulnerabilities = {}
        for counter, i in enumerate(states):
            vulnerabilities[counter] = i[0]

        self.graph_plotter.render(
            self.total_no_of_steps,
            main_graph,
            main_graph_pos,
            comp,
            safe,
            [],
            self.total_rewards,
            self.red_previous_node,
            vulnerabilities,
            [],
            "Four node network with an RL blue vs probabilistic red",
        )

    def _observe(self) -> np.array:
        """
        Create the next observation.

        Returns:
            A formatted observation array
        """
        observation = np.array(self.machine_states, dtype=np.float32)
        return observation

    def _get_reward(self) -> float:
        """
        Calculate the reward for the agent.

        The reward policy is set to incentivize survival and punish
        when red wins.

        Returns:
            A reward value for a time step
        """
        reward = 0

        if self.red_objective_accomplished is True:
            reward -= 1

        if self.total_no_of_steps == 499:
            reward += 1

        return reward

    def _is_done(self):
        """
        Determine if an epsiode has been completed.

        There are two terminal states.

        1) If the red agent successfully compromises the objective
        2) If the blue agent successfully survives 500 time steps.

        Sets self.done to True if either are fulfilled.
        """
        if self.red_objective_accomplished is True:
            logger.debug(
                f"Red Team Wins - Game Over Blue Team Survived - {self.total_no_of_steps}"
            )
            self.done = True

        if self.total_no_of_steps == 500:
            logger.debug("Blue Team Wins - Game Over")
            self.done = True
