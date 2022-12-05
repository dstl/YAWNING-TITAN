from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.core import reward_functions
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


@dataclass()
class RewardsConfig(ConfigABC):
    """Class that validates and stores Rewards Configuration."""

    _rewards_for_loss: int
    _rewards_for_reaching_max_steps: int
    _end_rewards_are_multiplied_by_end_state: bool
    _reduce_negative_rewards_for_closer_fails: bool
    _reward_function: str

    # region Getters
    @property
    def rewards_for_loss(self) -> int:
        """Rewards for the blue agent losing."""
        return self._rewards_for_loss

    @property
    def rewards_for_reaching_max_steps(self) -> int:
        """
        Rewards for reaching max steps.

        Rewards for the blue agent winning by reaching the maximum number of
        steps.
        """
        return self._rewards_for_reaching_max_steps

    @property
    def end_rewards_are_multiplied_by_end_state(self) -> bool:
        """
        End rewards are multiplied by end state.

        How good the end state is (what % blue controls) is multiplied by
        the rewards that blue receives for winning.
        """
        return self._end_rewards_are_multiplied_by_end_state

    @property
    def reduce_negative_rewards_for_closer_fails(self) -> bool:
        """
        Reduce negative rewards for closer fails.

        The negative rewards from the red agent winning are reduced the
        closer to the end the blue agent gets.
        """
        return self._reduce_negative_rewards_for_closer_fails

    @property
    def reward_function(self) -> str:
        """
        Reward function.

        There are several built in example reward methods that you can
        choose from (shown below). You can also create your own reward
        method by copying one of the built in methods and calling it here
        built in reward methods: standard_rewards, one_per_timestep,
        safe_nodes_give_rewards, punish_bad_actions.
        """
        return self._reward_function

    # endregion

    # region Setters
    @rewards_for_loss.setter
    def rewards_for_loss(self, value):
        self._rewards_for_loss = value

    @rewards_for_reaching_max_steps.setter
    def rewards_for_reaching_max_steps(self, value):
        self._rewards_for_reaching_max_steps = value

    @end_rewards_are_multiplied_by_end_state.setter
    def end_rewards_are_multiplied_by_end_state(self, value):
        self._end_rewards_are_multiplied_by_end_state = value

    @reduce_negative_rewards_for_closer_fails.setter
    def reduce_negative_rewards_for_closer_fails(self, value):
        self._reduce_negative_rewards_for_closer_fails = value

    @reward_function.setter
    def reward_function(self, value):
        self._reward_function = value

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> RewardsConfig:
        """
        Creates an instance of `RewardsConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        cls.validate(config_dict)

        rewards = RewardsConfig(
            _rewards_for_loss=config_dict["rewards_for_loss"],
            _rewards_for_reaching_max_steps=config_dict[
                "rewards_for_reaching_max_steps"
            ],
            _end_rewards_are_multiplied_by_end_state=config_dict[
                "end_rewards_are_multiplied_by_end_state"
            ],
            _reduce_negative_rewards_for_closer_fails=config_dict[
                "reduce_negative_rewards_for_closer_fails"
            ],
            _reward_function=config_dict["reward_function"],
        )

        return rewards

    @classmethod
    def validate(cls, config_dict: dict):
        """
        Validates the rewards config dict.

        :param: config_dict: A config dict with the required key/values pairs.
        """
        # validate types
        check_type(config_dict, "rewards_for_loss", [int, float])
        check_type(config_dict, "rewards_for_reaching_max_steps", [int, float])
        check_type(config_dict, "end_rewards_are_multiplied_by_end_state", [bool])
        check_type(config_dict, "reduce_negative_rewards_for_closer_fails", [bool])

        # make sure the reward type exists
        if not hasattr(reward_functions, config_dict["reward_function"]):
            raise ValueError(
                "The reward function '"
                + config_dict["reward_function"]
                + "' does not exist inside: yawning_titan.envs.helpers.reward_functions"
            )
