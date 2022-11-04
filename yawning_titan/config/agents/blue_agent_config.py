from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_group_class import ConfigGroupABC
from yawning_titan.envs.generic.helpers.environment_input_validation import check_within_range, check_type


@dataclass()
class BlueAgentConfig(ConfigGroupABC):
    """
    Class that validates and stores the Blue Agent Configuration
    """

    blue_max_deceptive_nodes: int
    """Integer value specifying how many deceptive nodes the blue agent can place in the network"""

    blue_immediate_detection_chance: float
    """Chance for the blue agent to immediately discover the node compromised by the red agent"""

    blue_scan_detection_chance: float
    """Chance for the blue agent to discover a compromised node on scan"""

    blue_deception_immediate_detection_chance: float
    """Chance for the blue agent to immediately discover that a deceptive node has been compromised"""

    blue_deception_scan_detection_chance: float
    """Chance for the blue agent to discover that a deceptive node has been compromised on scan"""

    blue_discover_failed_attacks: bool
    """Is true if blue agent can discover failed attacks"""

    blue_discover_attack_source_if_detected: bool
    """Is true if the blue agent can learn information about an attack that succeeds if the compromise is known"""

    blue_discover_attack_source_if_not_detected: bool
    """Is true if the blue agent can learn information about an attack that succeeds if the compromise is not known"""

    blue_chance_to_discover_source_failed: float
    """Chance for blue to discover information about a failed attack"""

    blue_chance_to_discover_source_succeed_known: float
    """Chance for blue to discover information about an attack that succeeded and the compromise was known"""

    blue_chance_to_discover_source_succeed_unknown: float
    """Chance for blue to discover information about an attack that succeeded and the compromise was not known"""

    blue_chance_to_discover_source_deceptive_failed: float
    """Chance to discover the location of a failed attack on a deceptive node"""

    blue_chance_to_discover_source_deceptive_succeed: float
    """Chance to discover the location of a succeeded attack against a deceptive node"""

    blue_make_node_safe_modifies_vuln: bool
    """Is true if blue agent can fix a node to decrease its vulnerability"""

    blue_vuln_change_amount_make_safe: float
    """The amount the vulnerability score will change when blue agent fixes a node"""

    blue_make_safe_random_vuln: bool
    """Is true if the vulnerability score is randomised when blue agent fixes a node"""

    blue_reduce_vuln_action: bool
    """Is true if blue agent will try to reduce a node's vulnerability score"""

    blue_restore_node_action: bool
    """Is true if the blue agent will try to reset the node state to what it was at the beginning of the game"""

    blue_make_node_safe_action: bool
    """Is true if the blue agent will try to fix a node without resetting the node to what it was at the beginning
    of the game"""

    blue_scan_action: bool
    """Is true if blue can scan all nodes in the network to detect red agent intrusions"""

    blue_isolate_action: bool
    """Is true if blue agent can isolate a node i.e. remove connections to and from a node"""

    blue_reconnect_action: bool
    """Is true if blue agent can reinstate node connections after the node is isolated"""

    blue_do_nothing_action: bool
    """Is true if the blue agent can decide to do nothing"""

    blue_deceptive_action: bool
    """Is true if the blue agent can use deceptive nodes"""

    blue_deceptive_node_make_new: bool
    """Is true if the blue agent can reuse a deceptive node if it has run out of deceptive nodes it can place"""

    @classmethod
    def create(
            cls,
            settings: Dict[str, Any],
    ):
        # validate blue agent config values
        cls._validate(settings)

        blue_agent = BlueAgentConfig(
            blue_max_deceptive_nodes=settings["max_number_deceptive_nodes"],
            blue_immediate_detection_chance=settings[
                "chance_to_immediately_discover_intrusion"
            ],
            blue_scan_detection_chance=settings[
                "chance_to_discover_intrusion_on_scan"
            ],
            blue_deception_immediate_detection_chance=settings[
                "chance_to_immediately_discover_intrusion_deceptive_node"
            ],
            blue_deception_scan_detection_chance=settings[
                "chance_to_discover_intrusion_on_scan_deceptive_node"
            ],
            blue_discover_failed_attacks=settings[
                "can_discover_failed_attacks"
            ],
            blue_discover_attack_source_if_detected=settings[
                "can_discover_succeeded_attacks_if_compromise_is_discovered"
            ],
            blue_discover_attack_source_if_not_detected=settings[
                "can_discover_succeeded_attacks_if_compromise_is_not_discovered"
            ],
            blue_chance_to_discover_source_failed=settings[
                "chance_to_discover_failed_attack"
            ],
            blue_chance_to_discover_source_succeed_known=settings[
                "chance_to_discover_succeeded_attack_compromise_known"
            ],
            blue_chance_to_discover_source_succeed_unknown=settings[
                "chance_to_discover_succeeded_attack_compromise_not_known"
            ],
            blue_chance_to_discover_source_deceptive_failed=settings[
                "chance_to_discover_failed_attack_deceptive_node"
            ],
            blue_chance_to_discover_source_deceptive_succeed=settings[
                "chance_to_discover_succeeded_attack_deceptive_node"
            ],
            blue_make_node_safe_modifies_vuln=settings[
                "making_node_safe_modifies_vulnerability"
            ],
            blue_vuln_change_amount_make_safe=settings[
                "vulnerability_change_during_node_patch"
            ],
            blue_make_safe_random_vuln=settings[
                "making_node_safe_gives_random_vulnerability"
            ],
            blue_reduce_vuln_action=settings[
                "blue_uses_reduce_vulnerability"
            ],
            blue_restore_node_action=settings["blue_uses_restore_node"],
            blue_make_node_safe_action=settings["blue_uses_make_node_safe"],
            blue_scan_action=settings["blue_uses_scan"],
            blue_isolate_action=settings["blue_uses_isolate_node"],
            blue_reconnect_action=settings["blue_uses_reconnect_node"],
            blue_do_nothing_action=settings["blue_uses_do_nothing"],
            blue_deceptive_action=settings["blue_uses_deceptive_nodes"],
            blue_deceptive_node_make_new=settings[
                "relocating_deceptive_nodes_generates_a_new_node"
            ]
        )

        return blue_agent

    @classmethod
    def _validate(cls, data: dict):
        # data is int or float
        for name in [
            "chance_to_immediately_discover_intrusion",
            "chance_to_discover_intrusion_on_scan",
            "vulnerability_change_during_node_patch",
            "chance_to_discover_failed_attack",
            "chance_to_discover_succeeded_attack_compromise_known",
            "chance_to_discover_succeeded_attack_compromise_not_known",
            "chance_to_immediately_discover_intrusion_deceptive_node",
            "chance_to_discover_intrusion_on_scan_deceptive_node",
            "chance_to_discover_failed_attack_deceptive_node",
            "chance_to_discover_succeeded_attack_deceptive_node",
            "vulnerability_change_during_node_patch",
        ]:
            check_type(data, name, [int, float])
        # data is int
        for name in ["max_number_deceptive_nodes"]:
            check_type(data, name, [int])

        # data is bool
        for name in [
            "making_node_safe_modifies_vulnerability",
            "making_node_safe_gives_random_vulnerability",
            "blue_uses_reduce_vulnerability",
            "blue_uses_restore_node",
            "blue_uses_make_node_safe",
            "blue_uses_scan",
            "blue_uses_isolate_node",
            "blue_uses_reconnect_node",
            "blue_uses_do_nothing",
            "blue_uses_deceptive_nodes",
            "can_discover_failed_attacks",
            "can_discover_succeeded_attacks_if_compromise_is_discovered",
            "can_discover_succeeded_attacks_if_compromise_is_not_discovered",
            "relocating_deceptive_nodes_generates_a_new_node",
        ]:
            check_type(data, name, [bool])

        # data is between 0 and 1 inclusive
        for name in [
            "chance_to_immediately_discover_intrusion",
            "chance_to_immediately_discover_intrusion_deceptive_node",
            "chance_to_discover_intrusion_on_scan_deceptive_node",
            "chance_to_discover_intrusion_on_scan",
            "chance_to_discover_failed_attack",
            "chance_to_discover_succeeded_attack_compromise_known",
            "chance_to_discover_succeeded_attack_compromise_not_known",
            "chance_to_discover_failed_attack_deceptive_node",
            "chance_to_discover_succeeded_attack_deceptive_node",
        ]:
            check_within_range(data, name, 0, 1, True, True)

        check_within_range(
            data, "vulnerability_change_during_node_patch", -1, 1, True, True
        )

        # misc
        if (
                not data["blue_uses_reduce_vulnerability"]
                and (not data["blue_uses_restore_node"])
                and (not data["blue_uses_make_node_safe"])
                and (not data["blue_uses_scan"])
                and (not data["blue_uses_isolate_node"])
                and (not data["blue_uses_reconnect_node"])
                and (not data["blue_uses_do_nothing"])
                and (not data["blue_uses_deceptive_nodes"])
        ):
            raise ValueError(
                "'blue_uses_****' -> Blue must have at least one action selected. If you want blue to do nothing set 'blue_uses_do_nothing' to True"
                # noqa
            )

        if (data["blue_uses_isolate_node"] and (not data["blue_uses_reconnect_node"])) or (
                (not data["blue_uses_isolate_node"]) and data["blue_uses_reconnect_node"]
        ):
            raise ValueError(
                "'blue_uses_isolate_node', 'blue_uses_reconnect_node' -> Blue should be able to reconnect or isolate nodes if the other is true"
                # noqa
            )

        check_within_range(data, "max_number_deceptive_nodes", 0, None, True, True)

        if data["blue_uses_deceptive_nodes"] and (0 == data["max_number_deceptive_nodes"]):
            raise ValueError(
                "'blue_uses_deceptive_nodes', 'max_number_deceptive_nodes' -> If blue can use deceptive nodes then max_number_deceptive_nodes."
                # noqa
            )

        if data["blue_uses_scan"]:
            if data["chance_to_immediately_discover_intrusion"] == 1:
                raise ValueError(
                    "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> The scan action is selected yet blue has 100% chance to spot detections. There is no need for the blue to have the scan action in this case"
                    # noqa
                )
        else:
            if data["chance_to_immediately_discover_intrusion"] != 1:
                raise ValueError(
                    "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> If the blue agent cannot scan nodes then it should be able to automtically detect the intrusions"
                    # noqa
                )

        if (
                data["chance_to_discover_intrusion_on_scan_deceptive_node"]
                <= data["chance_to_discover_intrusion_on_scan"]
        ):
            if data["chance_to_discover_intrusion_on_scan_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_intrusion_on_scan_deceptive_node', 'chance_to_discover_intrusion_on_scan' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                    # noqa
                )

        if (
                data["chance_to_discover_failed_attack_deceptive_node"]
                <= data["chance_to_discover_failed_attack"]
        ):
            if data["chance_to_discover_failed_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_failed_attack_deceptive_node', 'chance_to_discover_failed_attack' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                    # noqa
                )

        if (
                data["chance_to_discover_succeeded_attack_deceptive_node"]
                <= data["chance_to_discover_succeeded_attack_compromise_known"]
        ):
            if data["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_succeeded_attack_deceptive_node', 'chance_to_discover_succeeded_attack_compromise_known' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                    # noqa
                )

        if (
                data["chance_to_discover_succeeded_attack_deceptive_node"]
                <= data["chance_to_discover_succeeded_attack_compromise_not_known"]
        ):
            if data["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_succeeded_attack_deceptive_node', 'chance_to_discover_succeeded_attack_compromise_not_known' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                    # noqa
                )

        if (
                data["making_node_safe_gives_random_vulnerability"]
                and data["making_node_safe_modifies_vulnerability"]
        ):
            raise ValueError(
                "'making_node_safe_gives_random_vulnerability', 'making_node_safe_modifies_vulnerability' -> Does not make sense to give a node a random vulnerability and to increase its vulnerability when a node is made safe"
                # noqa
            )

        if (
                data["chance_to_immediately_discover_intrusion_deceptive_node"]
                <= data["chance_to_immediately_discover_intrusion"]
        ):
            if data["chance_to_immediately_discover_intrusion_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_immediately_discover_intrusion_deceptive_node', 'chance_to_immediately_discover_intrusion' -> The deceptive nodes should have a higher chance at detecting intrusions that the regular nodes"
                    # noqa
                )
