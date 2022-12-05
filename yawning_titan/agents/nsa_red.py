import logging
import random
from typing import List, Tuple, Union

logger = logging.getLogger(__name__)


class NSARed:
    """
        Provides the red agent behaviour within the `18-node-def` environment.

        The agent is a loose replication of:
    https://www.nsa.gov.Portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9
    """

    def __init__(
        self,
        skill: float,
        action_set: List,
        action_probabilities: List,
        node_set: List,
        zd_start_amount: int = 0,
        zd_gain: int = 0,
        zd_required: int = 10,
    ):
        self.skill = skill
        self.action_set = action_set
        self.action_probabilities = action_probabilities
        self.node_set = node_set
        self.zd_amount = zd_start_amount
        self.zg_gain = zd_gain
        self.zd_required = zd_required
        self.zd_current_day = 0

    def update_node_set(self, nodes: List[int]):
        """
        Update the set of nodes the agent can act upon.

        Args:
            nodes: A list containing the nodes
        """
        self.node_set = nodes

    def update_actions(self, actions: List[str], probabilities: List[float]):
        """
        Update the set of actions and the corresponding probabilities.

        Args:
            actions: the new set of actions the agent can take
            probabilities: the weights associated with the actions

        """
        self.action_set = actions
        self.action_probabilities = probabilities

    def choose_node(self) -> int:
        """
        Choose a node to act on.

        Returns:
            The node to act on

        """
        node = random.choices(self.node_set)[0]

        return node

    def choose_action(self) -> str:
        """
        Choose an action to perform.

        Returns:
            The action to perform on

        """
        action = random.choices(self.action_set, weights=self.action_probabilities)[0]

        return action

    def update_location(self, target: int, red_current_node: int) -> Tuple[int, int]:
        """
        Update the current location of the red agent.

        Args:
            target: the location to move to
            red_current_node: red agents current node

        Returns:
            Reds previous node
            The node red is currently in

        """
        red_previous_node = red_current_node
        red_current_node = target

        return red_previous_node, red_current_node

    def increment_day(self):
        """
        Increment the day related to zero day development.

        If the day has reached a threshold for a zero day then add 1 to the number of available
        zero days.
        """
        if self.zd_current_day == self.zd_required:
            self.zd_amount += 1
            self.zd_current_day = 0
        else:
            self.zd_current_day += 1

    def check_zd_available(self) -> bool:
        """
        Check if a zero day is available .

        Returns:
            True if a zero day is available to use
            False if no zero day is available to use
        """
        if self.zd_amount > 0:
            self.zd_amount -= 1
            return True
        else:
            return False

    def zd_attack(self, target: int, args: Tuple[List[List[float]], int, int, bool]):
        """
        Perform a zd attack on a targetted node.

        Args:
            target: the target node
            args: A tuple containing:
                * "machine_states": the current state of the machines
                * "red_current_node": the red agents current node
                * "able_to_move": if the red agent is able to move
        """
        # extracts args
        [machine_states, red_current_node, _, able_to_move] = args
        machine_states[target][1] = 1
        logger.debug(f"Red Team: Zero Day Used on {target + 1}")
        if able_to_move:
            self.update_location(target, red_current_node)

    def basic_attack(self, target: int, args: Tuple[List[List[float]], int, int, bool]):
        """
        Perform a basic attack on a targetted node.

        Args:
            target: The target node
            args: A tuple containing:
                * "machine_states": the current state of the machines
                * "skill_level": The skill level of the attack
                * "attack_success_threshold": A threshold to determine if the attack succeeds
                * "red_current_node": The current position of the red agent
                * "able_to_move": if the red agent is able to move
        """
        [
            machine_states,
            red_current_node,
            attack_success_threshold,
            able_to_move,
        ] = args

        # Calculate Attack power based on skill level and target vulnerability score/
        attack = (self.skill * machine_states[target][0]) / 100
        logger.debug(f"Red Attack Power: {attack}")
        # If Attack Power greater than ATTACK_SUCCESS_THRESHOLD, compromise machine
        if attack >= attack_success_threshold:
            machine_states[target][1] = 1  # Compromised
            logger.debug(f"Red Team: {attack} on target {target + 1} - SUCCESS")
            if able_to_move:
                self.update_location(target, red_current_node)
        else:
            # If Attack Power below ATTACK_SUCCESS_THRESHOLD, attack failed
            logger.debug(f"Red Team: {attack} on target {target + 1} - FAILED")

    def move(self, target: int, args: Tuple[List[List[float]], int, int, bool]):
        """
        Move the red agent from one node to another.

        Args:
            target: the node the agent is moving to
            args: A tuple containing the following:
                * "red_current_node": the current node of the agent
                * "able_to_move": if the agent is able to move
        """
        [_, red_current_node, _, able_to_move] = args
        if able_to_move:
            logger.debug(f"Red Team: Moved to target {target + 1}")
            self.update_location(target, red_current_node)

    def spread(self, state, args: Tuple[float, float]):
        """
        Attempt to spread to all nodes connected to a compromised node.

        Args:
            state: the current state of the environment
            args: A tuple containing:
                * "chance_to_spread": the chance to spread from one node to another
                * "chance_to_randomly_compromise": chance to randomly infect a node
        """
        [chance_to_spread, _] = args
        logger.debug("Red Action: SPREAD")
        compromised_nodes = state.get_compromised_nodes()
        # runs through all of the compromised nodes
        for i in compromised_nodes:
            connected = state.get_connected_nodes(i)
            for j in connected:
                # tries to spread to every connected node
                chance = random.randint(0, 100)
                if chance < chance_to_spread * 100:
                    state.modify_node(j, [False, 2])
                    logger.debug(f"Spread from: {i} to {j}")

    def intrude(self, state, args: Tuple[float, float]):
        """
        Attempt to randomly intrude every uncompromised node.

        Args:
            state: the current state of the environment
            args: A tuple containing:
                * "chance_to_spread": the chance to spread from one node to another
                * "chance_to_randomly_compromise": chance to randomly infect a node
        """
        [_, chance_to_randomly_compromise] = args
        logger.debug("Red Action: RANDOM INTRUSION")
        uncompromised_nodes = state.get_un_compromised_nodes()
        # tries to compromise every un-compromised node
        for i in uncompromised_nodes:
            chance = random.randint(0, 100)
            if chance < chance_to_randomly_compromise * 100:
                state.modify_node(i, [False, 2])
                logger.debug(f"Compromised: {i}")

    def do_action(
        self,
        nodes: Union[Union[List[int], int], "NodeCollection"],  # noqa
        action: str,
        args: Union[List[float], Tuple[List[List[int]], int, bool]],
    ):
        """
        Perform the selected action on the given target nodes.

        Args:
            nodes: the nodes to perform the action on
            action: the action to perform
                0* - actions for the 5 node env
                1* - actions for the new node env
            args: any parameters needed to perform the action

        """
        dispatch = {
            "00": self.zd_attack,
            "01": self.basic_attack,
            "02": self.move,
            "10": self.spread,
            "11": self.intrude,
        }
        # args: 0: machine_states, 1: red_current_node, 2: attack_sucsess_threshold, 3: able_to_move
        # args: spread, random infect
        dispatch[action](nodes, args)
