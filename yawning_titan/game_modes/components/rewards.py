from __future__ import annotations

from typing import Optional

from yawning_titan.config.core import ConfigGroup
from yawning_titan.config.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.item_types.int_item import IntItem, IntProperties
from yawning_titan.config.item_types.str_item import StrItem, StrProperties
from yawning_titan.db.schemas import GameModeConfigurationSchema

# --- Tier 0 groups


class Rewards(ConfigGroup):
    """The rewards the blue agent receives based upon the final game state."""

    def __init__(
        self,
        for_loss: Optional[int] = 0,
        for_reaching_max_steps: Optional[int] = 0,
        end_rewards_are_multiplied_by_end_state: Optional[bool] = False,
        reduce_negative_rewards_for_closer_fails: Optional[bool] = False,
        function: Optional[str] = "standard_rewards",
    ):
        from yawning_titan.envs.generic.core import reward_functions

        doc = "The rewards the blue agent gets for different game states"

        self.for_loss = IntItem(
            value=for_loss,
            doc="Rewards for the blue agent losing",
            query=GameModeConfigurationSchema.REWARD.FOR_LOSS,
            properties=IntProperties(allow_null=True, default=0),
            alias="rewards_for_loss",
        )
        self.for_reaching_max_steps = IntItem(
            value=for_reaching_max_steps,
            doc="Rewards for the blue agent winning by reaching the maximum number of steps",
            query=GameModeConfigurationSchema.REWARD.FOR_REACHING_MAX_STEPS,
            properties=IntProperties(allow_null=True, default=0),
            alias="rewards_for_reaching_max_steps",
        )
        self.end_rewards_are_multiplied_by_end_state = BoolItem(
            value=end_rewards_are_multiplied_by_end_state,
            doc="How good the end state is (what % blue controls) is multiplied by the rewards that blue receives for winning",
            query=GameModeConfigurationSchema.REWARD.END_REWARDS_ARE_MULTIPLIED_BY_END_STATE,
            properties=BoolProperties(allow_null=False, default=False),
            alias="end_rewards_are_multiplied_by_end_state",
        )
        self.reduce_negative_rewards_for_closer_fails = BoolItem(
            value=reduce_negative_rewards_for_closer_fails,
            doc="The negative rewards from the red agent winning are reduced the closer to the end the blue agent gets",
            query=GameModeConfigurationSchema.REWARD.REDUCE_NEGATIVE_REWARDS_FOR_CLOSER_FAILS,
            properties=BoolProperties(allow_null=False, default=False),
            alias="reduce_negative_rewards_for_closer_fails",
        )
        self.function: StrItem = StrItem(
            value=function,
            doc=(
                "There are several built in example reward methods that you can choose from (shown below) "
                "You can also create your own reward method by copying one of the built in methods and calling it here "
                "built in reward methods: standard_rewards, one_per_timestep, safe_nodes_give_rewards, punish_bad_actions"
            ),
            query=GameModeConfigurationSchema.REWARD.FUNCTION,
            properties=StrProperties(
                default="standard_rewards",
                options=list(reward_functions.__dict__.keys()),
            ),
            alias="reward_function",
        )
        super().__init__(doc)
