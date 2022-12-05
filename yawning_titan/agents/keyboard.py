from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


class KeyboardAgent:
    """
    A means for a human player to play the YAWNING-TITAN simulation.

    The keyboard agent provides a basic means for a human player to play the
    YAWNING-TITAN simulation.

    An example of using this class can be found within the `notebooks/Creating and
    playing as a Keyboard Agent.ipynb`
    """

    def __init__(self, env: GenericNetworkEnv):
        self.env = env

    def get_move_set(self):
        """
        Return the action set mapped to action numbers.

        Get the action set for the given environment and map it to the action numbers
        used by the open AI gym env.

        Returns:
            An action mask for top level actions to the first action number in the
            environment. A full dictionary of all the actions that can be taken. The
            action number where the standard actions start (actions that can be applied
            to every node). The number of standard actions
        """
        network_interface = self.env.network_interface
        settings = network_interface.game_mode
        full_action_dict = {}
        top_level_action_mask = {}
        actions = 0
        standard_actions = 0

        # checks the settings for the currently active blue actions
        if settings.blue.blue_uses_deceptive_nodes:
            # If the actions are active then creates a map using dictionaries between
            # the AI gym action number and the
            # action name and any sub actions that this action has
            edge_list = network_interface.edge_map.values()
            full_action_dict["add_deceptive_node"] = edge_list
            top_level_action_mask["add_deceptive_node"] = actions
            actions += len(edge_list)
            standard_actions += len(edge_list)

        if settings.blue.blue_uses_scan:
            full_action_dict["scan"] = None
            top_level_action_mask["scan"] = actions
            actions += 1
            standard_actions += 1
        if settings.blue.blue_uses_do_nothing:
            full_action_dict["do_nothing"] = None
            top_level_action_mask["do_nothing"] = actions
            actions += 1
            standard_actions += 1

        node_list = ["Node " + i for i in network_interface.get_nodes()]
        if settings.blue.blue_uses_reduce_vulnerability:
            full_action_dict["reduce_vulnerability"] = node_list
            top_level_action_mask["reduce_vulnerability"] = actions
            actions += 1
        if settings.blue.blue_uses_restore_node:
            full_action_dict["restore_node"] = node_list
            top_level_action_mask["restore_node"] = actions
            actions += 1
        if settings.blue.blue_uses_make_node_safe:
            full_action_dict["make_node_safe"] = node_list
            top_level_action_mask["make_node_safe"] = actions
            actions += 1
        if settings.blue.blue_uses_isolate_node:
            full_action_dict["isolate"] = node_list
            top_level_action_mask["isolate"] = actions
            actions += 1
        if settings.blue.blue_uses_reconnect_node:
            full_action_dict["connect"] = node_list
            top_level_action_mask["connect"] = actions
            actions += 1
        number_standard_actions = actions - standard_actions

        return (
            top_level_action_mask,
            full_action_dict,
            standard_actions,
            number_standard_actions,
        )

    def play(self, render_graphically: bool = True):
        """
        Play the game as a keyboard agent.

        Allows the user to select an action using the console and displays the
        effect of the action on the envionrment.

        Args:
            render_graphically: If True render using the matplotlib renderer, if False
                display if state of the environment in the console.

        """
        done = False
        notes = {}

        # Runs until the game has been won
        while not done:
            # Gets the possible top level actions
            (
                top,
                move_set,
                start_of_standard_actions,
                number_of_standard_actions,
            ) = self.get_move_set()
            possible_top_actions = list(top.keys())
            print("Current possible actions:")
            for counter, i in enumerate(possible_top_actions):
                # Displays the possible actions to the user
                print(counter, ")", i)
            top_action_legal = False
            chosen_top_action = ""
            # If the user does not input a legal action then they are forced to retry
            # until they do
            while not top_action_legal:
                try:
                    chosen_top_action = int(input("Chosen Action: "))
                    # Checks if the action is legal
                    if chosen_top_action in [
                        i for i in range(len(possible_top_actions))
                    ]:
                        top_action_legal = True
                    else:
                        # Informs the user if they input an invalid action
                        print("Invalid Input")
                except ValueError:
                    print("Invalid Input")
            # Checks if there are any secondary actions for this chosen top action
            secondary_actions = move_set[possible_top_actions[chosen_top_action]]
            chosen_secondary_action = -1
            if secondary_actions is not None:
                # Prints out all of the possible secondary actions
                print("Action Location:")
                for counter, i in enumerate(secondary_actions):
                    print(counter, ")", i)
                secondary_action_legal = False
                chosen_secondary_action = ""
                while not secondary_action_legal:
                    # Runs until the user inputs a legal action
                    try:
                        chosen_secondary_action = int(input("Chosen Location: "))
                        if chosen_secondary_action in [
                            i for i in range(len(secondary_actions))
                        ]:
                            secondary_action_legal = True
                        else:
                            print("Invalid Input")
                    except ValueError:
                        print("Invalid Input")

            # calculates the final action number
            final_action = top[possible_top_actions[chosen_top_action]]
            if chosen_secondary_action != -1:
                if final_action >= start_of_standard_actions:
                    final_action += chosen_secondary_action * number_of_standard_actions
                else:
                    final_action += chosen_secondary_action

            print(final_action)
            # steps the environment 1 step forward using the chosen blue action
            obs, rew, done, notes = self.env.step(final_action)
            if notes["blue_action"] != possible_top_actions[chosen_top_action]:
                if not (
                    notes["blue_action"] == "do_nothing"
                    and possible_top_actions[chosen_top_action] == "add_deceptive_node"
                ):
                    raise EnvironmentError(
                        "Action selected was not the action taken by the environment"
                    )
            # renders the environment to show the effect of the action and the red
            # agents turn
            if render_graphically:
                self.env.render(show_only_blue_view=True, show_node_names=True)
            else:
                for node, state in notes["end_blue_view"].items():
                    print("Node: ", node, " State: ", state)

        # checks if the red or blue agent won
        if self.env.current_duration == self.env.settings["GAME_RULES"]["max_steps"]:
            print("---Blue agent wins---")
        else:
            print("---Red agent wins---")

        # Renders the final true state of the environment
        print("Final True State: ")
        if render_graphically:
            self.env.render()
        else:
            for node, state in notes["end_blue_view"].items():
                print("Node: ", node, " State: ", state)
