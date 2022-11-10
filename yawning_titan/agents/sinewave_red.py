import math
import random
from typing import Dict, List, Union

from yawning_titan.envs.generic.core.red_interface import RedInterface


def calculate_number_moves(attack_strength):
    """
    Calculate the number of moves for the red agent to take.

    Args:
        attack_strength: Current red agent attack strength

    Returns:
        An int representing the number of moves the red agent can take that turn
    """
    amount = math.floor(attack_strength)
    random_value = random.randint(0, 10)
    diff = attack_strength - amount
    if diff * 10 > random_value:
        amount += 1

    return int(amount)


class SineWaveRedAgent(RedInterface):
    """
    An agent which is based on the RedInterface provided by the YAWNING TITAN generic environment.

    This agent is an example of how the generic RedInterface can be extended to include custom red
    team behaviour - in this case, action selection.

    The agent uses a sine wave to allow the red agent to attack more randomly and in waves rather than constantly.
    """

    def __init__(self, network_interface):
        self.time = 0
        self.sine_offset = random.randint(0, 10)
        self.cosine_offset = random.randint(0, 10)
        self.sine_multiplier = round(random.uniform(1.5, 2.25), 4)
        self.cosine_multiplier = round(random.uniform(2.75, 3.5), 4)
        super().__init__(network_interface)

    def perform_action(self) -> Dict[int, Dict[str, List[Union[bool, str, None]]]]:
        """
        Chooses and then performs an action. This is called for every one of the red agents turns.

        Returns:
            A tuple containing the name of the action, the success status, the target, the attacking node and any natural spreading attacks
        """
        current_turn_attack_info = {}
        action_counter = 0

        # advances the agents power time
        self.time += round(random.uniform(0.2, 0.8), 2)
        if self.time >= 50:
            self.time = 0
            self.sine_offset = random.randint(0, 10)
            self.cosine_offset = random.randint(0, 10)

        red_skill = self.network_interface.game_mode.red.red_skill

        # works out the current strength of the red agent
        current_strength = (
            (
                math.sin(self.sine_multiplier * self.time + self.sine_offset)
                + math.cos(self.cosine_multiplier * self.time + self.cosine_offset)
            )
            + red_skill
            - 0.5
        )
        # uses the red agents skill as a baseline
        if current_strength < red_skill:
            current_strength = red_skill

        # calculate the number of attacks that the red agent will get this go
        number_runs = calculate_number_moves(current_strength)

        if self.network_interface.game_mode.red.red_uses_spread_action:
            current_turn_attack_info[action_counter] = self.natural_spread()

        zd = False
        # tries to use a zero day attack if it is enabled (not in the main dictionary as it tries it every turn)
        if self.network_interface.game_mode.red.red_uses_zero_day_action:
            inter = self.zero_day_attack()
            if True in inter["Successes"]:
                current_turn_attack_info[action_counter] = inter
                zd = True
                action_counter += 1
        if zd is False:
            counter = 0
            name = ""
            while counter < number_runs and name != "no_possible_targets":
                # chooses an action
                action = self.choose_action()

                current_turn_attack_info[action_counter] = self.action_dict[action]()
                action_counter += 1

                counter += 1
                name = current_turn_attack_info[action_counter - 1]["Action"]

            # If there are no possible targets for an attack then red will attempt to move to a new node
            if name == "no_possible_targets" and number_runs >= counter:
                current_turn_attack_info[action_counter] = self.random_move()
                action_counter += 1

        # increments the day for the zero day
        if self.network_interface.game_mode.red.red_uses_zero_day_action:
            self.increment_day()

        all_attacking = [
            node
            for l_nodes in list(
                map(
                    lambda y: y["Attacking_Nodes"],
                    filter(
                        lambda x: x["Action"] not in self.non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )
            )
            for node in l_nodes
        ]

        all_target = [
            node
            for l_nodes in list(
                map(
                    lambda y: y["Target_Nodes"],
                    filter(
                        lambda x: x["Action"] not in self.non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )
            )
            for node in l_nodes
        ]

        all_success = [
            node
            for l_nodes in list(
                map(
                    lambda y: y["Successes"],
                    filter(
                        lambda x: x["Action"] not in self.non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )
            )
            for node in l_nodes
        ]

        self.network_interface.update_stored_attacks(
            all_attacking, all_target, all_success
        )
        return current_turn_attack_info
