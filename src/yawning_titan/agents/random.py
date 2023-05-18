from gym import Space


class RandomAgent(object):
    """
    A simple implementation of a Random Agent capable of randomly acting within anOpenAI Gym environment.

    *Note: Both act and predict methods are provided to fit with different tutorials
    online that use different terminology for the same thing.*
    """

    def __init__(self, action_space: Space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        """Randomly sample an action from the action space."""
        return self.action_space.sample()

    def predict(self, observation, reward, done):
        """Randomly sample an action from the action space."""
        return self.action_space.sample()
