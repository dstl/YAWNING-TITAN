"""
A generic class that creates Open AI environments within YAWNING TITAN.

This class has several key inputs which determine aspects of the environment such
as how the red agent behaves, what the red team and blue team objectives are, the size
and topology of the network being defended and what data should be collected during the simulation.
"""

import copy
import json
from collections import Counter
from typing import Dict, Tuple

import gym
import numpy as np
from gym import spaces
from stable_baselines3.common.utils import set_random_seed

import yawning_titan.envs.generic.core.reward_functions as reward_functions
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.helpers.eval_printout import EvalPrintout
from yawning_titan.envs.generic.helpers.graph2plot import CustomEnvGraph


class GenericNetworkEnv(gym.Env):
    """Class to create a generic YAWNING TITAN gym environment."""

    def __init__(
        self,
        red_agent: RedInterface,
        blue_agent: BlueInterface,
        network_interface: NetworkInterface,
        print_metrics: bool = False,
        show_metrics_every: int = 1,
        collect_additional_per_ts_data: bool = True,
        print_per_ts_data: bool = False,
    ):
        """
        Initialise the generic network environment.

        Args:
            red_agent: Object from the RedInterface class
            blue_agent: Object from the BlueInterface class
            network_interface: Object from the NetworkInterface class
            print_metrics: Whether or not to print metrics (boolean)
            show_metrics_every: Number of timesteps to show summary metrics (int)
            collect_additional_per_ts_data: Whether or not to collect additional per timestep data (boolean)
            print_per_ts_data: Whether or not to print collected per timestep data (boolean)

        Note: The ``notes`` variable returned at the end of each timestep contains the per
        timestep data. By default it contains a base level of info required for some of the
        reward functions. When ``collect_additional_per_ts_data`` is toggled on, a lot more
        data is collected.
        """
        super(GenericNetworkEnv, self).__init__()

        self.RED = red_agent
        self.BLUE = blue_agent
        self.blue_actions = blue_agent.get_number_of_actions()
        self.network_interface = network_interface
        self.current_duration = 0
        self.game_stats_list = []
        self.num_games_since_avg = 0
        self.avg_every = show_metrics_every
        self.current_game_blue = {}
        self.current_game_stats = {}
        self.total_games = 0
        self.made_safe_nodes = []
        self.current_reward = 0
        self.print_metrics = print_metrics
        self.print_notes = print_per_ts_data

        self.random_seed = self.network_interface.random_seed

        self.graph_plotter = None
        self.eval_printout = EvalPrintout(self.avg_every)

        self.action_space = spaces.Discrete(self.blue_actions)

        self.network_interface.get_observation_size()

        # sets up the observation space. This is a (n+2 by n) matrix. The first two columns show the state of all the
        # nodes. The remaining n columns show the connections between the nodes (effectively the adjacency matrix)
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(self.network_interface.get_observation_size(),),
            dtype=np.float32,
        )

        # The gym environment can only properly deal with a 1d array so the observation is flattened

        self.collect_data = collect_additional_per_ts_data
        self.env_observation = self.network_interface.get_current_observation()

    def reset(self) -> np.array:
        """
        Reset the environment to the default state.

        :todo: May need to add customization of cuda setting.

        :return: A new starting observation (numpy array).
        """
        if self.random_seed is not None:  # conditionally set random_seed
            set_random_seed(self.random_seed, True)
        self.network_interface.reset()
        self.RED.reset()
        self.current_duration = 0
        self.env_observation = self.network_interface.get_current_observation()
        self.current_game_blue = {}

        return self.env_observation

    def step(self, action: int) -> Tuple[np.array, float, bool, Dict[str, dict]]:
        """
        Take a time step and executes the actions for both Blue RL agent and non-learning Red agent.

        Args:
            action: The action value generated from the Blue RL agent (int)

        Returns:
             A four tuple containing the next observation as a numpy array,
             the reward for that timesteps, a boolean for whether complete and
             additional notes containing timestep information from the environment.
        """
        # sets the nodes that have been made safe this turn to an empty list
        self.made_safe_nodes = []

        # Gets the initial states of various states for logging and testing purposes
        if self.collect_data:
            # notes collects information about the state of the env
            notes = {
                "initial_state": self.network_interface.get_all_node_compromised_states(),
                "initial_blue_view": self.network_interface.get_all_node_blue_view_compromised_states(),
                "initial_vulnerabilities": self.network_interface.get_all_vulnerabilities(),
                "initial_red_location": copy.deepcopy(
                    self.network_interface.red_current_location
                ),
                "initial_graph": self.network_interface.get_current_graph_as_dict(),
                "current_step": self.current_duration,
            }
        else:
            # If not logging everything, the program still needs to collect some information (required by other parts
            # of the program)
            notes = {}

        # resets the attack list for the red agent (so that only the current turns attacks are held)
        self.network_interface.reset_stored_attacks()

        # The red agent performs their turn
        if (
            self.network_interface.game_mode.game_rules.grace_period_length.value
            <= self.current_duration
        ):
            red_info = self.RED.perform_action()
        else:
            red_info = {
                0: {
                    "Action": "do_nothing",
                    "Attacking_Nodes": [],
                    "Target_Nodes": [],
                    "Successes": [True],
                }
            }
        # Gets the number of nodes that are safe
        number_uncompromised = len(
            self.network_interface.current_graph.get_nodes(filter_true_safe=True)
        )

        # Collects data on the natural spreading
        if self.collect_data:
            notes["red_info"] = red_info

        # The states of the nodes after red has had their turn (Used by the reward functions)
        notes[
            "post_red_state"
        ] = self.network_interface.get_all_node_compromised_states()
        # Blues view of the environment after red has had their turn
        notes[
            "post_red_blue_view"
        ] = self.network_interface.get_all_node_blue_view_compromised_states()
        # A dictionary of vulnerabilities after red has had their turn
        notes[
            "post_red_vulnerabilities"
        ] = self.network_interface.get_all_vulnerabilities()
        # The isolation status of all the nodes
        notes["post_red_isolation"] = self.network_interface.get_all_isolation()

        # collects extra data if turned on
        if self.collect_data:
            # The location of the red agent after red has had their turn
            notes["post_red_red_location"] = copy.deepcopy(
                self.network_interface.red_current_location
            )

        # set up initial variables that are reassigned based on the action that blue takes
        done = False
        reward = 0
        blue_action = ""
        blue_node = None

        # Check if the game is over and red has won
        if (
            self.network_interface.game_mode.game_rules.blue_loss_condition.all_nodes_lost.value
        ):
            if number_uncompromised == 0:
                done = True
                reward = self.network_interface.game_mode.rewards.for_loss.value
                blue_action = "failed"
        if (
            self.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.use.value
        ):
            # calculate the number of safe nodes
            percent_comp = (
                len(
                    self.network_interface.current_graph.get_nodes(
                        filter_true_compromised=True
                    )
                )
                / self.network_interface.current_graph.number_of_nodes()
            )
            if (
                percent_comp
                >= self.network_interface.game_mode.game_rules.blue_loss_condition.n_percent_nodes_lost.value.value
            ):
                done = True
                reward = self.network_interface.game_mode.rewards.for_loss.value
                # If the game ends before blue has had their turn the the blue action is set to failed
                blue_action = "failed"
        if (
            self.network_interface.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value
        ):
            # check if a high value node was compromised
            compromised_hvn = False
            for hvn in self.network_interface.current_graph.high_value_nodes:
                if hvn.true_compromised_status == 1:
                    compromised_hvn = True
                    break

            if compromised_hvn:
                # If this mode is selected then the game ends if the high value node has been compromised
                done = True
                reward = self.network_interface.game_mode.rewards.for_loss.value
                blue_action = "failed"

        # if self.network_interface.gr_loss_tn:
        tn = self.network_interface.get_target_node()
        if (
            tn is not None
            and self.network_interface.game_mode.game_rules.blue_loss_condition.target_node_lost.value
        ):
            if tn.true_compromised_status == 1:
                # If this mode is selected then the game ends if the target node has been compromised
                done = True
                reward = self.network_interface.game_mode.rewards.for_loss.value
                blue_action = "failed"

        if done:
            if (
                self.network_interface.game_mode.rewards.reduce_negative_rewards_for_closer_fails.value
            ):
                reward = reward * (
                    1
                    - (
                        self.current_duration
                        / self.network_interface.game_mode.game_rules.max_steps.value
                    )
                )
        if not done:
            blue_action, blue_node = self.BLUE.perform_action(action)

            if blue_action == "make_node_safe" or blue_action == "restore_node":
                self.made_safe_nodes.append(blue_node)

            if blue_action in self.current_game_blue:
                self.current_game_blue[blue_action] += 1
            else:
                self.current_game_blue[blue_action] = 1

            # calculates the reward from the current state of the network
            reward_args = {
                "network_interface": self.network_interface,
                "blue_action": blue_action,
                "blue_node": blue_node,
                "start_state": notes["post_red_state"],
                "end_state": self.network_interface.get_all_node_compromised_states(),
                "start_vulnerabilities": notes["post_red_vulnerabilities"],
                "end_vulnerabilities": self.network_interface.get_all_vulnerabilities(),
                "start_isolation": notes["post_red_isolation"],
                "end_isolation": self.network_interface.get_all_isolation(),
                "start_blue": notes["post_red_blue_view"],
                "end_blue": self.network_interface.get_all_node_blue_view_compromised_states(),
            }

            reward = getattr(
                reward_functions,
                self.network_interface.game_mode.rewards.function.value,
            )(reward_args)

            # gets the current observation from the environment
            self.env_observation = (
                self.network_interface.get_current_observation().flatten()
            )
            self.current_duration += 1

            # if the total number of steps reaches the set end then the blue agent wins and is rewarded accordingly
            if (
                self.current_duration
                == self.network_interface.game_mode.game_rules.max_steps.value
            ):
                if (
                    self.network_interface.game_mode.rewards.end_rewards_are_multiplied_by_end_state.value
                ):
                    reward = (
                        self.network_interface.game_mode.rewards.for_reaching_max_steps.value
                        * (
                            len(
                                self.network_interface.current_graph.get_nodes(
                                    filter_true_safe=True
                                )
                            )
                            / self.network_interface.current_graph.number_of_nodes()
                        )
                    )
                else:
                    reward = (
                        self.network_interface.game_mode.rewards.for_reaching_max_steps.value
                    )
                done = True

        # Gets the state of the environment at the end of the current time step
        if self.collect_data:
            # The blues view of the network
            notes[
                "end_blue_view"
            ] = self.network_interface.get_all_node_blue_view_compromised_states()
            # The state of the nodes (safe/compromised)
            notes[
                "end_state"
            ] = self.network_interface.get_all_node_compromised_states()
            # A dictionary of vulnerabilities
            notes[
                "final_vulnerabilities"
            ] = self.network_interface.get_all_vulnerabilities()
            # The location of the red agent
            notes["final_red_location"] = copy.deepcopy(
                self.network_interface.red_current_location
            )

        if (
            self.network_interface.game_mode.miscellaneous.output_timestep_data_to_json.value
        ):
            current_state = self.network_interface.create_json_time_step()
            self.network_interface.save_json(current_state, self.current_duration)

        if self.print_metrics and done:
            # prints end of game metrics such as who won and how long the game lasted
            self.num_games_since_avg += 1
            self.total_games += 1

            # Populate the current game's dictionary of stats with the episode winner and the number of timesteps
            if (
                self.current_duration
                == self.network_interface.game_mode.game_rules.max_steps.value
            ):
                self.current_game_stats = {
                    "Winner": "blue",
                    "Duration": self.current_duration,
                }
            else:
                self.current_game_stats = {
                    "Winner": "red",
                    "Duration": self.current_duration,
                }

            # Add the actions taken by blue during the episode to the stats dictionary
            self.current_game_stats.update(self.current_game_blue)

            # Add the current game dictionary to the list of dictionaries to average over
            self.game_stats_list.append(Counter(dict(self.current_game_stats.items())))

            # Every self.avg_every episodes, print the stats to console
            if self.num_games_since_avg == self.avg_every:
                self.eval_printout.print_stats(self.game_stats_list, self.total_games)

                self.num_games_since_avg = 0
                self.game_stats_list = []

        self.current_reward = reward

        if self.collect_data:
            notes["safe_nodes"] = len(
                self.network_interface.current_graph.get_nodes(filter_true_safe=True)
            )
            notes["blue_action"] = blue_action
            notes["blue_node"] = blue_node
            notes["attacks"] = self.network_interface.true_attacks
            notes["end_isolation"] = self.network_interface.get_all_isolation()

        if self.print_notes:
            json_data = json.dumps(notes)
            print(json_data)
        # Returns the environment information that AI gym uses and all of the information collected in a dictionary
        return self.env_observation, reward, done, notes

    def render(
        self,
        mode: str = "human",
        show_only_blue_view: bool = False,
        show_node_names: bool = False,
    ):
        """
        Render the environment using Matplotlib to create an animation.

        Args:
            mode: the mode of the rendering
            show_only_blue_view: If true shows only what the blue agent can see
            show_node_names: Show the names of the nodes
        """
        if self.graph_plotter is None:
            self.graph_plotter = CustomEnvGraph()

        # gets the networkx object

        # compromised nodes is a dictionary of all the compromised nodes with a 1 if the compromise is known or a 0 if
        # not
        # gets information about the current state from the network interface
        main_graph = self.network_interface.current_graph
        if show_only_blue_view:
            attacks = self.network_interface.detected_attacks
        else:
            attacks = self.network_interface.true_attacks
        reward = round(self.current_reward, 2)

        # sends the current information to a graph plotter to display the information visually
        self.graph_plotter.render(
            current_step=self.current_duration,
            g=main_graph,
            attacked_nodes=attacks,
            current_time_step_reward=reward,
            # self.network_interface.red_current_location,
            made_safe_nodes=self.made_safe_nodes,
            target_node=self.network_interface.get_target_node(),
            # "RL blue agent vs probabilistic red in a generic network environment",
            show_only_blue_view=show_only_blue_view,
            show_node_names=show_node_names,
        )

    def calculate_observation_space_size(self, with_feather: bool) -> int:
        """
        Calculate the observation space size.

        This is done using the current active observation space configuration
        and the number of nodes within the environment.

        Args:
            with_feather: Whether to include the size of the Feather Wrapper output

        Returns:
            The observation space size
        """
        return self.network_interface.get_observation_size_base(with_feather)
