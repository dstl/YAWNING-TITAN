Enhancing Yawning Titan
========================

Yawning Titan has been built to allow easy addition and modification
of large sections. It is very easy to add:

 * Reward functions
 * Red actions
 * Blue actions
 * Red agents


Reward Functions
****************

To create a new reward function navigate to:

    yawning_titan/envs/generic/core/reward_functions.py

Here you will find all of the current reward functions. To add a new
reward function yo just have to add a new function with the following
form::

    def new_rewards(args: dict) -> float:

Args will contain certain stats from the current network that you can
use to determine your rewards.

 * network_interface: Interface with the network
 * blue_action: The action that the blue agent has taken this turn
 * blue_node: The node that the blue agent has targeted for their action
 * start_state: The state of the nodes before the blue agent has taken their action
 * end_state: The state of the nodes after the blue agent has taken their action
 * start_vulnerabilities: The vulnerabilities before blue agents turn
 * end_vulnerabilities: The vulnerabilities after the blue agents turn
 * start_isolation: The isolation status of all the nodes at the start of a turn
 * end_isolation: The isolation status of all the nodes at the end of a turn
 * start_blue: The env as the blue agent can see it before the blue agents turn
 * end_blue: The env as the blue agent can see it after the blue agents turn


Red Actions
************

To create a new red action navigate to:

    yawning_titan/envs/generic/core/red_action_set.py

There you can see all of the current actions and create your own.
To create your own action it must follow the following form::

    def new_action(self) -> Tuple[str, List[bool], List[Union[str, None]], List[Union[str, None]]]

This means that it returns:
 * The name of the action (string)
 * A list of successes (boolean)
 * A list of target nodes (List of strings)
 * A list of attacking nodes (List of strings)

You then have to tell the red agent that it can use this new action.
To do this you have to add a new setting to the config file for this new action.::

    RED:
        red_uses_new_action: True
        new_action_likelihood: 1

And then in the red interface::

    if settings_file["RED"]["red_uses_new_action"]:
        self.action_dict[action_number] = self.new_action
        action_set.append(action_number)
        probabilities_set.append(settings_file["RED"]["new_action_likelihood"])
        action_number += 1

And finally if the action is not an attacking action then it needs to be added to
the list of non attacking actions in the red_interface::

    self.non_attacking_actions = ["do_nothing", "random_move", "new_action"]


Blue Actions
*************

Adding blue actions are slightly more complicated as there are 3 types
of blue actions:

 * General actions
    Act on a single node
 * Global actions
    Act on every node
 * Deceptive actions
    Act on every link between nodes

First navigate to the action set location:

    yawning_titan/envs/generic/core/blue_action_set.py

Adding a general action
^^^^^^^^^^^^^^^^^^^^^^^

Create an action with the form::

    def new_action(self, node: str) -> Tuple[str, str]

Add the action to the config file::

    BLUE:
        blue_uses_new_action: True

Then add the action to the interface::

    if self.settings["BLUE"]["blue_uses_new_action"]:
        self.action_dict[action_number] = self.new_action
        action_number += 1


Adding a Global action
^^^^^^^^^^^^^^^^^^^^^^^

Create an action with the form::

    def new_action(self) -> Tuple[str, str]

Add the action to the config file::

    BLUE:
        blue_uses_new_action: True

Add the action to the interface::

    if self.settings["BLUE"]["blue_uses_new_action"]:
        self.global_action_dict[global_action_number] = self.new_action
        global_action_number += 1


Adding a new Red Agent
^^^^^^^^^^^^^^^^^^^^^^^

First step is to look at the red_interface and advanced_red_interface:

    yawning_titan/envs/generic/core/red_interface.py

    yawning_titan/envs/generic/core/advanced_red_interface.py

Then to create a new interface you want a class with the following:

 * Inherits from RedInterface::

    class NewInterface(RedInterface):

 * An init method::

    def __init__(self, network_interface):
        super().__init__(network_interface)

 * A perform action method::

    def perform_action(self) -> Tuple[str, Union[bool, List[bool]], Union[List[str], str], Union[List[str], str], Tuple[List[str], List[bool]]]:

Where the perform action returns the:
 * name
    The name of the action performed
 * success
    A list of successes from the action
 * target
    A list of targets for the action
 * attacking_nodes
    A list of attacking nodes for the action
 * (n_target, n_success)
    Target and success rates for any natural spreading that occurred

It is also important that after calling calling any abilities that attack nodes you also need to use the following to update the list of known stored attacks::

    self.network_interface.update_stored_attacks(all_attacking_nodes, all_target_nodes, all_success)
