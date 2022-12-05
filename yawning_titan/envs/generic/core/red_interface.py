from typing import Dict, List, Union

from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_action_set import RedActionSet

"""
An interface to the parent red agent that selects what actions it wants to use base on the settings and then uses a
dictionary to call these actions.
"""


class RedInterface(RedActionSet):
    """The interface used by the Red Agents to act within the environment."""

    def __init__(self, network_interface: NetworkInterface):
        """
        Initialise the red interface.

        Args:
            network_interface: Object from the NetworkInterface class
        """
        self.network_interface = network_interface
        self.non_attacking_actions = ["do_nothing", "random_move"]

        self.action_dict = {}
        action_set = []
        probabilities_set = []
        action_number = 0
        # Goes through the actions that the red agent can perform
        if self.network_interface.game_mode.red.red_uses_spread_action:
            # If the action is enabled in the settings files then add to list of possible actions
            self.action_dict[action_number] = self.spread
            action_set.append(action_number)
            # also gets the weight for the action (likelihood action is performed) from the settings file
            probabilities_set.append(
                self.network_interface.game_mode.red.spread_action_likelihood
            )
            action_number += 1
        if self.network_interface.game_mode.red.red_uses_random_infect_action:
            self.action_dict[action_number] = self.intrude
            action_set.append(action_number)
            probabilities_set.append(
                self.network_interface.game_mode.red.random_infect_action_likelihood
            )
            action_number += 1
        if self.network_interface.game_mode.red.red_uses_basic_attack_action:
            self.action_dict[action_number] = self.basic_attack
            action_set.append(action_number)
            probabilities_set.append(
                self.network_interface.game_mode.red.basic_attack_action_likelihood
            )
            action_number += 1
        if self.network_interface.game_mode.red.red_uses_do_nothing_action:
            self.action_dict[action_number] = self.do_nothing
            action_set.append(action_number)
            probabilities_set.append(
                self.network_interface.game_mode.red.do_nothing_action_likelihood
            )
            action_number += 1
        if self.network_interface.game_mode.red.red_uses_move_action:
            self.action_dict[action_number] = self.random_move
            action_set.append(action_number)
            probabilities_set.append(
                self.network_interface.game_mode.red.move_action_likelihood
            )
            action_number += 1

        # normalises the weights so they work with numpy choices
        probabilities_set_normal = [
            float(i) / sum(probabilities_set) for i in probabilities_set
        ]

        super().__init__(network_interface, action_set, probabilities_set_normal)

    def perform_action(self) -> Dict[int, Dict[str, List[Union[bool, str, None]]]]:
        """
        Chooses and then performs an action.

        This is called for every one of the red agents turns

        Returns:
            A tuple containing the name of the action, the success status, the target, the attacking node and any natural spreading attacks
        """
        current_turn_attack_info = {}
        action_count = 0

        if self.network_interface.game_mode.red.red_can_naturally_spread:
            current_turn_attack_info[action_count] = self.natural_spread()
            action_count += 1

        zd = False
        # tries to use a zero day attack if it is enabled (not in the main dictionary as it tries it every turn)
        if self.network_interface.game_mode.red.red_uses_zero_day_action:
            inter = self.zero_day_attack()
            if True in inter["Successes"]:
                current_turn_attack_info[action_count] = inter
                zd = True
                action_count += 1
        if zd is False:
            # chooses an action
            action = self.choose_action()

            # performs the action
            current_turn_attack_info[action_count] = self.action_dict[action]()
            action_count += 1

            # If there are no possible targets for an attack then red will attempt to move to a new node
            if (
                current_turn_attack_info[action_count - 1]["Action"]
                == "no_possible_targets"
            ):
                current_turn_attack_info[action_count] = self.random_move()
                action_count += 1
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
