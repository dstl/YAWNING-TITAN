from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_type


<<<<<<< HEAD
@dataclass
=======
@dataclass()
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
class ResetConfig(ConfigGroupABC):
    """
    Class that validates and stores the Reset Configuration
    """

    reset_random_vulns: bool
    """Is true if the vulnerabilities are re-randomised on reset"""

    reset_move_hvt: bool
    """Is true if new high value nodes are chosen on reset"""

    reset_move_entry_nodes: bool
    """Is true if new entry nodes are chosen on reset"""

    @classmethod
<<<<<<< HEAD
    def create(cls,settings: Dict[str, Any]) -> ResetConfig:
=======
    def create(
            cls,
            settings: Dict[str, Any]
    ) -> ResetConfig:
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
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
<<<<<<< HEAD
            check_type(data, name, [bool])
=======
            check_type(data, name, [bool])
>>>>>>> methods-YT/feature/AIDT-67-define-config-class-structure
