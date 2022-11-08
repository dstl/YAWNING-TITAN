.. _config file:

The Config File Explained
=========================

Red agent settings:
********************
 * **red_skill:**
    The red agents skill level. Higher means that red is more likely to succeed in attacks

 * **red_uses_skill:**
    Red uses its skill modifier when attacking nodes

 * **red_ignores_defences:**
    The red agent ignores the defences of nodes

 * **red_always_succeeds:**
    Reds attacks always succeed

 * **red_can_only_attack_from_red_agent_node:**
    The agent has a central "command" node. the red agent can only attack from its command node and so has to move around the environment to be able to be able to conquer the whole thing

 * **red_can_attack_from_any_red_node:**
    The red agent can act from and control any node that it has compromised

 * **red_can_naturally_spread:**
    The red agent naturally spreads its influence every time-step

 * **chance_to_spread_to_connected_node:**
    If a node is connected to a compromised node what chance does it have to become compromised every turn through natural spreading

 * **chance_to_spread_to_unconnected_node:**
    If a node is not connected to a compromised node what chance does it have to become randomly infected through natural spreading

 * **Red Actions**
     * **red_uses_spread_action:**

        Every compromised node has a chance to infect every neighbouring safe node

         * **spread_action_likelihood:**
            The weighting for the action - how often the red agent performs the action
         * **chance_for_red_to_spread:**
            The chance for each "spread" to occur

     * **red_uses_random_infect_action:**

        Red has a chance to infect every safe node irrespective of its position in the network

         * **random_infect_action_likelihood:**
            The weighting for the action - how often the red agent performs the action
         * **chance_for_red_to_random_compromise:**
            The chance for each "infect" to succeed

     * **red_uses_basic_attack_action:**

        The red agent picks a single node connected to an infected node and tries to attack and take over that node

         * **basic_attack_action_likelihood:**
            The weighting for the action - how often the red agent performs the action

     * **red_uses_do_nothing_action:**

        The red agent does nothing on this turn

         * **do_nothing_action_likelihood:**
            The weighting for the action - how often the red agent performs the action

     * **red_uses_move_action:**

        The red agent moves it central "control" node to a connected compromised node

         * **move_action_likelihood:**
            The weighting for the action - how often the red agent performs the action

     * **red_uses_zero_day_action:**

        Red builds up and uses an attack that has a 100% success chance to compromise a single node

         * **zero_day_start_amount:**
            The number of zero day attacks the red agent starts with
         * **days_required_for_zero_day:**
            The number of progress "points" that the red agent needs to earn to perform a zero day action

* **Red Targeting methods**
     * **red_chooses_target_at_random:**
        Red picks nodes to attack at random
     * **red_prioritises_connected_nodes:**
        Red sorts the nodes it can attack and chooses the one that has the most connections
     * **red_prioritises_un_connected_nodes:**
        Red sorts the nodes it can attack and chooses the one that has the least connections
     * **red_prioritises_vulnerable_nodes:**
        Red sorts the nodes is can attack and chooses the one that is the most vulnerable
     * **red_prioritises_resilient_nodes:**
        Red sorts the nodes is can attack and chooses the one that is the least vulnerable

Observation Space settings
***************************
 * **compromised_status:**
    The blue agent can see the compromised status of all the nodes
 * **vulnerabilities:**
    The blue agent can see the vulnerability scores of all the nodes
 * **node_connections:**
    The blue agent can see what nodes are connected to what other nodes
 * **average_vulnerability:**
    The blue agent can see the average vulnerability of all the nodes
 * **graph_connectivity:**
    The blue agent can see a graph connectivity score
 * **attacking_nodes:**
    The blue agent can see all of the nodes that have recently attacked a safe node
 * **attacked_nodes:**
    The blue agent can see all the nodes that have recently been attacked
 * **special_nodes:**
    The blue agent can see all of the special nodes (entry nodes, high value nodes)
 * **red_agent_skill:**
    The blue agent can see the skill level of the red agent


Blue Agent settings
*******************

The blue agent does not have to have perfect detection. In these settings you can change how much information blue
can gain from the red agents actions. There are two different pieces of information blue can get: intrusions and
attacks.

**Intrusions**

An intrusion is when the red agent takes over a node and compromises it. You can change the chance that blue has to
be able to detect this using the "chance_to_immediately_discover_intrusion". If blue does not detect an intrusion
then it can use the scan action to try and discover these intrusions with "chance_to_discover_intrusion_on_scan".

There are also deceptive nodes that blue can place down. These nodes are used as detectors to inform blue when they
are compromised. They should have a chance to detect of 1 so that they can detect everything (at the very least
they should have a chance to detect higher than the normal chance to detect) but you can modify it if you so wish
with "chance_to_immediately_discover_intrusion_deceptive_node" and "chance_to_discover_intrusion_on_scan_deceptive_node"

**Attacks**

Attacks are the actual attacks that the red agent does to compromise the nodes. For example you may be able to see
that node 14 is compromised but using the attack detection, the blue agent may be able to see that it was node 12
that attacked node 14. You can modify the chance for blue to see attacks that failed, succeeded (and blue was able
to detect that the node was compromised) and attacks that succeeded and the blue agent did not detect the intrusion.

