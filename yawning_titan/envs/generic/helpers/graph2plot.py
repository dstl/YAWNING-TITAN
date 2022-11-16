import math
import statistics
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx
from matplotlib.lines import Line2D


def repeat_check(node: Dict, legend_list: List[Line2D]):
    """
    Checks if a node already exists by comparing the nodes colour and description with nodes already in the legend.

    Args:
        node: A node dict.
        legend_list: The legend list.

    Returns:
        `True` if is already exists, otherwise `False`.
    """
    for legend in legend_list:
        if (
            legend.get_markerfacecolor() == node["colour"]
            and legend.get_label() == node["description"]
        ):
            return True
    return False


class CustomEnvGraph:
    """A network graph rendering environment for Open AI Gym use."""

    def __init__(self, title: str = None):
        """
        Initialise the CustomEnvGraph that is used to visualise and render node environments.

        Args:
            title: The name of the plot
        """
        self.fig = plt.figure(figsize=(12, 6))
        self.fig.suptitle(title)
        # Create subplot for network graph drawing
        self.vis_ax = plt.subplot2grid(shape=(1, 1), loc=(0, 0), rowspan=1, colspan=1)
        plt.subplots_adjust(
            # left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0
            left=0.02,
            bottom=0.15,
            right=0.80,
            top=0.90,
            wspace=0.15,
            hspace=0,
        )

        # Show the graph without blocking the rest of the program
        plt.show(block=False)

    def render(
        self,
        current_step: int,
        g: networkx.Graph,
        pos: dict,
        compromised_nodes: dict,
        uncompromised_nodes: list,
        attacks: list,
        current_time_step_reward: float,
        red_previous_node,
        vulnerability_dict: dict,
        made_safe_nodes: list,
        title: str,
        special_nodes: dict = None,
        entrance_nodes: list = None,
        show_only_blue_view: bool = False,
        target_node: str = None,
        show_node_names: bool = False,
    ):
        """
        Render the current network into an axis.

        Args:
            current_step: the current step in the environment (int)
            g: a networkx object that stores the current connectivity (networkx graph)
            pos: a dictionary that contains the points and their positions
            compromised_nodes: a dictionary of all the compromised nodes and a boolean value if blue can see the intrusion or not
            uncompromised_nodes: a list of all the uncompromised nodes
            attacks: a list of the nodes where an attack is happening
                (infected node, target node)
            current_time_step_reward: the current total reward
            red_previous_node: CURRENTLY NOT USED
            vulnerability_dict: A dictionary that stores the vulnerability of the nodes
            made_safe_nodes: a list of nodes that the blue agent has made safe this turn
            title: The title for the render
            special_nodes: A dictionary containing dictionaries of: nodes, node descriptions and colours for the nodes
            entrance_nodes: Nodes that serve as a gateway for the red agent to be able to access the network
            show_only_blue_view: If true only shows what the blue agent can see
            show_node_names: Show the names of nodes
        """
        # If no value for  entrance nodes is passed in then it is set to an empty list
        if entrance_nodes is None:
            entrance_nodes = []
        if special_nodes is None:
            special_nodes = {}
        self.vis_ax.clear()

        # Creates a list that contains the details for the legend
        legend_objects = [
            # Each item in the legend is an marker with a colour and a description
            # Compromised Nodes
            Line2D(
                [0],
                [0],
                color="white",
                marker="o",
                markerfacecolor="orange",
                label="Compromised Node",
                markersize=15,
            ),
            # Vulnerable safe nodes
            Line2D(
                [0],
                [0],
                color="white",
                marker="o",
                markerfacecolor="#00FF13",
                label="Safe Node: Weak",
                markersize=15,
            ),
            # Safe nodes with low vulnerability
            Line2D(
                [0],
                [0],
                color="white",
                marker="o",
                markerfacecolor="#006007",
                label="Safe Node: Strong",
                markersize=15,
            ),
            # Nodes that have just been taken over by red
            Line2D(
                [0],
                [0],
                color="white",
                marker="o",
                markerfacecolor="red",
                label="Attacked Node",
                markersize=15,
            ),
            # The nodes that blue has "patched" or "fixed" this turn
            Line2D(
                [0],
                [0],
                color="white",
                marker="o",
                markerfacecolor="#4ef2e7",
                label="Blue Patch",
                markersize=15,
            ),
        ]
        # If a target node is specified add to the legend
        if target_node is not None:
            legend_objects.append(
                Line2D(
                    [0],
                    [0],
                    color="white",
                    marker="o",
                    markerfacecolor="#2c195e",
                    label="Target Node",
                    markersize=15,
                )
            )
            # plots the target node
            plt.scatter(
                [pos[str(target_node)][0]],
                [pos[str(target_node)][1]],
                color="#2c195e",
                s=324,
                zorder=8,
            )

        legend_objects.extend(
            [
                # An edge that red has attacked along this turn
                Line2D(
                    [0],
                    [0],
                    color="red",
                    marker="_",
                    markerfacecolor="red",
                    label="Attack Path",
                    markersize=15,
                ),
                # An edge
                Line2D(
                    [0],
                    [0],
                    color="gray",
                    marker="_",
                    markerfacecolor="gray",
                    label="Connection",
                    markersize=15,
                ),
            ]
        )

        # If only showing the blue view then only render red nodes that blue can see
        if not show_only_blue_view:
            legend_objects.append(
                Line2D(
                    [0],
                    [0],
                    color="white",
                    marker="$\\bf{O}$",
                    markerfacecolor="red",
                    label="Unknown Compromise",
                    markersize=12,
                )
            )
            legend_objects.append(
                Line2D(
                    [0],
                    [0],
                    color="white",
                    marker="$\\bf{O}$",
                    markerfacecolor="blue",
                    label="Known Compromise",
                    markersize=12,
                )
            )
        # Some environments may have special custom nodes that they want to add
        if len(special_nodes) > 0:
            for _, node_info in special_nodes.items():

                # only insert if the legend is not in the list yet
                if not repeat_check(node_info, legend_objects):
                    # Inserts the object into the legends at position 3. This is because it looks better if there are any
                    # special nodes added that they are added at the some point as the other nodes in the legend
                    legend_objects.insert(
                        3,
                        Line2D(
                            [0],
                            [0],
                            color="white",
                            marker="o",
                            markerfacecolor=node_info["colour"],
                            label=node_info["description"],
                            markersize=15,
                        ),
                    )

        # If entrance nodes are used then they are added to the legend
        if entrance_nodes is not None:
            legend_objects.append(
                Line2D(
                    [0],
                    [0],
                    color="white",
                    marker="$\\bf{E}$",
                    markerfacecolor="black",
                    label="Entry Node",
                    markersize=12,
                )
            )
        # plots all of the edges in the graph
        for edge in g.edges:
            plt.plot(
                [pos[edge[0]][0], pos[edge[1]][0]],
                [pos[edge[0]][1], pos[edge[1]][1]],
                color="grey",
                zorder=1,
            )

        # plots all of the current turns attacks
        red_nodes_x = []
        red_nodes_y = []
        for attack in attacks:
            red_nodes_x.append(pos[attack[1]][0])
            red_nodes_y.append(pos[attack[1]][1])
            if attack[0] is not None:
                plt.plot(
                    [pos[attack[0]][0], pos[attack[1]][0]],
                    [pos[attack[0]][1], pos[attack[1]][1]],
                    color="red",
                    zorder=2,
                )

        # All the shades of green for the different levels of vulnerability
        green_shades = [
            "#00FF13",
            "#00DF11",
            "#00BF0E",
            "#009F0C",
            "#00800A",
            "#006007",
        ]
        max_x = 0
        max_y = 0
        min_x = 100000
        min_y = 100000
        comp_x = []
        comp_y = []
        known_comp_x = []
        known_comp_y = []
        unknown_comp_x = []
        unknown_comp_y = []
        safe_x = []
        safe_y = []
        safe_colours = []
        void_x = []
        void_y = []
        special_x = []
        special_y = []
        special_colour = []
        made_safe_x = []
        made_safe_y = []
        for i in g.nodes():
            max_x = max(max_x, pos[i][0])
            max_y = max(max_y, pos[i][1])
            min_x = min(min_x, pos[i][0])
            min_y = min(min_y, pos[i][1])
            if i in made_safe_nodes:
                # get the locations of nodes that have been made safe
                made_safe_x.append(pos[i][0])
                made_safe_y.append(pos[i][1])
            elif i in special_nodes:
                # get the locations of special nodes
                special_x.append(pos[i][0])
                special_y.append(pos[i][1])
                special_colour.append(special_nodes[i]["colour"])
            elif i in compromised_nodes.keys():
                if compromised_nodes[i]:
                    # get the locations of compromised nodes (unknown)
                    comp_x.append(pos[i][0])
                    comp_y.append(pos[i][1])
                    if not show_only_blue_view:
                        # get the locations of compromised nodes (known)
                        known_comp_x.append(pos[i][0])
                        known_comp_y.append(pos[i][1])
                else:
                    if not show_only_blue_view:
                        comp_x.append(pos[i][0])
                        comp_y.append(pos[i][1])
                        unknown_comp_x.append(pos[i][0])
                        unknown_comp_y.append(pos[i][1])
                    else:
                        # get the location of the safe nodes
                        vuln = vulnerability_dict[i]
                        index = 5 - math.floor(vuln * (len(green_shades) - 1))
                        safe_colours.append(green_shades[index])
                        safe_x.append(pos[i][0])
                        safe_y.append(pos[i][1])
            elif i in uncompromised_nodes:
                # get the locations of safe nodes
                vuln = vulnerability_dict[i]
                index = 5 - math.floor(vuln * (len(green_shades) - 1))
                safe_colours.append(green_shades[index])
                safe_x.append(pos[i][0])
                safe_y.append(pos[i][1])
            else:
                void_x.append(pos[i][0])
                void_y.append(pos[i][1])

        # plots any nodes that have no features
        plt.scatter(void_x, void_y, color="grey", s=300, zorder=1)

        # plots all of the compromised nodes
        plt.scatter(comp_x, comp_y, color="orange", s=324, zorder=8)
        # plot the circles around unknown compromised nodes
        plt.scatter(unknown_comp_x, unknown_comp_y, color="red", s=484, zorder=7)
        # plot the circles around known compromised nodes
        plt.scatter(known_comp_x, known_comp_y, color="blue", s=484, zorder=7)
        # plots all of the safe nodes
        plt.scatter(safe_x, safe_y, color=safe_colours, s=324, zorder=5)
        # plots all of the recently taken red nodes
        plt.scatter(red_nodes_x, red_nodes_y, color="red", s=324, zorder=9)
        # plots all of the nodes that have just been patched
        plt.scatter(made_safe_x, made_safe_y, color="#4ef2e7", s=324, zorder=10)
        # plots any special nodes for the env
        plt.scatter(special_x, special_y, color=special_colour, s=324, zorder=6)
        # plot the entrance nodes
        for node in entrance_nodes:
            plt.scatter(
                [pos[node][0]],
                [pos[node][1]],
                color="black",
                zorder=11,
                s=121,
                marker="$E$",
            )
        if show_node_names:
            for node in g.nodes:
                plt.text(
                    pos[node][0] + 0.1,
                    pos[node][1] + 0.1,
                    node,
                    color="red",
                    fontsize=12,
                    zorder=11,
                )

        # Creates a string containing information about the current state of the network

        info = (
            "Current Step: "
            + str(current_step)
            + "\nReward for current time step: "
            + str(current_time_step_reward)
            + "\nCurrent Avg vulnerability: "
            + str(round(statistics.mean(vulnerability_dict.values()), 2))
        )

        ax = plt.gca()
        ax.legend(
            handles=legend_objects,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            borderpad=1,
            labelspacing=1,
            fontsize=10,
            edgecolor="black",
        )
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        ax.axes.set_xlim(min_x - 0.1 * max_x, max_x * 1.1)
        ax.axes.set_ylim(min_y - 0.1 * max_y, max_y * 1.1)

        ax.set_xlabel(info)
        for pos in ["left", "right", "top", "bottom"]:
            plt.gca().spines[pos].set_visible(False)

        # plt.show()

        plt.pause(0.001)

    def close(self):
        """Close all handles to external renderers."""
        plt.close()
