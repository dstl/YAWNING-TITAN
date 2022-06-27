"""
Util to print out agent evaluation metrics.

The metrics printed out are:
    - Total episodes elapsed
    - Absolute wins for red and blue
    - Percentage win rate for red and blue
    - Average episode length
    - Actions taken by blue each game/Average actions taken by blue over n games
"""

from collections import Counter, defaultdict
from typing import List, Tuple

from tabulate import tabulate


class EvalPrintout:
    """Class to represnt an Eval Printer."""

    def __init__(self, avg_every: int):
        """
        Initialise printout object.

        Args:
            avg_every: Number of timesteps to average stats over
        """
        # Assert that the number of timesteps to average over must be a positive, non-zero integer
        if avg_every < 1:
            raise ValueError("avg_every must be greater than or equal to 1")
        elif not (isinstance(avg_every, int)):
            raise ValueError("avg_every must be an integer")
        self.avg_every = avg_every

    def print_stats(self, game_stats_list: List[dict], total_games: int):
        """
        Print out the (averaged) stats from the last avg_every number of games to the console.

        Args:
            game_stats_list: List of dictionaries containing the last avg_every number of game stats
            total_games: Total games played since starting
        """
        print("--Game over--")
        print("Total number of Games Played: ", total_games)

        # Calculate average metrics from the list of individual game metrics
        (
            blue_wins,
            red_wins,
            percentage_blue,
            percentage_red,
            avg_duration,
            avg_actions,
        ) = self.calculate_metrics(game_stats_list)

        # If printing every game, no need to print blue/red win ratio
        if self.avg_every == 1:
            print(game_stats_list[-1]["Winner"], "wins!")
            print("Episode length: ", game_stats_list[-1]["Duration"])
        # If printing every avg_every games, use different messages and print blue/red win ratio
        else:
            print(f"Stats over the last {self.avg_every} games:")
            print("Average episode length: ", avg_duration, "\n")
            print(
                tabulate(
                    [
                        (blue_wins, red_wins),
                        (f"{percentage_blue}%", f"{percentage_red}%"),
                    ],
                    headers=["Blue Won", "Red Won"],
                )
            )
            print("\n")

        # Print actions used by blue
        print(
            tabulate(
                [(x[0], x[1][0], f"{x[1][1]}%") for x in list(avg_actions)],
                headers=["Action", "Avg Times Used", "Percentage of Action Usage"],
            )
        )
        print("\n\n")

    def calculate_metrics(
        self, game_stats_list: List[dict]
    ) -> Tuple[int, int, float, float, int, list]:
        """
        Calculate the metrics to be printed.

        Args:
            game_stats_list: List of dictionaries containing the last avg_every number of game stats

        Returns:
            blue_wins: Number of games blue won in the last avg_every number of games
            red_wins: Number of games red won in the last avg_every number of games
            percentage_blue: Percentage of games blue won in the last avg_every number of games
            percentage_red: Percentage of games red won in the last avg_every number of games
            avg_duration: Average number of timesteps per episode over the last avg_every number of games
            sorted_actions: Dictionary of actions taken by blue, averaged over the last avg_every number of games
                            and ordered by frequency of each action from highest to lowest. Dictionary values are
                            tuples: (average frequency of action, action usage percentage)
        """
        winner_list = []
        duration_list = []
        action_list = []

        cumulative_actions = Counter({})
        combined_actions = defaultdict(list)
        blue_wins = 0
        red_wins = 0

        # Split stats list into separate lists containing winners, game durations, and actions taken by blue
        for game in game_stats_list:
            game_actions = {}

            winner_list.append(game["Winner"])
            duration_list.append(game["Duration"])
            for k, v in game.items():
                if k not in ["Winner", "Duration"]:
                    game_actions[k] = v
            action_list.append(game_actions)

        # Count how many times blue and red won
        for winner in winner_list:
            if winner == "blue":
                blue_wins += 1
            else:
                red_wins += 1

        # Calculate blue/red win ratios
        percentage_blue = round((blue_wins / self.avg_every) * 100, 2)
        percentage_red = round((red_wins / self.avg_every) * 100, 2)

        # Calculate the average number of timesteps that episodes last for
        total_duration = sum(duration_list)
        avg_duration = round(total_duration / self.avg_every)

        # Calculate blue's average usage for each action
        for actions in action_list:
            cumulative_actions += actions

        avg_actions = {
            k: round(v / self.avg_every) for k, v in dict(cumulative_actions).items()
        }

        # Calculate percentage of blue's action usage for each action
        total_actions = sum(avg_actions.values())

        if total_actions == 0:
            total_actions = 1

        percentage_actions = {
            k: round((v / total_actions) * 100, 2) for k, v in avg_actions.items()
        }

        # Combine average action usage and percentage of action usage into the same dictionary (values are tuples)
        for d in (avg_actions, percentage_actions):
            for k, v in d.items():
                combined_actions[k].append(v)

        # Sort the actions in order from highest average usage to lowest
        sorted_actions = sorted(
            combined_actions.items(), key=lambda item: item[1], reverse=True
        )

        return (
            blue_wins,
            red_wins,
            percentage_blue,
            percentage_red,
            avg_duration,
            sorted_actions,
        )
