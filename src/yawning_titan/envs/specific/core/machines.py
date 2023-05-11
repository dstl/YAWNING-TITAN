import random
from typing import List


class Machines:
    """
    Class that represents a collection of machines.

    Sets the initial state for the machines within the environment and
    randomly generates vulnerability scores for each machine
    """

    def __init__(
        self,
        n_machines: int = 5,
        vuln_score_ub: float = 0.80,
        vuln_score_lb: float = 0.40,
    ):
        self.n_machines = n_machines
        self.vuln_score_upper_bound = vuln_score_ub
        self.vuln_score_lower_bound = vuln_score_lb
        self.machine_states = self.init_machines()
        self.initial_states = self.get_initial_state()

    def init_machines(self) -> List[List[float]]:
        """
        Generate a set of machines state pairs.

        Each pair has a vulnerability score between the
        upper and lower bound values provided and a 0
        to denote uncompromised state

        Returns:
            A list of fresh machine states pairs.

        Example:
            [[0.74,0],[0.47,0],[0.62, 0],[0.52, 0],[0.83,0]]
        """
        machine_states = []

        for _ in range(self.n_machines):
            # generate vulnerability
            vuln_score = (
                random.randint(
                    (self.vuln_score_lower_bound * 100),
                    (self.vuln_score_upper_bound * 100),
                )
                / 100.0
            )
            vuln_score = round(vuln_score, 2)

            machine_state = [vuln_score, 0]
            machine_states.append(machine_state)

        return machine_states

    def get_initial_state(self) -> List[List[float]]:
        """
        Get the initial states of the machines.

        Returns:
            The initial machine states

        Notes: This is required in order to ensure that the initial
        states are saved properly.
        """
        initial_states = []
        for i in self.machine_states:
            temp = []
            for j in i:
                temp.append(j)
            initial_states.append(temp)

        return initial_states
