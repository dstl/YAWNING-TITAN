Create a Network
================

Imports
*******

To get started, import Network and Node.

.. code:: python

    from yawning_titan.networks.node import Node
    from yawning_titan.networks.network import Network

Network Instantiation
*********************

To create a Network, first, we must instantiate an instance of :class:`~yawning_titan.networks.network.Network`.

While a :class:`~yawning_titan.networks.network.Network` can be instantiated right out of the box by calling ``Network()``,
there are some configurable parameters that you can set (we'll get onto these further down).

.. code:: python

network = Network()

Node Instantiation
******************

Next, we instantiate some :class:`~yawning_titan.networks.node.Node`'s.

Again, while a :class:`~yawning_titan.networks.node.Node` can be instantiated right out of the box by calling ``Node()``,
there are some configurable parameters that you can set (we'll get onto these further down).

.. code:: python

    node_1 = Node()
    node_2 = Node()
    node_3 = Node()
    node_4 = Node()
    node_5 = Node()
    node_6 = Node()

Add Nodes to a Network
**********************

Currently we only have an instance of :class:`~yawning_titan.networks.network.Network` and some instances of
:class:`~yawning_titan.networks.node.Node`.

To add a :class:`~yawning_titan.networks.node.Node` to a :class:`~yawning_titan.networks.network.Network`, we need to
call ``.add_node()``.

.. code:: python

    network.add_node(node_1)
    network.add_node(node_2)
    network.add_node(node_3)
    network.add_node(node_4)
    network.add_node(node_5)
    network.add_node(node_6)

Adding Edges Between Nodes
**************************

With our :class:`~yawning_titan.networks.node.Node`'s added to the :class:`~yawning_titan.networks.network.Network`,
we can begin joining them by calling ``.add_edge()``.

.. code:: python

    network.add_edge(node_1, node_2)
    network.add_edge(node_1, node_3)
    network.add_edge(node_1, node_4)
    network.add_edge(node_2, node_5)
    network.add_edge(node_2, node_6)

And that's it, our basic :class:`~yawning_titan.networks.network.Network` has been created.

Setting Entry Nodes
*******************

Entry nodes can be set manually at the :class:`~yawning_titan.networks.node.Node`:

.. code:: python

    node_1.entry_node = True

Or by configuring the :class:`~yawning_titan.networks.network.Network` to set them at random:

.. code:: python

    from yawning_titan.networks.network import RandomEntryNodePreference

    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 1
    network.random_entry_node_preference = RandomEntryNodePreference.EDGE
    network.reset_random_entry_nodes()

Setting EntHigh Value Nodes
***************************

High value nodes can be set manually at the :class:`~yawning_titan.networks.node.Node`:

.. code:: python

    node_1.high_value_node = True

Or by configuring the :class:`~yawning_titan.networks.network.Network` to set them at random:

.. code:: python

    from yawning_titan.networks.network import RandomHighValueNodePreference

    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 1
    network.random_high_value_node_preference = RandomHighValueNodePreference.FURTHEST_AWAY_FROM_ENTRY
    network.reset_random_high_value_nodes()

Setting Node Vulnerability
**************************

A nodes vulnerability can be set manually at the :class:`~yawning_titan.networks.node.Node`:

.. code:: python

    node_1.vulnerability = 0.5

Or by configuring the :class:`~yawning_titan.networks.network.Network` to set them at random:

.. code:: python

    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()

Reset the Network
*****************

To reset all entry nodes, high value nodes, and vulnerabilities at once:

.. code:: python

    network.reset()

View a Networks Node Details
****************************

To view a table of the :class:`~yawning_titan.networks.node.Node`'s in a :class:`~yawning_titan.networks.network.Network`:

.. code:: python

    network.show(verbose=True)

This gives an output like:

.. code:: text

    UUID                                  Name    High Value Node    Entry Node      Vulnerability  Position (x,y)
    ------------------------------------  ------  -----------------  ------------  ---------------  ----------------
    bf308d9f-8382-4c15-99be-51f84f75f9ed          False              False               0.0296121  0.34, -0.23
    1d757e6e-b637-4f63-8988-36e25e51cd55          False              False               0.711901   -0.34, 0.23
    8f76d75c-5afd-4b2c-98ed-9c9dc6181299          True               False               0.65281    0.50, -0.88
    38819aa3-0c05-4863-8b9d-c704f254e065          False              False               0.723192   1.00, -0.13
    cc06f5e0-c956-449a-b397-b0e7bed3b8d4          False              True                0.85681    -0.49, 0.88
    665b150b-fbd3-42a7-b899-3770ef2b285a          False              False               0.48435    -1.00, 0.13

Example Network
***************

Here we will create the corporate network that is used as a fixture in the Yawning-Titan tests (`tests.conftest.corporate_network`).

Names are added to each of the nodes for when they're displayed in a network graph.

.. code:: python

    # Instantiate the Network
    network = Network(
        set_random_entry_nodes=True,
        num_of_random_entry_nodes=3,
        set_random_high_value_nodes=True,
        num_of_random_high_value_nodes=2,
        set_random_vulnerabilities=True,
    )

    # Instantiate the Node's and add them to the Network
    router_1 = Node("Router 1")
    network.add_node(router_1)

    switch_1 = Node("Switch 1")
    network.add_node(switch_1)

    switch_2 = Node("Switch 2")
    network.add_node(switch_2)

    pc_1 = Node("PC 1")
    network.add_node(pc_1)

    pc_2 = Node("PC 2")
    network.add_node(pc_2)

    pc_3 = Node("PC 3")
    network.add_node(pc_3)

    pc_4 = Node("PC 4")
    network.add_node(pc_4)

    pc_5 = Node("PC 5")
    network.add_node(pc_5)

    pc_6 = Node("PC 6")
    network.add_node(pc_6)

    server_1 = Node("Server 1")
    network.add_node(server_1)

    server_2 = Node("Server 2")
    network.add_node(server_2)

    # Add the edges between Node's
    network.add_edge(router_1, switch_1)
    network.add_edge(switch_1, server_1)
    network.add_edge(switch_1, pc_1)
    network.add_edge(switch_1, pc_2)
    network.add_edge(switch_1, pc_3)
    network.add_edge(router_1, switch_2)
    network.add_edge(switch_2, server_2)
    network.add_edge(switch_2, pc_4)
    network.add_edge(switch_2, pc_5)
    network.add_edge(switch_2, pc_6)

    # Reset the entry nodes, high value nodes, and vulnerability scores by calling .setup()
    network.reset()

    # View the Networks Node Details
    network.show(verbose=True)

Gives:

.. code:: text

    UUID                                  Name      High Value Node    Entry Node      Vulnerability  Position (x,y)
    ------------------------------------  --------  -----------------  ------------  ---------------  ----------------
    c883596b-1d86-44f5-b4de-331292d8e3d5  Router 1  False              False               0.320496   0.00, -0.00
    b2bd683b-a773-40de-85e8-36c21e66613d  Switch 1  False              False               0.889044   0.01, 0.61
    68d9689b-5365-4022-b3bd-92bdc5a1627b  Switch 2  True               False               0.0671795  -0.00, -0.62
    3554ed26-9480-487b-9d3c-57975654a2af  PC 1      False              False               0.400729   -0.38, 0.69
    89700b3f-8be2-4b70-a21e-a0772551a6bc  PC 2      True               False               0.0807914  0.18, 1.00
    82e91c52-5458-493a-a7cd-00fb702d6af1  PC 3      False              True                0.86676    0.39, 0.70
    91edf896-f004-4ca7-9587-cc8417c4a26b  PC 4      False              False               0.967413   -0.39, -0.69
    ebbc79f7-9a52-4a08-8b56-fee816284b54  PC 5      False              True                0.684436   0.38, -0.69
    2cdaaf06-9b4a-41e9-ba6f-129aec634080  PC 6      False              False               0.727421   -0.19, -1.00
    b81ad769-688a-4d02-ae7b-a64f0984b101  Server 1  False              False               0.630726   -0.17, 0.99
    52cbd8ec-b063-40c5-a73e-a51291347e8f  Server 2  False              True                0.789554   0.17, -1.00
