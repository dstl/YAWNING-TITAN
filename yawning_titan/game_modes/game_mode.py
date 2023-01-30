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
from yawning_titan.db.doc_metadata import DocMetadata, DocMetaDataObject

# --- Tier 0 groups


class GameMode(ConfigGroup, DocMetaDataObject):
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
        _doc_metadata: Optional[DocMetadata] = None,
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
        self._doc_metadata = _doc_metadata if _doc_metadata else DocMetadata()
        super().__init__(doc)

    def to_dict(
        self,
        json_serializable: bool = False,
        include_none: bool = True,
        values_only: bool = False,
    ) -> dict:
        """
        Serialize the :class:`~yawning_titan.networks.network.Network` as a :class:`dict`.

        :param json_serializable: If ``True``, the :attr:`~yawning_titan.networks.network.Network`
            "d numpy array is converted to a list."
        :param include_none: Determines whether to include empty fields in the dict. Has a default
            value of ``True``.
        :return: The :class:`~yawning_titan.networks.network.Network` as a :class:`dict`.
        """
        config_dict = super().to_dict(
            values_only=values_only, include_none=include_none
        )
        if json_serializable and self.doc_metadata is not None:
            config_dict["_doc_metadata"] = self.doc_metadata.to_dict(include_none=True)

        return config_dict
