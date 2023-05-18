import random
from typing import Tuple

import gym
import networkx as nx
import numpy as np

from yawning_titan.envs.generic.helpers.graph2plot import CustomEnvGraph


class GraphExplore(gym.Env):
    """
    A custom environment that follows the gym interface spec.

    This environment emulates a network and enables an agent to select which node
    to visit, if it is not possible to move to the node the agent is denied
    the move.
    """

    metadata = {"render.modes": ["human"]}
    NODES = 10  # the number of nodes within the network
    random_seed = 1010  # the initial random_seed of the random network generated
    GAME_MAX = 1000  # the number of game moves allowed
    visualisation = None

    def __init__(self):
        """Initialise environment."""
        print("GAME INIT")
        super(GraphExplore, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects

        # Example when using discrete actions:
        self.G = nx.random_internet_as_graph(n=self.NODES, random_seed=self.random_seed)
        self.pos = nx.spring_layout(self.G)
        self.action_space = gym.spaces.Discrete(self.NODES + 1)
        # Example for using image as input:
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(self.NODES, 1, 1), dtype=np.uint8
        )
        # all can communicate, or none can
        self.reward_range = (-1 * (self.NODES * self.NODES), self.NODES * self.NODES)

        # start blue
        self.INITIAL_BLUE = random.choice(list(self.G.nodes()))
        self.POS_BLUE = self.INITIAL_BLUE

        # blue visit list
        self.BLUE_VISIT = [self.INITIAL_BLUE]

        # current step
        self.CURRENT_STEP = 0

        # score
        self.BLUE_SCORE = 0

    def step(self, action: int) -> Tuple[np.array, float, bool, dict]:
        """Execute one time step within the environment."""
        print(
            "GAME STEP {_step} of {_max}".format(
                _step=1 + self.CURRENT_STEP, _max=self.GAME_MAX
            )
        )
        self._take_action(action)

        self.CURRENT_STEP += 1

        reward = self._calc_reward()

        obs = self._next_observation()

        done = False
        if len(self.BLUE_VISIT) == self.NODES or (self.CURRENT_STEP == self.GAME_MAX):
            done = True
        return obs, reward, done, {}

    def _take_action(self, action: int):
        """Take an action withint the environment from the node chosen to be visited."""
        if action == self.NODES:
            # do nothing
            print("Passing turn")
            pass
        else:
            # attempt to visit node
            print(
                "Currently at node:{current} and want to move to: {future}".format(
                    current=self.POS_BLUE, future=action
                )
            )
            # is possible?
            if action in list(self.G.neighbors(self.POS_BLUE)) or (
                action == self.POS_BLUE
            ):
                # move
                print("Moved to: {future}".format(future=action))
                self.POS_BLUE = action
                try:
                    self.BLUE_VISIT.remove(action)
                except:  # noqa
                    print("Never visited node {future} before".format(future=action))
                self.BLUE_VISIT.append(action)
            else:
                # do not move
                print("Cannot move to: {future}".format(future=action))
                pass

    def _calc_reward(self) -> float:
        """
        Calculate agent reward.

        The defined reward as the total number of nodes visited with
        some penalty to try and coax the the agent into moving.
        """
        return len(self.BLUE_VISIT) - (
            (self.CURRENT_STEP / (1.0 * self.GAME_MAX)) * len(self.BLUE_VISIT)
        )

    def _next_observation(self) -> np.array:
        """
        Get the next observation.

        The observation space is just a list of nodes visited and therefore
        the agent is blind to the connectivity space
        """
        # return has blue visited nodes?
        obs = np.zeros(self.NODES)
        for i in self.BLUE_VISIT:
            obs[i] = 1
        obs = np.array(obs).reshape(self.NODES, 1, 1)
        return obs

    def reset(self) -> np.array:
        """Reset the initial game configurations."""
        # Reset the state of the environment to an initial state
        print("GAME RESET")
        self.CURRENT_STEP = 0
        self.G = nx.random_internet_as_graph(n=self.NODES, random_seed=self.random_seed)
        self.pos = nx.spring_layout(self.G)
        self.INITIAL_BLUE = random.choice(list(self.G.nodes()))
        self.POS_BLUE = self.INITIAL_BLUE
        self.CURRENT_STEP = 0
        self.BLUE_SCORE = 0
        self.BLUE_VISIT = [self.INITIAL_BLUE]
        return self._next_observation()

    def render(self, mode: str = "live", close: bool = False):
        """Render the environment to the screen so that it can be played in realtime."""
        if mode == "file":
            pass
        elif mode == "live":
            print("rendering..")
            if self.visualisation is None:
                self.visualisation = CustomEnvGraph(title="Network Visualisation")
            if self.CURRENT_STEP > 0:
                self.visualisation.render(
                    self.CURRENT_STEP,
                    self.G,
                    self.pos,
                    {},
                    self.BLUE_VISIT,
                    [],
                    self._calc_reward(),
                    None,
                    {i: 0.5 for i in range(len(self.G.nodes))},
                    [self.POS_BLUE],
                    "Graph explore",
                )

    def close(self):
        """Remove all open visualisations."""
        if self.visualisation is not None:
            self.visualisation.close()
            self.visualisation = None
