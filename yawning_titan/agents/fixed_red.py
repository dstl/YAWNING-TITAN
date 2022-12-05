import logging
import random

logger = logging.getLogger(__name__)


class FixedRedAgent:
    """
    The `FixedRegAgent` provides the red activity for the FourNodeEnv specific environment.

    This agent has two linked concepts to make it more dynamic. The first is the concept of
    zero days. These guarantee compromise and work 100% of the time regardless of the vulnerability score.
    In addition, the agent also has the ability to develop additional zero days.

    The behaviour of the agent is relatively fixed. The agent will prioritise the usage of zero days when
    available and otherwise randomly target nodes with a basic attack based on a configurable skill level.
    """

    red_previous_node = None
    red_current_node = None

    def __init__(
        self, skill=None, exploit_capability_dev=10, initial_no_of_zero_days=1
    ):
        self.skill = skill
        self.one_shot_exploits = initial_no_of_zero_days
        self.exploit_capability_dev = exploit_capability_dev
        self.exploit_dev_progress = 0

    def select_action(self, uncompromised_nodes, compromised_nodes):
        """
        Select the Red Teams action for a time step.

        Args:
            uncompromised_nodes: The list of uncompromised nodes linked to the Red team current position
            compromised_nodes: The list of compromised nodes linked to the Red team current position

        Returns:
            The action and target of the Red Team action
        """
        if len(uncompromised_nodes) > 0:
            machine = random.choice(uncompromised_nodes)
            if self.one_shot_exploits > 0:
                self.one_shot_exploits = 0
                return 0, machine

            else:
                self.exploit_dev_progress += 1

                if self.exploit_dev_progress >= self.exploit_capability_dev:
                    self.one_shot_exploits += 1
                    self.exploit_dev_progress = 0

                return 1, machine

        else:
            machine = random.choice(compromised_nodes)
            return 2, machine

    def update_location(self, target, red_current_node) -> None:
        """
        Update the current and previous location pointers.

        Args:
            target: the node within the environment being attacked
            red_current_node: the red agents current position
        """
        self.red_previous_node = red_current_node
        self.red_current_node = target

    def do_red_action(
        self,
        red_action,
        skill_level,
        attack_sucess_threshold,
        machine_states,
        target,
        able_to_move=False,
    ):
        """
        Execute a red action and changes the environment state.

        Args:
            red_action: The numeric value corresponding to the chosen action
            skill_level: The red team skill level
            attack_sucess_threshold: The attack power threshold for an attack to be succesful
            machine_states: The current machine states
            target: The machine being targetted by the attack

        Returns:
            None
        """
        if able_to_move and self.red_current_node is None:
            raise ValueError(
                "In order for the red agent to move, it needs its current position"
            )
        if red_action == 0:
            # Red Team Agent uses One-Shot
            machine_states[target][1] = 1
            logger.debug(f"Red Team: Zero Day Used on {target + 1}")
            if able_to_move:
                self.update_location(target, self.red_current_node)

        if red_action == 1:
            # Calculate Attack power based on skill level and target vulnerability score
            attack = (skill_level * machine_states[target][0]) / 100
            logger.debug(f"Red Attack Power: {attack}")
            # If Attack Power greater than ATTACK_SUCCESS_THRESHOLD, comrpomise machine
            if attack >= attack_sucess_threshold:
                machine_states[target][1] = 1  # Compromised
                logger.debug(f"Red Team: {attack} on target {target + 1} - SUCCESS")
                if able_to_move:
                    self.update_location(target, self.red_current_node)
            else:
                # If Attack Power below ATTACK_SUCCESS_THRESHOLD, attack failed
                logger.debug(f"Red Team: {attack} on target {target + 1} - FAILED")

        if able_to_move and red_action == 2:
            logger.debug(f"Red Team: Moved to target {target + 1}")
            self.update_location(target, self.red_current_node)
