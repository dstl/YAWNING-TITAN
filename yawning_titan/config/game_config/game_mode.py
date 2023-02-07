from __future__ import annotations

from typing import Optional

from yawning_titan.config.agents.blue_agent_config import Blue
from yawning_titan.config.agents.red_agent_config import Red
from yawning_titan.config.environment.game_rules_config import GameRules
from yawning_titan.config.environment.observation_space_config import ObservationSpace
from yawning_titan.config.environment.reset_config import Reset
from yawning_titan.config.environment.rewards_config import Rewards
from yawning_titan.config.game_config.miscellaneous_config import Miscellaneous
from yawning_titan.config.toolbox.core import ConfigGroup

# --- Tier 0 groups


class GameMode(ConfigGroup):
    """All options to configure and represent a complete game mode."""

    def __init__(
        self,
        doc: Optional[str] = None,
        red: Red = None,
        blue: Blue = None,
        game_rules: GameRules = None,
        blue_can_observe: ObservationSpace = None,
        on_reset: Reset = None,
        rewards: Rewards = None,
        miscellaneous: Miscellaneous = None,
    ):
        self.red: Red = red if red else Red(doc="The configuration of the red agent")
        self.blue: Blue = (
            blue if blue else Blue(doc="The configuration of the blue agent")
        )
        self.game_rules: GameRules = (
            game_rules
            if game_rules
            else GameRules(doc="The rules of the overall game mode")
        )
        self.blue_can_observe: ObservationSpace = (
            blue_can_observe
            if blue_can_observe
            else ObservationSpace(
                doc="The characteristics of the network and the red agent that the blue agent can observe"
            )
        )
        self.on_reset: Reset = (
            on_reset
            if on_reset
            else Reset(doc="The changes to the network made upon reset")
        )
        self.rewards: Rewards = (
            rewards
            if rewards
            else Rewards(
                doc="The rewards the blue agent gets for different game states"
            )
        )
        self.miscellaneous: Miscellaneous = (
            miscellaneous if miscellaneous else Miscellaneous(doc="Additional options")
        )
        super().__init__(doc)

    @classmethod
    def create_from_yaml(
        cls,
        yaml: Optional[str] = None,
        legacy: Optional[bool] = False,
        infer_legacy: Optional[bool] = True,
    ) -> GameMode:
        """
        Generate a formatted instance of :class: `GameMode` from stored data.

        :param yaml: A yaml dictionary in the format generated by the `to_yaml` method.
        :param legacy: Whether the dictionary will be in legacy format.
        :param infer_legacy: Whether to try to set the legacy parameter based upon the keys in the dictionary.

        :return: An instance of :class: `GameMode`.
        """
        game_mode = GameMode()
        game_mode.set_from_yaml(yaml, legacy=legacy, infer_legacy=infer_legacy)
        return game_mode

    @classmethod
    def create(
        cls,
        dict: Optional[dict] = None,
        legacy: Optional[bool] = False,
        infer_legacy: Optional[bool] = True,
        raise_errors: bool = False,
    ) -> GameMode:
        """
        Generate a formatted instance of :class: `GameMode` from stored data.

        :param dict: A nested dictionary in the format generated by the `to_dict` method.
        :param legacy: Whether the dictionary will be in legacy format.
        :param infer_legacy: Whether to try to set the legacy parameter based upon the keys in the dictionary.

        :return: An instance of :class: `GameMode`.
        """
        game_mode = GameMode()
        game_mode.set_from_dict(dict, legacy=legacy, infer_legacy=infer_legacy)
        if (
            raise_errors
            and not game_mode.validation.passed
            and game_mode.validation.log()
        ):
            raise ValueError(game_mode.validation.log())
        return game_mode
