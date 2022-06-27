from typing import Tuple


class Node:
    """Class representing a the state of single node within the Ridley 17 inspired environment."""

    def __init__(self):
        self.isolated = False
        self.compromised = False

    def get_condition(self) -> Tuple[int, int]:
        """
        Return the condition of the node.

        Returns:
            reward: a list containing the isolation and compromised status of the node ([bool, bool])
        """
        return self.isolated, self.compromised

    def change_isolated(self):
        """
        Change the isolation status of a node.

        Flips it so if it was true it becomes false and vice versa
        """
        if self.isolated:
            self.isolated = False
        else:
            self.isolated = True

    def change_compromised(self, mode: int):
        """
        Change the compromised status of a node.

        Args:
            mode: either 0, 1 or 2
                0: does nothing
                1: changes the node to safe
                2: changes the node to compromised
        """
        if mode == 0:
            pass
        elif mode == 1:
            self.compromised = False
        else:
            self.compromised = True
