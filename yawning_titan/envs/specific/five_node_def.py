"""
NOTE: This environment is deprecated but has been included as an example of how to create a specific environment.

Five Node Environment AKA Cyber Whack A Mole
---------------------------------------------

This environment is made up of five nodes in the following topology:

+------------+  +------------+  +------------+  +------------+  +------------+
|            |  |            |  |            |  |            |  |            |
|  Node 1    |  |   Node 2   |  |    Node 3  |  |   Node 4   |  |   Node 5   |
|            |  |            |  |            |  |            |  |            |
+------------+  +------------+  +------------+  +------------+  +------------+

Configurable Parameters:

    Number of Machines - This value determines the number of machines within the environment and defaults to 5.
    Number of Compromised Machines for Loss - This value determines how many compromised machines equal a loss.
    Attack Success Threshold - This value determines what the red agents attack value must be to be successful.
"""

import logging
from typing import Tuple

import gym
import numpy as np

from yawning_titan.agents.nsa_red import NSARed
from yawning_titan.agents.simple_blue import SimpleBlue
from yawning_titan.envs.specific.core import node_states as nodes
from yawning_titan.envs.specific.core.machines import Machines

logger = logging.getLogger(__name__)


class FiveNodeDef(gym.Env):
    """OpenAI Gym Environment for Cyber Whack-a-Mole."""

    def __init__(
        self,
        attacker_skill: float = 50,
        n_machines: int = 5,
        attack_success_threshold: float = 0.3,
        no_compromised_machine_loss: int = 4,
    ):
        # Setting number of machines
        self.n_machines = n_machines

        # Setting up environment spaces
        # Each machine has two values, vulnerability score and compromised status
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(self.n_machines, 2)
        )
        # Set Discrete Action Space Based on the number of machines in environment
        # Actions 0 to n_machines - 1 = Patch
        # Actions n_machines to (n_machines * 2) - 1 = Recover
        # Action n_machines * 2 = Do Nothing
        self.action_space = gym.spaces.Discrete(self.n_machines * 2)

        # Setting up Episode Settings
        self.reward_range = [-50, 50]
        self.total_rewards = 0
        self.total_no_of_steps = 0
        if no_compromised_machine_loss >= self.n_machines:
            raise ValueError(
                "The number of compromised machines for loss must be less than the total number of machines"
            )
        else:
            self.no_compromised_machine_loss = no_compromised_machine_loss
        self.done = False

        # Setting up Machine States
        machines = Machines(n_machines=self.n_machines)
        self.machine_states = machines.machine_states
        self.initial_states = machines.initial_states
        self.no_compromised_machines = 0

        # Setting up blue agents actions
        self.blue = SimpleBlue(n_machines=self.n_machines)

        # Setting up the red agent settings
        self.attacker_skill = attacker_skill
        self.attack_success_threshold = attack_success_threshold
        self.red = NSARed(
            self.attacker_skill, [0, 1], [0, 0], [], zd_gain=1, zd_start_amount=1
        )
        self.uncompromised_nodes = self.n_machines
        self.compromised_nodes = None

        logger.debug("Experiment Started")
        logger.debug(f"Starting State: {self.initial_states}")

    def reset(self) -> np.array:
        """
        Reset the environment to the default state.

        Returns:
            A new starting observation (numpy array)
        """
        # Reset Machines
        machines = Machines(n_machines=self.n_machines)
        self.machine_states = machines.machine_states
        self.initial_states = machines.initial_states

        # Reset Episode Values
        self.total_rewards = 0
        self.total_no_of_steps = 0
        self.done = False

        # Reset Red Team
        self.no_compromised_machines = 0
        self.red = NSARed(
            self.attacker_skill, [0, 1], [0, 0], [], zd_gain=1, zd_start_amount=1
        )

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
        """
        logger.debug(f"Timestep - {self.total_no_of_steps}")
        self.uncompromised_nodes = nodes.get_uncompromised_nodes(self.machine_states)
        self.compromised_machines = nodes.get_compromised_nodes(self.machine_states)

        # RED TEAM AGENT
        node_set = self.uncompromised_nodes
        self.red.update_node_set(node_set)
        if len(node_set) == 0:
            red_action = "02"
        else:
            zd = self.red.check_zd_available()
            if zd:
                red_action = "00"
            else:
                self.red.increment_day()
                red_action = "01"

        target = self.red.choose_node()

        self.red.do_action(
            target,
            red_action,
            [self.machine_states, None, self.attack_success_threshold, False],
        )

        # BLUE TEAM AGENT

        self.blue.do_blue_action(action, self.machine_states, self.initial_states)

        # Calculate Timestep Reward
        reward = self._get_reward()
        self.total_rewards += reward

        # Add to timestep counter
        self.total_no_of_steps += 1

        # Check if Episode is complete
        self._is_done()
        # Get next observation
        observation = self._observe()

        logger.debug(
            f"Total Reward: {self.total_rewards} Total No. of Steps : {self.total_no_of_steps} No. of Compromised Machines: {self.no_compromised_machines} "
        )
        return observation, reward, self.done, {}

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
        Calculate the Reward for agent.

        The reward policy is set to incentivise having no compromised machines.
        The only state where the agent recieves a reward is when there are
        no compromised machines.

        Returns:
            A reward value for a timestep
        """
        self.compromised_machines = nodes.get_compromised_nodes(self.machine_states)
        reward = 0
        if self.no_compromised_machines == 0:
            reward += 1
        else:
            reward = 0

        return reward

    def _is_done(self):
        """
        Determine if an epsiode is completed.

        There are two terminal states.

        1) Is the number of compromised machines above the number of
        compromised machines for loss parameter?
        2) Has the blue team surviced more than 1500 timesteps

        Sets self.done to True if the game ends
        """
        self.no_compromised_machines = len(self.compromised_machines)

        if self.no_compromised_machines == self.no_compromised_machine_loss:
            logger.debug(
                f"Red Team Wins - Game Over Blue Team Survived - {self.total_no_of_steps}"
            )
            self.done = True
        elif self.total_no_of_steps == 1500:
            logger.debug("Blue Team Wins - Game Over")
            self.done = True
