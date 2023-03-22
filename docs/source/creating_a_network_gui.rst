=================
Create a Network
=================

Gettting started
################

To get started, Navigate to the network manager (node tree icon) page from the sidebar or main menu

.. image:: ../_static/create_template_network.gif
  :width: 800
  :alt: create network

Copying a network
######################

Existing networks can be copied by clicking the *clipboard icon* of the network that should be copied and entering
a name for the resultant network in the popup prompt.

Creating a new network
######################

Networks are created from the network manager page. Networks can either be created from a template or from scratch using
the cytoscape network editor. To create a network click the *New network* button and follow the popup prompt.

Deleting a network
##################

Networks can be deleted singularly or on mass. To delete a single network click on the *trash bin icon*.
To delete multiple networks select multiple networks then with each of these networks show as selected click the
*Delete all* button on the bottom right of the window and respond to the prompt.

Template
********
Template networks are created by choosing a named layout representing a certain
network topology and a series of configurable parameters dependent on that topology.

Launch the *Template network creator* by clicking the *Template network* button on the *Network management* page.

Node editor
***********
Networks can be created from scratch in the network editor by manually adding nodes and edges.
Launch the *Node editor* by clicking the *Custom network* button on the *Network management* page.

Saving changes
==============
By default when the network is updated the changes will automatically be saved to the network in the database.

Menus
=====

Node colour key
---------------
This dropdown menu contains a key indicating the meaning of each of the colours that a node can appear within the network

Network toolbars
----------------
This dropdown menu allows for the selection of the menu which will display on the left side of the window.
Either the *Node list* or *Network randomisation* options can be chosen

Node Instantiation
==================

To add an node you must double click a the point you wish for the node to spawn.

Adding Edges Between Nodes
==========================

To add an edge you must click on a node then subsequently click on a different node to join the two with an edge.

Setting Entry Nodes
===================

Manually
--------
By selecting a node the attributes menu will open to the right of the window;
here the entry node status of the node can be toggled

Randomly
--------
Entry nodes can be set randomly by opening the *Network randomisation* menu and toggling on *set random entry nodes*.
From here the location preference of the random entry nodes can also be selected

Setting High Value Nodes
========================

Manually
--------
By selecting a node the attributes menu will open to the right of the window;
here the high value node status of the node can be toggled

Randomly
--------
High value nodes can be set randomly by opening the *Network randomisation* menu and toggling on *set random high value nodes*.
From here the location preference of the random entry nodes can also be selected

Setting Node Vulnerability
==========================

Manually
--------
By selecting a node the attributes menu will open to the right of the window;
here vulnerability of the node can be set using a slider

Randomly
--------
Vulnerability can be set randomly by opening the *Network randomisation* menu and toggling on *set random vulnerability*.
From here the range of random values that the node vulnerability can take must be set
