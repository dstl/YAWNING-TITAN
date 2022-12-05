from typing import Tuple

from yawning_titan.envs.generic.core.blue_action_set import BlueActionSet
from yawning_titan.envs.generic.core.network_interface import NetworkInterface


class BlueInterface(BlueActionSet):
    """The interface used by the Blue Agents to act within the environment."""

    def __init__(self, network_interface: NetworkInterface):
        """
        Initialise the blue interface.

        Args:
            network_interface: Object from the NetworkInterface class
        """
        super().__init__(network_interface)

        # standard actions (apply to a single node)
        self.action_dict = {}
        action_number = 0
        self.deceptive_actions = 0
        # all of the actions that blue can do
        if self.network_interface.game_mode.blue.blue_uses_reduce_vulnerability:
            # Checks if the action is enabled in the settings file
            self.action_dict[action_number] = self.reduce_node_vulnerability
            action_number += 1
        if self.network_interface.game_mode.blue.blue_uses_restore_node:
            self.action_dict[action_number] = self.restore_node
            action_number += 1
        if self.network_interface.game_mode.blue.blue_uses_make_node_safe:
            self.action_dict[action_number] = self.make_safe_node
            action_number += 1
        if self.network_interface.game_mode.blue.blue_uses_isolate_node:
            self.action_dict[action_number] = self.isolate_node
            action_number += 1
        if self.network_interface.game_mode.blue.blue_uses_reconnect_node:
            self.action_dict[action_number] = self.reconnect_node
            action_number += 1

        # deceptive actions -> since the number of edges is not equal to the number of nodes this has to be done
        # separately
        if self.network_interface.game_mode.blue.blue_uses_deceptive_nodes:
            self.deceptive_actions = self.network_interface.get_number_base_edges()

        # global actions (don't apply to a single node)
        self.global_action_dict = {}
        global_action_number = 0
        if self.network_interface.game_mode.blue.blue_uses_scan:
            # scans all of the nodes in the network
            self.global_action_dict[global_action_number] = self.scan_all_nodes
            global_action_number += 1
        if self.network_interface.game_mode.blue.blue_uses_do_nothing:
            # does nothing
            self.global_action_dict[global_action_number] = self.do_nothing
            global_action_number += 1
        self.number_of_actions = action_number
        self.number_global_action = global_action_number

    def perform_action(self, action: int) -> Tuple[str, str]:
        """
        Perform an action within the environment.

        Takes in an action number and then maps this to the correct action to perform. There are 3 different types of
        actions:
            - standard actions
            - deceptive actions
            - global actions

        --standard actions--
        Standard actions are actions that can apply to all nodes. For each standard action there are n actions (where n
        is the number of nodes in the network). An example of this action would be to isolate a node. The agent has to
        pick the isolate action and then the node it is being applied to.

        --deceptive actions--
        Actions relating to deceptive nodes. Since the number of deceptive actions relate to the edges not the nodes
        (see deceptive nodes for more info), the deceptive actions cannot come under the standard actions. An example
        would be to place a deceptive node. The deceptive nodes can only be placed on an edge so the agent has to pick
        the "place deceptive node" action and then the edge to place it on.

        --global actions--
        Global actions are actions where the agent does not need to pick any sub action other than the action. For
        example an action that applies to all nodes so the agent does not need to pick a specific node to apply the
        action to. "Do nothing" is an example of a global action as there is no secondary choice to be made.


        The function also maps any actions outside of the action space to the "do nothing" action.

        Order of operations:
        1- check if the action is inside the action space --> perform "do nothing"
        2- check if the action is a deceptive action --> perform action
        3- check if the action is a global action --> perform action
        4- perform the standard action

        Args:
            action: the action to perform

        Returns:
            The action that has been taken
            The node the action was performed on
        """
        if action >= self.get_number_of_actions():
            blue_action, blue_node = self.do_nothing()
        elif action < self.deceptive_actions:
            # use a deceptive action
            blue_action, blue_node = self.add_deceptive_node(action)
        # global actions
        else:
            action = action - self.deceptive_actions
            # global actions
            if action < self.number_global_action:

                blue_action, blue_node = self.global_action_dict[action]()
            else:
                # standard actions
                action = action - self.number_global_action
                action_node = int(action / self.number_of_actions)
                if action_node >= self.network_interface.get_number_of_nodes():
                    blue_action, blue_node = self.do_nothing()
                else:
                    action_node = self.network_interface.get_nodes()[action_node]
                    action_taken = int(action % self.number_of_actions)

                    blue_action, blue_node = self.action_dict[action_taken](action_node)

        return blue_action, blue_node

    def get_number_of_actions(self) -> int:
        """
        Get the number of actions that this blue agent can perform.

        There are three types of actions:
            - global actions (apply to all nodes) - need 1 action space
            - deceptive actions (Add new nodes to environment)
            - standard actions (apply to a single node) - need 2 action space (action and node to perform on)

        Returns:
            The number of actions that this agent can perform
        """
        return (
            (self.number_of_actions * self.network_interface.get_total_num_nodes())
            + self.number_global_action
            + self.deceptive_actions
        )