Again there are settings to change the likelihood that a deceptive node can detect an attack. While this should
remain at 1, it is open for you to change.

 * **max_number_deceptive_nodes:**
    The number of deceptive nodes that blue can place down. Deceptive nodes are special nodes that have a higher chance (usually 100%) of being able to detect when they are being attacked/compromised.
 * **can_discover_failed_attacks:**
    If the blue agent can detect attacks that have failed

 * **Intrusions**
     * **chance_to_immediately_discover_intrusion:**
        Chance for blue to discover when red compromises a node the instant it is taken
     * **chance_to_discover_intrusion_on_scan:**
        Chance for blue to find a node red has compromised during the scan action
     * **chance_to_immediately_discover_intrusion_deceptive_node:**
        Chance for blue to discover when red compromises a deceptive node the instant it is taken
     * **chance_to_discover_intrusion_on_scan_deceptive_node:**
        Chance for blue to find a deceptive node red has compromised during the scan action
 * **Attacks**
     * **chance_to_discover_failed_attack:**
        Chance for blue to discover a red attack that did not compromise a node
     * **can_discover_succeeded_attacks_if_compromise_is_discovered:**
        If an attack compromises a node and blue detected the intrusion can blue detect the attack
     * **can_discover_succeeded_attacks_if_compromise_is_not_discovered:**
        If an attack compromises a node and blue did not detect the intrusion can blue detect the attack
     * **chance_to_discover_succeeded_attack_compromise_known:**
        Chance for blue to discover a successful attack the blue can see has compromised the node
     * **chance_to_discover_succeeded_attack_compromise_not_known:**
        Chance for blue to discover a successful attack the blue cannot see has compromised the node
     * **chance_to_discover_failed_attack_deceptive_node**
        Chance for blue to discover an attack that failed to compromise a deceptive node
     * **chance_to_discover_succeeded_attack_deceptive_node:**
        Chance for blue to discover an attack that succeeded to compromise a deceptive node
 * **making_node_safe_modifies_vulnerability:**
    Using the make_node_safe action also modifies the vulnerability of a node by a fixed amount
 * **vulnerability_change_during_fix:**
    The vulnerability change the occurs during the make_node_safe action
 * **making_node_safe_gives_random_vulnerability:**
    Using the make_node_safe action modifies the vulnerability to a new random number
 * **Blue Actions**
     * **blue_uses_reduce_vulnerability:**
        Blue can use the reduce vulnerability of a node
     * **blue_uses_restore_node:**
        Blue can restore a node to its default (initial) state
     * **blue_uses_make_node_safe:**
        Blue patches a node and removes the red agent from it
     * **blue_uses_scan:**
        Blue tries to check the status of all of the nodes to detect and red intrusions
     * **blue_uses_isolate_node:**
        Blue isolates a node and removes all connections to and from the node
     * **blue_uses_reconnect_node:**
        Blue reconnects a node adding back any lost connections
     * **blue_uses_do_nothing:**
        Blue does nothing
     * **blue_uses_deceptive_nodes:**
        Blue can place down deceptive nodes on an existing edge. Deceptive nodes can more accurately detect when red tries to compromise them

Game Rules
***********

 * **node_vulnerability_lower_bound:**
    The lowest value that could be generated (or reached) for vulnerability (lower means more resilient nodes)
 * **node_vulnerability_upper_bound:**
    The highest value that could be generated (or reached) for vulnerability (higher means easier to compromise nodes)
 * **max_steps:**
    How many steps blue has to survive for before winning
 * **lose_when_all_nodes_lost:**

    Does the red agent win if it takes all of the nodes

     * **lose_when_n_percent_of_nodes_lost:**
        Does the red agent win if it takes n% of all the nodes
 * **percentage_of_nodes_compromised_equals_loss:**
    If red wins if it takes n% of nodes what value is n
 * **lose_when_high_value_node_lost:**

    Does red win if a special "high value" node is taken

     * **number_of_high_value_nodes:**
        How many "high value" nodes will be chosen
     * **choose_high_value_nodes_placement_at_random:**
        Choose the "high value" node at random
     * **choose_high_value_nodes_furthest_away_from_entry:**
        Choose the "high value" to be one of the nodes furthest from all of the entry points
 * **choose_entry_nodes_randomly:**
    If no entry nodes are supplied choose some at random
 * **number_of_entry_nodes:**
    If no entry nodes are supplied and are automatically generated, how many should be generated
 * **prefer_central_nodes_for_entry_nodes:**
    If no entry nodes are supplied then when auto-generating new entry nodes apply a bias towards more central/connected nodes
 * **prefer_edge_nodes_for_entry_nodes:**
    If no entry nodes are supplied then when auto-generating new entry nodes apply a bias towards more edge/outer nodes
 * **grace_period_length:**
    The length of a grace period at the start of the game. During this time the red agent cannot act. This gives the blue agent a chance to "prepare" (A length of 0 means that there is no grace period)

Reset
******
 * **randomise_vulnerabilities_on_reset:**
    Pick new vulnerabilities for all the nodes on every reset
 * **choose_new_high_value_nodes_on_reset:**
    Pick new high value nodes on every reset
 * **choose_new_entry_nodes_on_reset:**
    Pick new entry nodes every reset


Rewards
*******

 * **rewards_for_loss:**
    The reward blue gets for losing
 * **rewards_for_reaching_max_steps:**
    The reward blue gets for winning
 * **reward_function:**
    Choose the reward method. There are several built in example reward methods that you can choose from (shown below) You can also create your own reward method by copying one of the built in methods and calling it here

    Built in reward methods:
         * standard_rewards
         * one_per_timestep
         * safe_nodes_give_rewards
         * punish_bad_actions

Miscellaneous
**************
 * **output_timestep_data_to_json:**
    Toggle to output a json file for each step that contains the connections between nodes, the states of the nodes and the attacks that blue saw in that turn
