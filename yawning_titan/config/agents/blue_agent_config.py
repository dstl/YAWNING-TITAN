from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.envs.generic.helpers.environment_input_validation import (
    check_type,
    check_within_range,
)


@dataclass()
class BlueAgentConfig(ConfigABC):
    """
    Class that validates and stores the Blue Agent Configuration.

    Notes from the DSTL
    -------------------
    The blue agent does not have to have perfect detection. In these settings
    you can change how much information blue can gain from the red agents
    actions. There are two different pieces of information blue can get:
    intrusions and attacks.

    Intrusions
        An intrusion is when the red agent takes over a node and compromises
        it. You can change the chance that blue has to be able to detect
        this using the "chance_to_immediately_discover_intrusion". If blue
        does not detect an intrusion then it can use the scan action to try
        and discover these intrusions with
        are used as detectors to inform blue when they are compromised. They
        should have a chance to detect of 1 so that they can detect
        everything (at the very least they should have a chance to detect
        higher than the normal chance to detect) but you can modify it if
        you so wish  with
        "chance_to_immediately_discover_intrusion_deceptive_node" and
        "chance_to_discover_intrusion_on_scan_deceptive_node".

    Attacks
        Attacks are the actual attacks that the red agent does to compromise
        the nodes. For example you may be able to see that node 14 is
        compromised but using the attack detection, the blue agent may be
        able to see that it was node 12 that attacked node 14. You can
        modify the chance for blue to see attacks that failed, succeeded (
        and blue was able to detect that the node was compromised) and
        attacks that succeeded and the blue agent did not detect the intrusion.

    Again there are settings to change the likelihood that a deceptive node
    can detect an attack. While this should remain at 1, it is open for you
    to change.
    """

    _max_number_deceptive_nodes: int
    _can_discover_failed_attacks: bool
    _chance_to_immediately_discover_intrusion: float
    _chance_to_discover_intrusion_on_scan: float
    _chance_to_immediately_discover_intrusion_deceptive_node: float
    _chance_to_discover_intrusion_on_scan_deceptive_node: float
    _chance_to_discover_failed_attack: float
    _can_discover_succeeded_attacks_if_compromise_is_discovered: bool
    _can_discover_succeeded_attacks_if_compromise_is_not_discovered: bool
    _chance_to_discover_succeeded_attack_compromise_known: float
    _chance_to_discover_succeeded_attack_compromise_not_known: float
    _chance_to_discover_failed_attack_deceptive_node: float
    _chance_to_discover_succeeded_attack_deceptive_node: float
    _making_node_safe_modifies_vulnerability: bool
    _vulnerability_change_during_node_patch: float
    _making_node_safe_gives_random_vulnerability: bool
    _blue_uses_reduce_vulnerability: bool
    _blue_uses_restore_node: bool
    _blue_uses_make_node_safe: bool
    _blue_uses_scan: bool
    _blue_uses_isolate_node: bool
    _blue_uses_reconnect_node: bool
    _blue_uses_do_nothing: bool
    _blue_uses_deceptive_nodes: bool
    _relocating_deceptive_nodes_generates_a_new_node: bool

    # region Getters
    @property
    def max_number_deceptive_nodes(self) -> int:
        """The max number of deceptive nodes that blue can place."""
        return self._max_number_deceptive_nodes

    @property
    def can_discover_failed_attacks(self) -> bool:
        """Can discover the location an attack came from if the attack failed."""
        return self._can_discover_failed_attacks

    @property
    def chance_to_immediately_discover_intrusion(self) -> float:
        """Chance for blue to discover a node that red has compromised the instant red compromises the node."""
        return self._chance_to_immediately_discover_intrusion

    @property
    def chance_to_discover_intrusion_on_scan(self) -> float:
        """When blue performs the scan action this is the chance that a red intrusion is discovered."""
        return self._chance_to_discover_intrusion_on_scan

    @property
    def chance_to_immediately_discover_intrusion_deceptive_node(self) -> float:
        """Chance for blue to discover a deceptive node that red has compromised the instant it is compromised."""
        return self._chance_to_immediately_discover_intrusion_deceptive_node

    @property
    def chance_to_discover_intrusion_on_scan_deceptive_node(self) -> float:
        """When blue uses the scan action what is the chance that blue will detect an intrusion in a deceptive node."""
        return self._chance_to_discover_intrusion_on_scan_deceptive_node

    @property
    def chance_to_discover_failed_attack(self) -> float:
        """Chance for blue to discover information about a failed attack."""
        return self._chance_to_discover_failed_attack

    @property
    def can_discover_succeeded_attacks_if_compromise_is_discovered(self) -> bool:
        """Can blue learn information about an attack that succeeds if the compromise is known."""
        return self._can_discover_succeeded_attacks_if_compromise_is_discovered

    @property
    def can_discover_succeeded_attacks_if_compromise_is_not_discovered(self) -> bool:
        """Can blue learn information about an attack that succeeds if the compromise is NOT known."""
        return self._can_discover_succeeded_attacks_if_compromise_is_not_discovered

    @property
    def chance_to_discover_succeeded_attack_compromise_known(self) -> float:
        """Chance for blue to discover information about an attack that succeeded and the compromise was known."""
        return self._chance_to_discover_succeeded_attack_compromise_known

    @property
    def chance_to_discover_succeeded_attack_compromise_not_known(self) -> float:
        """Chance for blue to discover information about an attack that succeeded and the compromise was NOT known."""
        return self._chance_to_discover_succeeded_attack_compromise_not_known

    @property
    def chance_to_discover_failed_attack_deceptive_node(self) -> float:
        """Chance to discover the location of a failed attack on a deceptive node."""
        return self._chance_to_discover_failed_attack_deceptive_node

    @property
    def chance_to_discover_succeeded_attack_deceptive_node(self) -> float:
        """Chance to discover the location of a succeeded attack against a deceptive node."""
        return self._chance_to_discover_succeeded_attack_deceptive_node

    @property
    def making_node_safe_modifies_vulnerability(self) -> bool:
        """If blue fixes a node then the vulnerability score of that node increases."""
        return self._making_node_safe_modifies_vulnerability

    @property
    def vulnerability_change_during_node_patch(self) -> float:
        """The amount that the vulnerability of a node changes when it is made safe."""
        return self._vulnerability_change_during_node_patch

    @property
    def making_node_safe_gives_random_vulnerability(self) -> bool:
        """When fixing a node the vulnerability score is randomised."""
        return self._making_node_safe_gives_random_vulnerability

    @property
    def blue_uses_reduce_vulnerability(self) -> bool:
        """Blue picks a node and reduces the vulnerability score."""
        return self._blue_uses_reduce_vulnerability

    @property
    def blue_uses_restore_node(self) -> bool:
        """Blue picks a node and restores everything about the node to its starting state."""
        return self._blue_uses_restore_node

    @property
    def blue_uses_make_node_safe(self) -> bool:
        """Blue fixes a node but does not restore it to its initial state."""
        return self._blue_uses_make_node_safe

    @property
    def blue_uses_scan(self) -> bool:
        """Blue scans all the nodes to try and detect any red intrusions."""
        return self._blue_uses_scan

    @property
    def blue_uses_isolate_node(self) -> bool:
        """Blue disables all the connections to and from a node."""
        return self._blue_uses_isolate_node

    @property
    def blue_uses_reconnect_node(self) -> bool:
        """Blue re-connects all the connections to and from a node."""
        return self._blue_uses_reconnect_node

    @property
    def blue_uses_do_nothing(self) -> bool:
        """Blue agent does nothing."""
        return self._blue_uses_do_nothing

    @property
    def blue_uses_deceptive_nodes(self) -> bool:
        """
        Blue agent can place down deceptive nodes.

        These nodes act as just another node in the network but have a
        different chance of spotting attacks and always show when they
        are compromised.
        """
        return self._blue_uses_deceptive_nodes

    @property
    def relocating_deceptive_nodes_generates_a_new_node(self):
        """
        Relocating deceptive nodes generates a new node.

        When the blue agent places a deceptive node and it has none left in
        stock it will "pick up" the first deceptive node that it used and
        "relocate it" When relocating a node will the stats for the node (
        such as the vulnerability and compromised status) be re-generated as
        if adding a new node or will they carry over from the "old" node.
        """
        return self._relocating_deceptive_nodes_generates_a_new_node

    # endregion

    # region Setters
    @max_number_deceptive_nodes.setter
    def max_number_deceptive_nodes(self, value):
        self._max_number_deceptive_nodes = value

    @can_discover_failed_attacks.setter
    def can_discover_failed_attacks(self, value):
        self._can_discover_failed_attacks = value

    @chance_to_immediately_discover_intrusion.setter
    def chance_to_immediately_discover_intrusion(self, value):
        self._chance_to_immediately_discover_intrusion = value

    @chance_to_discover_intrusion_on_scan.setter
    def chance_to_discover_intrusion_on_scan(self, value):
        self._chance_to_discover_intrusion_on_scan = value

    @chance_to_immediately_discover_intrusion_deceptive_node.setter
    def chance_to_immediately_discover_intrusion_deceptive_node(self, value):
        self._chance_to_immediately_discover_intrusion_deceptive_node = value

    @chance_to_discover_intrusion_on_scan_deceptive_node.setter
    def chance_to_discover_intrusion_on_scan_deceptive_node(self, value):
        self._chance_to_discover_intrusion_on_scan_deceptive_node = value

    @chance_to_discover_failed_attack.setter
    def chance_to_discover_failed_attack(self, value):
        self._chance_to_discover_failed_attack = value

    @can_discover_succeeded_attacks_if_compromise_is_discovered.setter
    def can_discover_succeeded_attacks_if_compromise_is_discovered(self, value):
        self._can_discover_succeeded_attacks_if_compromise_is_discovered = value

    @can_discover_succeeded_attacks_if_compromise_is_not_discovered.setter
    def can_discover_succeeded_attacks_if_compromise_is_not_discovered(self, value):
        self._can_discover_succeeded_attacks_if_compromise_is_not_discovered = value

    @chance_to_discover_succeeded_attack_compromise_known.setter
    def chance_to_discover_succeeded_attack_compromise_known(self, value):
        self._chance_to_discover_succeeded_attack_compromise_known = value

    @chance_to_discover_succeeded_attack_compromise_not_known.setter
    def chance_to_discover_succeeded_attack_compromise_not_known(self, value):
        self._chance_to_discover_succeeded_attack_compromise_not_known = value

    @chance_to_discover_failed_attack_deceptive_node.setter
    def chance_to_discover_failed_attack_deceptive_node(self, value):
        self._chance_to_discover_failed_attack_deceptive_node = value

    @chance_to_discover_succeeded_attack_deceptive_node.setter
    def chance_to_discover_succeeded_attack_deceptive_node(self, value):
        self._chance_to_discover_succeeded_attack_deceptive_node = value

    @making_node_safe_modifies_vulnerability.setter
    def making_node_safe_modifies_vulnerability(self, value):
        self._making_node_safe_modifies_vulnerability = value

    @vulnerability_change_during_node_patch.setter
    def vulnerability_change_during_node_patch(self, value):
        self._vulnerability_change_during_node_patch = value

    @making_node_safe_gives_random_vulnerability.setter
    def making_node_safe_gives_random_vulnerability(self, value):
        self._making_node_safe_gives_random_vulnerability = value

    @blue_uses_reduce_vulnerability.setter
    def blue_uses_reduce_vulnerability(self, value):
        self._blue_uses_reduce_vulnerability = value

    @blue_uses_restore_node.setter
    def blue_uses_restore_node(self, value):
        self._blue_uses_restore_node = value

    @blue_uses_make_node_safe.setter
    def blue_uses_make_node_safe(self, value):
        self._blue_uses_make_node_safe = value

    @blue_uses_scan.setter
    def blue_uses_scan(self, value):
        self._blue_uses_scan = value

    @blue_uses_isolate_node.setter
    def blue_uses_isolate_node(self, value):
        self._blue_uses_isolate_node = value

    @blue_uses_reconnect_node.setter
    def blue_uses_reconnect_node(self, value):
        self._blue_uses_reconnect_node = value

    @blue_uses_do_nothing.setter
    def blue_uses_do_nothing(self, value):
        self._blue_uses_do_nothing = value

    @blue_uses_deceptive_nodes.setter
    def blue_uses_deceptive_nodes(self, value):
        self._blue_uses_deceptive_nodes = value

    @relocating_deceptive_nodes_generates_a_new_node.setter
    def relocating_deceptive_nodes_generates_a_new_node(self, value):
        self._relocating_deceptive_nodes_generates_a_new_node = value

    # endregion

    @classmethod
    def create(cls, config_dict: Dict[str, Any]) -> BlueAgentConfig:
        """
        Creates an instance of `BlueAgentConfig` after calling `.validate`.

        Args:
            config_dict: A config dict with the required key/values pairs.
        """
        cls.validate(config_dict)
        blue_agent_config = BlueAgentConfig(
            _max_number_deceptive_nodes=config_dict["max_number_deceptive_nodes"],
            _can_discover_failed_attacks=config_dict["can_discover_failed_attacks"],
            _chance_to_immediately_discover_intrusion=config_dict[
                "chance_to_immediately_discover_intrusion"
            ],
            _chance_to_discover_intrusion_on_scan=config_dict[
                "chance_to_discover_intrusion_on_scan"
            ],
            _chance_to_immediately_discover_intrusion_deceptive_node=config_dict[
                "chance_to_immediately_discover_intrusion_deceptive_node"
            ],
            _chance_to_discover_intrusion_on_scan_deceptive_node=config_dict[
                "chance_to_discover_intrusion_on_scan_deceptive_node"
            ],
            _chance_to_discover_failed_attack=config_dict[
                "chance_to_discover_failed_attack"
            ],
            _can_discover_succeeded_attacks_if_compromise_is_discovered=config_dict[
                "can_discover_succeeded_attacks_if_compromise_is_discovered"
            ],
            _can_discover_succeeded_attacks_if_compromise_is_not_discovered=config_dict[
                "can_discover_succeeded_attacks_if_compromise_is_not_discovered"
            ],
            _chance_to_discover_succeeded_attack_compromise_known=config_dict[
                "chance_to_discover_succeeded_attack_compromise_known"
            ],
            _chance_to_discover_succeeded_attack_compromise_not_known=config_dict[
                "chance_to_discover_succeeded_attack_compromise_not_known"
            ],
            _chance_to_discover_failed_attack_deceptive_node=config_dict[
                "chance_to_discover_failed_attack_deceptive_node"
            ],
            _chance_to_discover_succeeded_attack_deceptive_node=config_dict[
                "chance_to_discover_succeeded_attack_deceptive_node"
            ],
            _making_node_safe_modifies_vulnerability=config_dict[
                "making_node_safe_modifies_vulnerability"
            ],
            _vulnerability_change_during_node_patch=config_dict[
                "vulnerability_change_during_node_patch"
            ],
            _making_node_safe_gives_random_vulnerability=config_dict[
                "making_node_safe_gives_random_vulnerability"
            ],
            _blue_uses_reduce_vulnerability=config_dict[
                "blue_uses_reduce_vulnerability"
            ],
            _blue_uses_restore_node=config_dict["blue_uses_restore_node"],
            _blue_uses_make_node_safe=config_dict["blue_uses_make_node_safe"],
            _blue_uses_scan=config_dict["blue_uses_scan"],
            _blue_uses_isolate_node=config_dict["blue_uses_isolate_node"],
            _blue_uses_reconnect_node=config_dict["blue_uses_reconnect_node"],
            _blue_uses_do_nothing=config_dict["blue_uses_do_nothing"],
            _blue_uses_deceptive_nodes=config_dict["blue_uses_deceptive_nodes"],
            _relocating_deceptive_nodes_generates_a_new_node=config_dict[
                "relocating_deceptive_nodes_generates_a_new_node"
            ],
        )
        return blue_agent_config

    @classmethod
    def validate(cls, config_dict: dict):
        """
        Validates the blue agent config dict.

        :param: config_dict: A config dict with the required key/values pairs.
        """
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
            check_type(config_dict, name, [int, float])
        # data is int
        for name in ["max_number_deceptive_nodes"]:
            check_type(config_dict, name, [int])

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
            check_type(config_dict, name, [bool])

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
            check_within_range(config_dict, name, 0, 1, True, True)

        check_within_range(
            config_dict, "vulnerability_change_during_node_patch", -1, 1, True, True
        )

        # misc
        if (
            not config_dict["blue_uses_reduce_vulnerability"]
            and (not config_dict["blue_uses_restore_node"])
            and (not config_dict["blue_uses_make_node_safe"])
            and (not config_dict["blue_uses_scan"])
            and (not config_dict["blue_uses_isolate_node"])
            and (not config_dict["blue_uses_reconnect_node"])
            and (not config_dict["blue_uses_do_nothing"])
            and (not config_dict["blue_uses_deceptive_nodes"])
        ):
            raise ValueError(
                "'blue_uses_****' -> Blue must have at least one action selected. If "
                "you want blue to do nothing set 'blue_uses_do_nothing' to True."
                # noqa
            )

        if (
            config_dict["blue_uses_isolate_node"]
            and (not config_dict["blue_uses_reconnect_node"])
        ) or (
            (not config_dict["blue_uses_isolate_node"])
            and config_dict["blue_uses_reconnect_node"]
        ):
            raise ValueError(
                "'blue_uses_isolate_node', 'blue_uses_reconnect_node' -> Blue should "
                "be able to reconnect or isolate nodes if the other is true."
                # noqa
            )

        check_within_range(
            config_dict, "max_number_deceptive_nodes", 0, None, True, True
        )

        if config_dict["blue_uses_deceptive_nodes"] and (
            0 == config_dict["max_number_deceptive_nodes"]
        ):
            raise ValueError(
                "'blue_uses_deceptive_nodes', 'max_number_deceptive_nodes' -> If blue "
                "can use deceptive nodes then max_number_deceptive_nodes."
                # noqa
            )

        if config_dict["blue_uses_scan"]:
            if config_dict["chance_to_immediately_discover_intrusion"] == 1:
                raise ValueError(
                    "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> "
                    "The scan action is selected yet blue has 100% chance to spot "
                    "detections. There is no need for the blue to have the scan "
                    "action in this case "
                    # noqa
                )
        else:
            if config_dict["chance_to_immediately_discover_intrusion"] != 1:
                raise ValueError(
                    "'blue_uses_scan', 'chance_to_immediately_discover_intrusion' -> "
                    "If the blue agent cannot scan nodes then it should be able to "
                    "automtically detect the intrusions "
                    # noqa
                )

        if (
            config_dict["chance_to_discover_intrusion_on_scan_deceptive_node"]
            <= config_dict["chance_to_discover_intrusion_on_scan"]
        ):
            if config_dict["chance_to_discover_intrusion_on_scan_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_intrusion_on_scan_deceptive_node', "
                    "'chance_to_discover_intrusion_on_scan' -> The deceptive nodes "
                    "should have a higher chance at detecting intrusions that the "
                    "regular nodes "
                    # noqa
                )

        if (
            config_dict["chance_to_discover_failed_attack_deceptive_node"]
            <= config_dict["chance_to_discover_failed_attack"]
        ):
            if config_dict["chance_to_discover_failed_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_failed_attack_deceptive_node', "
                    "'chance_to_discover_failed_attack' -> The deceptive nodes should "
                    "have a higher chance at detecting intrusions that the regular "
                    "nodes "
                    # noqa
                )

        if (
            config_dict["chance_to_discover_succeeded_attack_deceptive_node"]
            <= config_dict["chance_to_discover_succeeded_attack_compromise_known"]
        ):
            if config_dict["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_succeeded_attack_deceptive_node', "
                    "'chance_to_discover_succeeded_attack_compromise_known' -> The "
                    "deceptive nodes should have a higher chance at detecting "
                    "intrusions that the regular nodes "
                    # noqa
                )

        if (
            config_dict["chance_to_discover_succeeded_attack_deceptive_node"]
            <= config_dict["chance_to_discover_succeeded_attack_compromise_not_known"]
        ):
            if config_dict["chance_to_discover_succeeded_attack_deceptive_node"] != 1:
                raise ValueError(
                    "'chance_to_discover_succeeded_attack_deceptive_node', "
                    "'chance_to_discover_succeeded_attack_compromise_not_known' -> "
                    "The deceptive nodes should have a higher chance at detecting "
                    "intrusions that the regular nodes "
                    # noqa
                )

        if (
            config_dict["making_node_safe_gives_random_vulnerability"]
            and config_dict["making_node_safe_modifies_vulnerability"]
        ):
            raise ValueError(
                "'making_node_safe_gives_random_vulnerability', "
                "'making_node_safe_modifies_vulnerability' -> Does not make sense to "
                "give a node a random vulnerability and to increase its vulnerability "
                "when a node is made safe "
                # noqa
            )

        if (
            config_dict["chance_to_immediately_discover_intrusion_deceptive_node"]
            <= config_dict["chance_to_immediately_discover_intrusion"]
        ):
            if (
                config_dict["chance_to_immediately_discover_intrusion_deceptive_node"]
                != 1
            ):
                raise ValueError(
                    "'chance_to_immediately_discover_intrusion_deceptive_node', "
                    "'chance_to_immediately_discover_intrusion' -> The deceptive "
                    "nodes should have a higher chance at detecting intrusions that "
                    "the regular nodes "
                    # noqa
                )
