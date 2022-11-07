    "red_skill":
    "Red agent's skill modifier"

    "red_use_skill":
    "Is true if red agent will use the skill modifier when attacking a node"

    # red agent attack pattern
    "red_ignore_defences":
    "Is true if red agent will ignore node defences"

    "red_always_succeeds":
    "Is true if red agent will always succeed when attacking"

    "red_attack_from_current_position":
    "Is true if red agent can only attack from its current position"

    "red_attack_from_any_node":
    "Is true if red can attack any safe node anywhere in the network"

    # red spread
    "red_naturally_spread":
    "Is true if red can naturally spread every timestep"

    "red_chance_to_spread_to_connected_node":
    "Chance of red agent spreading to a connected safe node"

    "red_chance_to_spread_to_unconnected_node":
    "Chance of red agent spreading to an unconnected safe node"

    "red_spread_action":
    "Is true if red can try to spread to every connected safe node"

    "red_spread_action_likelihood":
    "Chance of red agent to try and spread to every connected safe node"

    "red_spread_success_chance":
    "Chance for red agent spread action to succeed"

    "red_random_infection_action":
    "Is true if red agent can attack any safe node in the network"

    "red_random_infection_likelihood":
    "Chance of the red agent attacking any random safe node"

    "red_random_infection_success_chance":
    "Chance of the random safe node attacks from succeeding"

    "red_basic_attack_action":
    "Is true if red uses a basic attack to take over a safe node connected to an infected node"

    "red_basic_attack_likelihood":
    "Chance of the basic attack succeeding"

    # red do nothing
    "red_do_nothing_action":
    "Is true if the red agent can choose to do nothing"
    "red_do_nothing_likelihood":
    "Chance of the red agent from doing nothing"

    # red movement
    "red_move_action":
    "Is true if the red agent can choose to move to another infected node"

    "red_move_action_likelihood":
    "Chance of red agent choosing to move to another infected node"

    # red zero days
    "red_zero_day_action":
    "Is true if the red agent can use a zero day to infect a node with 100% success"

    "red_zero_day_start_amount":
    "Integer value specifying how many zero days the red agent can use at the start of the game"

    "red_zero_day_days_required_to_create":
    "Integer value specifying how many timesteps is needed until the red agent can get another zero day"

    # red targeting
    "red_targeting_random":
    "Is true if the red agent targets safe nodes at random"

    "red_targeting_prioritise_connected_nodes":
    "Is true if the red agent prioritises attacking nodes with the most connections"

    "red_targeting_prioritise_unconnected_nodes":
    "Is true if the red agent prioritises attacking nodes with the least connections"

    "red_targeting_prioritise_vulnerable_nodes":
    "Is true if the red agent prioritises attacking nodes with the most vulnerability"

    "red_targeting_prioritise_resilient_nodes":
    "Is true if the red agent prioritises attacking nodes with the least vulnerability"