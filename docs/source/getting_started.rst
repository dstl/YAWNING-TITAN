.. _getting-started:

Getting Started
===============
Pre-Requisites
**************
In order to get YAWNING TITAN (YT) installed, you will need to have the following installed:
 * python3.6+
 * python3-pip
 * virtualenv

Installation
************
1. Navigate to the YT folder and create a new python virtual environment

.. code-block:: text

    python3 -m venv <name_of_venv>

2. Activate virtual environment

.. code-block:: text

    source <name_of_venv>

3. Install yawning-titan into the environment along with all of it's dependencies

.. code-block:: text

    python3 -m pip install -e .


What's required to create a YT ``GenericEnv()``?
***************************************************
Now that you have installed YT, it's time to create your first environment but lets first quickly describe whats required to
create a YT ``GenericEnv()``. YT has the functionality to create generic OpenAI Gym based network environments and
requires the following to create a ``GenericEnv()``:

* A Scenario Settings File - Within YT, a scenario settings files defines everything other than the networks topology.
* A Red agent - Within YT, these are represented as probabilistic and can be configured using the scenario's settings file.
* A Blue agent - Within YT, blue agents are considered as ``learners`` which means they can be driven by some sort of decision making process such as a Reinforcement Learning algorithm.
* The Network to be defended. This is input into YT in two components. The first is an adjacency matrix which represents an undirected graphs connectivity and the second is a dictionary which contains the x and y co-ordinates for
  each vertex of the graph to support 2D plotting.

.. note::
    YT contains a network creator helper which generates both the adjacency matrix and the
    dictionary of points. It wraps ``Networkx``'s standard functions such as star and mesh.
    We will demonstrate the use of this later in this Getting Started guide.

    In addition to the five inputs detailed above, you can also supply the environment with optional
    parameters which are the Entry Node which act as the gateway nodes that the red uses to attack the
    network and node vulnerability scores. This is to aid modelling real networks within an abstracted
    environment such as YT.

Creating a YT ``GenericEnv()`` and Training an Stable Baselines 3 Agent
**************************************************************************

.. note::
    All of this section can be found within the ``notebooks/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering`` if you'd
    prefer to work through it like that.

For the purposes of this example, we are going to first create an environment that has the same network topology as
`Ridley 2017 <https://www.nsa.gov.Portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9>` which
looks likes this.

.. image:: ./images/18-node.gif
   :width: 400


Setting up the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

YAWNING TITAN's generic network environment is highly configurable. The main way that you can affect
and change the environment is through the config file. The config file is a yaml file that
contains settings such as what actions the blue agent can take and how the blue agent
wins. The config file is broken into the following sections:

* RED
    Settings relating to the red agent
* BLUE
    Settings relating to the blue agent
* GAME RULES
    Settings relating to the way the game is played and how it is won
* REWARDS
    Settings relating to the rewards that the blue agent gets for its actions
* MISCELLANEOUS
    Other settings that do not fit into any other category

The network interface comes with a config file check that ensures that the settings file
has not become corrupted and that the settings values chosen are valid.

To see a description of every setting see: :ref:`config file`

You can create your own settings file or use one of the pre-made ones.

If you do not supply the network with a config file then it will use a default one.
To supply one of your own config files then pass the file path of your config file
to the network_interface.

Creating a network representation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You will need to define the network that the agents will compete in. The network interface
requires an adjacency matrix and a dictionary of point locations (used to render the network).

YT contains a couple of builtin methods to create networks based of standard topologies.
Theses include:

* create_18_node_network
    Creates the 18 node network for the research paper: https://www.nsa.gov.Portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9
* create_mesh
    Creates a mesh network with variable connectivity
* create_star
    Creates a network based of the star topology
* create_p2p
    Creates a network based of two "peers" connecting
* create ring
    Creates a network based of the ring topology
* custom_network
    Creates a network using console input from the user
* procedural_network
    Creates a network with defined amounts of nodes with certain connectivity
* gnp_random_connected_graph
    Creates a mesh that is guaranteed for each node to have at least one connection

To create the data for a network::

    matrix, node_positions = network_creator.create_18_node_network()

    network_creator.save_network("current_net.txt", matrix, node_positions)
    matrix, node_positions = network_creator.load_network("current_net.txt")

The above code also shows how to save and load networks

Generating the network interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the Network Interface object::

    network_interface = NetworkInterface(matrix, node_positions)

There are also some optional parameters that you can use in the the network interface

* entry_nodes
    A list of node names that act as doorways to the network for the red agent. If left
    blank then the network generates some automatically. There are options in the settings
    file to choose how entry nodes are generated if they are left blank.
* vulnerabilities
    A dictionary of node names and vulnerabilities. A vulnerability is a number between 0 and 1
    that represents how easy a node is to compromise (1 very easy, 0 very hard). If left
    blank then generated randomly.
* high value target
    If the config is set up so that the red agent wins if it compromises a high value
    target then you can set the name of the node to be the target. Generated automatically
    if left blank.
* settings_path
    The path to the settings file. If left blank a default settings file is used. To see
    more information on the settings file see: :ref:`config file`

Settings up the Red and Blue agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To run an experiment through the generic network environment you will need a red and a
blue agent.

YAWNING TITAN comes supplied with a probabilistic customisable red agent and a
customisable RL blue agent.

Both the red and blue agents can be modified by changing the settings in the configuration
file under the appropriate section.

To create a blue agent::

    blue_agent = BlueInterface(network_interface)

To create a red agent::

    red_agent = RedInterface(network_interface)



Creating the environment
^^^^^^^^^^^^^^^^^^^^^^^^^

Create the open AI gym environment ::

    number_of_actions = blue_agent.get_number_of_actions()

    env = GenericNetworkEnv(red_agent, blue_agent, network_interface, number_of_actions)
