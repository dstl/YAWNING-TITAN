from __future__ import annotations


    # region Getters
    @property
    def red_skill(self) -> float:
        """
        Red Skill.

        The red agents skill level. Higher means that red is more likely to
        succeed in attacks.
        """
        return self._red_skill

    @property
    def red_uses_skill(self) -> bool:
        """Red uses its skill modifier when attacking nodes."""
        return self._red_uses_skill

    @property
    def red_ignores_defences(self) -> bool:
        """The red agent ignores the defences of nodes."""
        return self._red_ignores_defences

    @property
    def red_always_succeeds(self) -> bool:
        """Reds attacks always succeed."""
        return self._red_always_succeeds

    @property
    def red_can_only_attack_from_red_agent_node(self) -> bool:
        """
        Red can only attack from red agent node.

        The red agent will only ever be in one node however it can control any
        amount of nodes. Can the red agent only attack from its one main
        node or can it attack from any node that it controls.
        """
        return self._red_can_only_attack_from_red_agent_node

    @property
    def red_can_attack_from_any_red_node(self) -> bool:
        """
        Red can attack from any node.

        The red agent will only ever be in one node however it can control any
        amount of nodes. Can the red agent only attack from its one main
        node or can it attack from any node that it controls.
        """
        return self._red_can_attack_from_any_red_node

    @property
    def red_can_naturally_spread(self) -> bool:
        """The red agent naturally spreads its influence every time-step."""
        return self._red_can_naturally_spread

    @property
    def chance_to_spread_to_connected_node(self) -> float:
        """
        Chance to spread to connected node.

        If a node is connected to a compromised node what chance does it have
        to become compromised every turn through natural spreading.
        """
        return self._chance_to_spread_to_connected_node

    @property
    def chance_to_spread_to_unconnected_node(self) -> float:
        """
        Chance to spread to unconnected node.

        If a node is not connected to a compromised node what chance does it
        have to become randomly infected through natural spreading.
        """
        return self._chance_to_spread_to_unconnected_node

    @property
    def red_uses_spread_action(self) -> bool:
        """Tries to spread to every node connected to an infected node."""
        return self._red_uses_spread_action

    @property
    def spread_action_likelihood(self) -> float:
        """Weighting for red_uses_spread_action."""
        return self._spread_action_likelihood

    @property
    def chance_for_red_to_spread(self) -> float:
        """Chance for each 'spread' to succeed."""
        return self._chance_for_red_to_spread

    @property
    def red_uses_random_infect_action(self) -> bool:
        """Tries to infect every safe node in the environment."""
        return self._red_uses_random_infect_action

    @property
    def random_infect_action_likelihood(self) -> float:
        """Weighting for red_uses_random_infect_action."""
        return self._random_infect_action_likelihood

    @property
    def chance_for_red_to_random_compromise(self) -> float:
        """Chance for each 'infect' to succeed."""
        return self._chance_for_red_to_random_compromise

    @property
    def red_uses_basic_attack_action(self) -> bool:
        """
        Red uses basic attack action.

        The red agent picks a single node connected to an infected node and
        tries to attack and take over that node.
        """
        return self._red_uses_basic_attack_action

    @property
    def basic_attack_action_likelihood(self) -> float:
        """Weighting for red_uses_basic_attack_action."""
        return self._basic_attack_action_likelihood

    @property
    def red_uses_do_nothing_action(self) -> bool:
        """The red agent does nothing."""
        return self._red_uses_do_nothing_action

    @property
    def do_nothing_action_likelihood(self) -> float:
        """Chance for red_uses_do_nothing_action."""
        return self._do_nothing_action_likelihood

    @property
    def red_uses_move_action(self) -> bool:
        """The red agent moves to a different node."""
        return self._red_uses_move_action

    @property
    def move_action_likelihood(self) -> float:
        """Chance of red_uses_move_action."""
        return self._move_action_likelihood

    @property
    def red_uses_zero_day_action(self) -> bool:
        """
        Red uses zero day action.

        The red agent will pick a safe node connected to an infected node and
        take it over with a 100% chance to succeed (can only happen every n
        timesteps).
        """
        return self._red_uses_zero_day_action

    @property
    def zero_day_start_amount(self) -> float:
        """The number of zero-day attacks that the red agent starts with."""
        return self._zero_day_start_amount

    @property
    def days_required_for_zero_day(self) -> int:
        """The amount of 'progress' that need to have passed before the red agent gains a zero day attack."""
        return self._days_required_for_zero_day

    @property
    def red_chooses_target_at_random(self) -> bool:
        """Red picks nodes to attack at random."""
        return self._red_chooses_target_at_random

    @property
    def red_target_node(self) -> str:
        """Red targets a specific node."""
        return self._red_target_node

    @property
    def red_prioritises_connected_nodes(self) -> bool:
        """Red sorts the nodes it can attack and chooses the one that has the most connections."""
        return self._red_prioritises_connected_nodes

    @property
    def red_prioritises_un_connected_nodes(self) -> bool:
        """Red sorts the nodes it can attack and chooses the one that has the least connections."""
        return self._red_prioritises_un_connected_nodes

    @property
    def red_prioritises_vulnerable_nodes(self) -> bool:
        """Red sorts the nodes is can attack and chooses the one that is the most vulnerable."""
        return self._red_prioritises_vulnerable_nodes

    @property
    def red_prioritises_resilient_nodes(self) -> bool:
        """Red sorts the nodes is can attack and chooses the one that is the least vulnerable."""
        return self._red_prioritises_resilient_nodes

    @property
    def red_always_chooses_shortest_distance_to_target(self) -> bool:
        """Red always chooses the absolute shortest distance to target with no randomisation."""
        return self._red_always_chooses_shortest_distance_to_target

