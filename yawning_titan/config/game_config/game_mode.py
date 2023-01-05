from __future__ import annotations

from typing import Optional

from yawning_titan.config.agents.new_blue_agent_config import Blue
from yawning_titan.config.agents.new_red_agent_config import Red
from yawning_titan.config.environment.new_game_rules_config import GameRules
from yawning_titan.config.environment.new_observation_space_config import (
    ObservationSpace,
)
from yawning_titan.config.environment.new_reset_config import Reset
from yawning_titan.config.environment.new_rewards_config import Rewards
from yawning_titan.config.game_config.new_miscellaneous_config import Miscellaneous
from yawning_titan.config.toolbox.core import ConfigGroup

# --- Tier 0 groups


class GameMode(ConfigGroup):
    """All options to configure and represent a complete game mode."""

    def __init__(
        self,
        doc: Optional[str] = None,
        red: Red = Red(doc="The configuration of the red agent"),
        blue: Blue = Blue(doc="The configuration of the blue agent"),
        game_rules: GameRules = GameRules(doc="The rules of the overall game mode"),
        blue_can_observe: ObservationSpace = ObservationSpace(
            doc="The characteristics of the network and the red agent that the blue agent can observe"
        ),
        on_reset: Reset = Reset(doc="The changes to the network made upon reset"),
        rewards: Rewards = Rewards(
            doc="The rewards the blue agent gets for different game states"
        ),
        miscellaneous: Miscellaneous = Miscellaneous(doc="Additional options"),
    ):
        self.red: Red = red
        self.blue: Blue = blue
        self.game_rules: GameRules = game_rules
        self.blue_can_observe: ObservationSpace = blue_can_observe
        self.on_reset: Reset = on_reset
        self.rewards: Rewards = rewards
        self.miscellaneous: Miscellaneous = miscellaneous
        super().__init__(doc)
