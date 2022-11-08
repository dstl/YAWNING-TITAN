from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


@dataclass()
class ResetConfig(ConfigGroupABC):
    """
    Class that validates and stores the Reset Configuration
    """

    reset_random_vulns: bool = field(metadata="Is true if the vulnerabilities are re-randomised on reset")
    """Is true if the vulnerabilities are re-randomised on reset"""

    reset_move_hvt: bool = field(metadata="Is true if new high value nodes are chosen on reset")
    """Is true if new high value nodes are chosen on reset"""

    reset_move_entry_nodes: bool = field(metadata="Is true if new entry nodes are chosen on reset")
    """Is true if new entry nodes are chosen on reset"""

    @classmethod
    def create(
            cls,
            settings: Dict[str, Any]
    ) -> ResetConfig:
        cls._validate(settings)

        reset_config = ResetConfig(
            reset_random_vulns=settings[
                "randomise_vulnerabilities_on_reset"
            ],
            reset_move_hvt=settings[
                "choose_new_high_value_targets_on_reset"
            ],
            reset_move_entry_nodes=settings[
                "choose_new_entry_nodes_on_reset"
            ]
        )

        return reset_config

    @classmethod
    def _validate(cls, data: dict):
        for name in [
            "randomise_vulnerabilities_on_reset",
            "choose_new_high_value_targets_on_reset",
            "choose_new_entry_nodes_on_reset",
        ]:
            check_type(data, name, [bool])
