import logging
from typing import List

logger = logging.getLogger(__name__)


class SimpleBlue:
    """An interface capable of training a reinforcement learning agent in the `specific` environments."""

    def __init__(self, n_machines=None):
        self.n_machines = n_machines

    def patch_machines(self, action: int, machine_states: List[List[float]]):
        """
        Patch a target machine and reduce its vulnerability score.

        This action reduces a target machines vulerability score by 0.2
        per use to a lower threshold of 0.2.

        Args:
            action: The chosen action
            machine_states: The current state of the env
        """
        if machine_states[action][1] == 1:
            pass
        elif machine_states[action][0] < 0.39:
            machine_states[action][0] = 0.2
        else:
            machine_states[action][0] -= 0.2

    def recover_machines(
        self,
        action: int,
        machine_states: List[List[float]],
        initial_states: List[List[float]],
    ):
        """
        Recover a compromised machine and resets its state to the initial state during environment creation.

        Args:
            action: The chosen action
            machine_states: The current state of the env
            initial_states: The first state of the environment when initialised/reset
        """
        machine_states[action][0] = initial_states[action][0]
        machine_states[action][1] = initial_states[action][1]

    def nothing(self, action: int):
        """Do nothing - a noop in other reinforcement learning papers."""
        pass

    def do_blue_action(
        self,
        action: int,
        machine_states: List[List[float]],
        initial_states: List[List[float]],
    ):
        """
        Perform the chosen action.

        Args:
            action: The chosen action to perform
            machine_states: The state of the current env
            initial_states: The state of the env initially
        """
        if 0 <= action <= self.n_machines - 1:
            # Blue Agent takes Patch Action
            self.patch_machines(action, machine_states)
            logger.debug(f"Blue Team: Patched - Used {action}")
        elif self.n_machines <= action <= (self.n_machines * 2) - 1:
            # Blue Agent takes Recover Action
            self.recover_machines(
                action - self.n_machines, machine_states, initial_states
            )
            logger.debug(f"Blue Team: Recovered - Used {action}")
        elif action == self.n_machines * 2:
            # Blue Agent takes Nothing Action
            self.nothing(action)
            logger.debug(f"Blue Team: Did Nothing - Used {action}")
