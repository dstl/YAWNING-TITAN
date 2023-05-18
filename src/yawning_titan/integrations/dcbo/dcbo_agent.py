import random


class DCBOAgent(object):
    """An agent class that provides the supporting methods for a DCBO based learner."""

    def __init__(self, action_space, initial_probabilities):
        self.action_space = action_space
        self.probabilities = initial_probabilities
        self.isolated_nodes = {}

    def update_probabilities(self, new_probabilities) -> None:
        """
        Update the DCBO action probabilities.

        Args:
            new_probabilities: The output of a DCBO optimisation step
        """
        self.probabilities = new_probabilities

    def act(self, observation, reward, done):
        """
        Act within the environment.

        This function is not completely implemented and is named to
        support random actions within OpenAI Gym envs.
        """
        return self.action_space.sample()

    def reset(self):
        """Reset the Agent back to initial config by resetting the `isolated_nodes`."""
        self.isolated_nodes = {}

    def predict(self, observation, reward, done, env):
        """
        Predict what action should be used next.

        This is again named the same as an RL based learner but
        operates differently under the hood.

        As DCBO calculates the action probabilities in time slices,
        the predict step here is sampling an action according to the action probabilities
        returned by the most recent DCBO step.
        """
        action_nodes = {}

        for i in range(len(self.probabilities)):
            action_nodes[i] = []
        node_counter = 0
        for i in range(self.action_space.n):
            action_nodes[node_counter].append(i)
            node_counter += 1
            if node_counter == len(self.probabilities):
                node_counter = 0

        to_remove = []
        for key in self.isolated_nodes.keys():
            self.isolated_nodes[key] -= 1
            if self.isolated_nodes[key] == 0:
                env.BLUE.perform_action(action_nodes[1][key])
                to_remove.append(key)

        for i in to_remove:
            self.isolated_nodes.pop(i)

        chosen_action = random.choices(
            [i for i in range(len(self.probabilities))],
            weights=[float(i) / sum(self.probabilities) for i in self.probabilities],
            k=1,
        )[0]

        actionable_nodes = action_nodes[chosen_action]

        if chosen_action == 1:
            action = random.randint(0, len(actionable_nodes) - 1)
            self.isolated_nodes[action] = 5
            return actionable_nodes[action]
        else:
            try:
                node = list(
                    env.network_interface.get_all_node_blue_view_compromised_states().values()
                ).index(1)
                return actionable_nodes[node]
            except ValueError:
                return random.choice(actionable_nodes)
