"""
A Parent red agent.

This red agent acts as a container for any move that a red agent could want to make. An actual red
agent that would interfaces with the generic Gym environment uses all of or a subset of the methods available here.
All of the methods interact with the network interface to affect the environment.
"""
import copy
import random
from typing import Dict, List, Set, Tuple, Union

from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.networks.node import Node


class RedActionSet:
    """A class representing a Red Agents action set."""

    action_set = []
    action_probabilities = []
    node_set = []

    def __init__(
        self,
        network_interface: NetworkInterface,
        action_set: List[int],
        action_probabilities: List[float],
    ):
        """
        Initialise the red agent.

        Args:
            network_interface: Object from the NetworkInterface class
            action_set: The possible actions that the red agent can take (list)
            action_probabilities: The likelihood of those actions being chosen (list)
        """
        self.network_interface = network_interface
        self.skill = self.network_interface.game_mode.red.agent_attack.skill.value.value
        self.zero_day_amount = (
            self.network_interface.game_mode.red.action_set.zero_day.start_amount.value
        )
        self.zero_day_required = (
            self.network_interface.game_mode.red.action_set.zero_day.days_required.value
        )

        self.action_set = action_set
        self.action_probabilities = action_probabilities

        self.reset()

    def reset(self):
        """Reset red agent episode dependent variables to initial value."""
        self.zero_day_amount = (
            self.network_interface.game_mode.red.action_set.zero_day.start_amount.value
        )
        self.zero_day_current_day = 0

    def choose_target_node(self) -> Union[Tuple[Node, Node], Tuple[bool, bool]]:
        """
        Choose a target node.

        Returns:
            The target node (False if no possible nodes to attack)
            The node attacking the target node (False if no possible nodes to attack)
        """
        # creates a set of nodes that the red agent could attack
        possible_to_attack: Set[Node] = set()
        original_node = {}
        if (
            self.network_interface.game_mode.red.agent_attack.attack_from.any_red_node.value
        ):
            nodes = self.network_interface.current_graph.get_nodes(
                filter_true_compromised=True
            )
            # runs through the connected nodes and adds the safe nodes to a set of possible nodes to attack
            for node in nodes:
                # If red can attack from any compromised node
                connected = self.network_interface.get_current_connected_nodes(node)
                for connected_node in connected:
                    if connected_node.true_compromised_status == 0:
                        original_node[connected_node] = node
                        possible_to_attack.add(connected_node)
        elif (
            self.network_interface.game_mode.red.agent_attack.attack_from.only_main_red_node.value
        ):
            # If red can only attack from the central red node
            if self.network_interface.red_current_location is not None:
                connected = self.network_interface.get_current_connected_nodes(
                    self.network_interface.red_current_location
                )
                for node in connected:
                    if node.true_compromised_status == 0:
                        original_node[
                            node
                        ] = self.network_interface.red_current_location
                        possible_to_attack.add(node)
        # also adds entry nodes into the set of possible nodes. This is the red agents entrance into the network

        for node in self.network_interface.current_graph.entry_nodes:
            if node.true_compromised_status == 0:
                possible_to_attack.add(node)
                original_node[node] = None

        possible_to_attack = sorted(list(possible_to_attack))

        weights = []
        # red can prioritise nodes based on some different parameters chosen in the settings menu
        if self.network_interface.game_mode.red.target_mechanism.random.value:
            # equal weighting for all nodes
            weights = [1] * len(possible_to_attack)
        elif (
            self.network_interface.game_mode.red.target_mechanism.prioritise_connected_nodes.value
        ):
            for node in possible_to_attack:
                # more connections means a higher weight
                weights.append(
                    len(self.network_interface.get_current_connected_nodes(node))
                )
        elif (
            self.network_interface.game_mode.red.target_mechanism.prioritise_unconnected_nodes.value
        ):
            for node in possible_to_attack:
                # higher connections means a lower weight
                current_connected = len(
                    self.network_interface.get_current_connected_nodes(node)
                )
                if current_connected == 0:
                    current_connected = 0.1
                weights.append(1 / current_connected)
        elif (
            self.network_interface.game_mode.red.target_mechanism.prioritise_vulnerable_nodes.value
        ):
            for node in possible_to_attack:
                # higher vulnerability means a higher weight
                weights.append(1 / node.vulnerability_score)
        elif (
            self.network_interface.game_mode.red.target_mechanism.prioritise_resilient_nodes.value
        ):
            for node in possible_to_attack:
                # higher vulnerability means a lower weight
                weights.append(1 / node.vulnerability_score)
        elif (
            self.network_interface.game_mode.red.target_mechanism.target_specific_node.use.value
            or self.network_interface.game_mode.red.target_mechanism.target_specific_node.target.value
            is not None
        ):
            distances = self.network_interface.get_shortest_distances_to_target(
                possible_to_attack
            )
            for dist in distances:
                if (
                    self.network_interface.game_mode.red.target_mechanism.target_specific_node.always_choose_shortest_distance.value
                ):
                    weight = 1 if dist == min(distances) else 0
                else:
                    weight = 1 if dist == 0 else dist / sum(distances)
                weights.append(weight)
        else:
            # if using the configuration checker then this should never happen
            raise Exception(
                "Red should have have a method for how it chooses nodes to attack (enable "
                "red_chooses_targets_at_random in the config file if you are unsure)"
            )

        if len(possible_to_attack) == 0:
            # If the red agent cannot attack anything then return False showing that the attack has failed
            return False, False
        if sum(weights) == 0:
            for counter, i in enumerate(weights):
                weights[counter] = 1
        weights_normal = [float(i) / sum(weights) for i in weights]
        # Chooses a target with some being more likely than others
        target = random.choices(
            population=possible_to_attack, weights=weights_normal, k=1
        )[0]

        # get the node that red attacked from
        attacking_node = original_node[target]

        return target, attacking_node

    def choose_action(self) -> int:
        """
        Choose an action to perform.

        Returns:
            The chosen action to perform
        """
        action = random.choices(
            population=self.action_set, weights=self.action_probabilities, k=1
        )[0]

        return action

    def increment_day(self):
        """Increment the day for zero day attack generation."""
        # If the number of days equals the days required for a zero day then the number of available zero days is
        # increased
        if self.zero_day_current_day == self.zero_day_required:
            self.zero_day_amount += 1
            self.zero_day_current_day = 0
        else:
            self.zero_day_current_day += 1

    def get_amount_zero_day(self) -> int:
        """
        Get the amount of zero day attacks that the red agent has stored up.

        Returns:
            Integer number - amount of zero day attacks
        """
        return self.zero_day_amount

    def random_move(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Select a random connected compromised node to move to.

        Returns:
            A dictionary containing:
                The name of the action
                If the move succeeded
                The new red location
                The old red location
        """
        print("RANDOM MOVE")
        if self.network_interface.red_current_location is None:
            # If the central red agent is not in the environment then it will enter through the entry points
            connected = list(
                set(self.network_interface.current_graph.entry_nodes).intersection(
                    set(
                        self.network_interface.current_graph.get_nodes(
                            filter_true_compromised=True
                        )
                    )
                )
            )
        else:
            # Otherwise the red agent will move to a connected node
            connected = list(
                set(
                    self.network_interface.get_current_connected_nodes(
                        self.network_interface.red_current_location
                    )
                ).intersection(
                    set(
                        self.network_interface.current_graph.get_nodes(
                            filter_true_compromised=True
                        )
                    )
                )
            )
        # gets the current location and copies it. This is for logging purposes to ensure that the red agent moves
        # correctly
        pre = copy.deepcopy(self.network_interface.red_current_location)
        if len(connected) != 0:
            direction = random.choices(population=connected, k=1)[0]
            self.network_interface.red_current_location = direction
            return {
                "Action": "random_move",
                "Attacking_Nodes": [pre],
                "Target_Nodes": [self.network_interface.red_current_location],
                "Successes": [True],
            }

        return {
            "Action": "random_move",
            "Attacking_Nodes": [pre],
            "Target_Nodes": [pre],
            "Successes": [False],
        }

    def do_nothing(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        No-op.

        Returns:
            The name of the action
            If the move succeeded
            The target node
            The current node
        """
        return {
            "Action": "do_nothing",
            "Attacking_Nodes": [],
            "Target_Nodes": [],
            "Successes": [True],
        }

    def zero_day_attack(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Execute a zero-day attack if available.

        Returns:
            The name of the action taken
            If the action succeeded
            The target node
            The attacking node
        """
        if self.get_amount_zero_day() >= 1:
            # Can only use this if there are available zero days
            target, attacking_node = self.choose_target_node()
            if target is False:
                return {
                    "Action": "no_possible_targets",
                    "Attacking_Nodes": [],
                    "Target_Nodes": [],
                    "Successes": [False],
                }
            self.zero_day_amount -= 1
            self.network_interface.attack_node(target, guarantee=True)
            # Moves the red agent to the attacked location
            if self.network_interface.red_current_location is None:
                # moves the red agent into the network if it is not currently
                if target in self.network_interface.current_graph.entry_nodes:
                    self.network_interface.red_current_location = target
            elif target in self.network_interface.get_current_connected_nodes(
                self.network_interface.red_current_location
            ):
                self.network_interface.red_current_location = target
            return {
                "Action": "zero_day",
                "Attacking_Nodes": [attacking_node],
                "Target_Nodes": [target],
                "Successes": [True],
            }
        else:
            return {
                "Action": "zero_day",
                "Attacking_Nodes": [],
                "Target_Nodes": [],
                "Successes": [False],
            }

    def basic_attack(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Execute a basic attack.

        The red agent will attempt to compromise a target node using the predefined attack method.

        Returns:
            The name of the action taken
            If the action succeeded
            The target node
            The attacking node
        """
        target, attacking_node = self.choose_target_node()
        if target is False:
            return {
                "Action": "no_possible_targets",
                "Attacking_Nodes": [],
                "Target_Nodes": [],
                "Successes": [False],
            }
        attack_status = self.network_interface.attack_node(
            target,
            skill=self.skill,
            use_skill=self.network_interface.game_mode.red.agent_attack.skill.use.value,
            use_vulnerability=(
                not self.network_interface.game_mode.red.agent_attack.ignores_defences.value
            ),
            guarantee=self.network_interface.game_mode.red.agent_attack.always_succeeds.value,
        )
        if attack_status:
            # update the location of the red agent if applicable
            if self.network_interface.red_current_location is None:
                if target in self.network_interface.current_graph.entry_nodes:
                    self.network_interface.red_current_location = target
            elif target in self.network_interface.get_current_connected_nodes(
                self.network_interface.red_current_location
            ):
                self.network_interface.red_current_location = target
            return {
                "Action": "basic_attack",
                "Attacking_Nodes": [attacking_node],
                "Target_Nodes": [target],
                "Successes": [True],
            }
        else:
            return {
                "Action": "basic_attack",
                "Attacking_Nodes": [attacking_node],
                "Target_Nodes": [target],
                "Successes": [False],
            }

    def natural_spread(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Naturally spread throughout the network.

        Nodes that are connected to compromised nodes can have a different chance to become compromised.
        The settings for how likely nodes are to become compromised are in the config file.

        Returns:
            The success status of all the attacks
            The target nodes
            The attacking nodes
        """
        # Lists to contain what nodes were attacked and if the attacks succeeded
        success = []
        targets = []
        attacking_nodes = []

        # gets a list of all the compromised nodes
        compromised_nodes = self.network_interface.current_graph.get_nodes(
            filter_true_compromised=True
        )

        # creates a set that is used to store all of the nodes that the red agent naturally spreads to (used to work out
        # what nodes are not easily spread to)
        set_of_spreading_nodes = set()
        attacking_node_map = {}

        for compromised_node in compromised_nodes:
            for node in self.network_interface.get_current_connected_nodes(
                compromised_node
            ):
                if node.true_compromised_status == 0:
                    # add the current node to the set of nodes connected to a compromised node
                    set_of_spreading_nodes.add(node)
                    attacking_node_map[node] = compromised_node

        if (
            self.network_interface.game_mode.red.natural_spreading.chance.to_connected_node.value
            > 0
        ):
            for node in set_of_spreading_nodes:
                if (
                    random.randint(0, 100)
                    < self.network_interface.game_mode.red.natural_spreading.chance.to_unconnected_node.value
                    * 100
                ):
                    # try to naturally spread to the node based on a percentage change listed in the config file
                    attack_status = self.network_interface.attack_node(
                        node,
                        skill=self.skill,
                        use_skill=self.network_interface.game_mode.red.agent_attack.skill.use.value,
                        use_vulnerability=(
                            not self.network_interface.game_mode.red.agent_attack.ignores_defences.value
                        ),
                        guarantee=self.network_interface.game_mode.red.agent_attack.always_succeeds.value,
                    )
                    if attack_status:
                        # If the attack succeeds
                        success.append(True)
                    else:
                        success.append(False)

                    attacking_nodes.append(attacking_node_map[node])
                    targets.append(node)
        if (
            self.network_interface.game_mode.red.natural_spreading.chance.to_connected_node
        ):
            # Calculate the list of nodes that are not connected to a compromised node
            nodes_not_connected_to_red = (
                set(self.network_interface.current_graph.get_nodes())
                .difference(set(compromised_nodes))
                .difference(set_of_spreading_nodes)
            )

            # all the nodes that are not connected to red (has a different chance to naturally spread to)
            for node in nodes_not_connected_to_red:
                if (
                    random.randint(0, 100)
                    < self.network_interface.game_mode.red.natural_spreading.chance.to_connected_node.value
                    * 100
                ):
                    # Try to naturally randomly infect nodes based on a percentage chance in the config file
                    attack_status = self.network_interface.attack_node(
                        node,
                        skill=self.skill,
                        use_skill=self.network_interface.game_mode.red.agent_attack.skill.use.value,
                        use_vulnerability=(
                            not self.network_interface.game_mode.red.agent_attack.ignores_defences.value
                        ),
                        guarantee=self.network_interface.game_mode.red.agent_attack.always_succeeds.value,
                    )
                    targets.append(node)
                    if attack_status:
                        # store the success status of the attack
                        success.append(True)
                    else:
                        success.append(False)
                    attacking_nodes.append(None)

        # return the information about the attacks made during this turn
        return {
            "Action": "natural_spread",
            "Attacking_Nodes": attacking_nodes,
            "Target_Nodes": targets,
            "Successes": success,
        }

    def spread(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Execute a spread attack.

        The red agent will try and spread from every infected node to every connected safe node.
        The chance to spread between two nodes is independent of any other spreading.

        Returns:
            The name of the action
            A list of success status for each node attacked
            A list of the target nodes
            A list of the attacking nodes
        """
        compromised_nodes = []
        # check the nodes red can attack based on the current configuration
        if (
            self.network_interface.game_mode.red.agent_attack.attack_from.any_red_node.value
        ):
            compromised_nodes = self.network_interface.current_graph.get_nodes(
                filter_true_compromised=True
            )
        if (
            self.network_interface.game_mode.red.agent_attack.attack_from.only_main_red_node.value
        ):
            compromised_nodes = [self.network_interface.red_current_location]
        nodes = []
        # store the location the attack originated from
        attacking_nodes = []
        success = []
        for node in compromised_nodes:
            if node is None:
                # If red does not control any nodes then the entry nodes are used
                connected_nodes = self.network_interface.current_graph.entry_nodes
                connected_nodes = [
                    n for n in connected_nodes if n.true_compromised_status == 0
                ]
                attacking_nodes.extend([None] * len(connected_nodes))
            else:
                connected_nodes = self.network_interface.get_current_connected_nodes(
                    node
                )
                connected_nodes = [
                    n for n in connected_nodes if n.true_compromised_status == 0
                ]

                attacking_nodes.extend([node] * len(connected_nodes))
            for connected_node in connected_nodes:
                nodes.append(connected_node)
                attack_status = self.network_interface.attack_node(
                    connected_node,
                    skill=self.network_interface.game_mode.red.action_set.spread.chance.value,
                    use_skill=True,
                    use_vulnerability=(
                        not self.network_interface.game_mode.red.agent_attack.ignores_defences.value
                    ),
                    guarantee=self.network_interface.game_mode.red.agent_attack.always_succeeds.value,
                )
                if attack_status:
                    # If the attack succeeds
                    if node == self.network_interface.red_current_location:
                        self.network_interface.red_current_location = connected_node
                    # Since spread can attack multiple nodes in one go the agent remembers the success of each of the
                    # attacks in a list
                    success.append(True)
                else:
                    success.append(False)

        return {
            "Action": "spread",
            "Attacking_Nodes": attacking_nodes,
            "Target_Nodes": nodes,
            "Successes": success,
        }

    def intrude(self) -> Dict[str, List[Union[bool, str, None]]]:
        """
        Execute an attack on all nodes simultaneously.

        The red agent will try to infect every safe node at once (regardless of connectivity).
        The chance for the red agent to compromise a node is independent to each of the other nodes

        Returns:
            The name of the action
            A list of success status for each node attacked
            A list of the target nodes
            A list of the attacking nodes
        """
        # gets the nodes that are currently safe
        safe_nodes = self.network_interface.current_graph.get_nodes(
            filter_true_safe=True
        )
        success = []
        nodes = []
        attacking_nodes = []
        # tries to attack the safe nodes
        for node in safe_nodes:
            attack_status = self.network_interface.attack_node(
                node,
                skill=self.network_interface.game_mode.red.action_set.random_infect.chance.value,
                use_skill=True,
                use_vulnerability=(
                    not self.network_interface.game_mode.red.agent_attack.ignores_defences.value
                ),
                guarantee=self.network_interface.game_mode.red.agent_attack.always_succeeds.value,
            )
            nodes.append(node)
            if attack_status:
                # Agent remembers each of the successes or failures for each node it
                # attempts to intrude
                success.append(True)
            else:
                success.append(False)
            attacking_nodes.append(None)
        return {
            "Action": "intrude",
            "Attacking_Nodes": attacking_nodes,
            "Target_Nodes": nodes,
            "Successes": success,
        }
