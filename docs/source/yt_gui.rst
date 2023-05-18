.. _yt-gui:

Yawning-Titan GUI
=================

How is the Yawning-Titan GUI built
-----------------------------------
The Yawning-Titan GUI is designed as an optional extension to the underlying Yawning-Titan library.
The Yawning Titan GUI primarily uses `Django <https://github.com/django/django/>`_ to convert aspects of Yawning-Titan
into html objects that can be interacted with in a local browser instance by the user thereby allowing the underlying
Python to be executed without need for a command line interface or knowledge of the python language.

The Yawning-Titan GUI also integrates with a customised version `Cytoscape JS <https://github.com/cytoscape/cytoscape.js/>`_
which has been extended to work directly with Yawning-Titan. This allows for users to directly interface with network
topologies and edit the position and attributes of network nodes that actively updates a database of stored networks.

Start the GUI from the CLI
--------------------------

Running the GUI from the Yawning-Titan CLI is very easy and can be done in one line:

.. code:: bash

    yawning-titan gui

Start the GUI from the repo
---------------------------

If you're a developer making changes to Yawning-Titan, you can run the GUI from the cloned repo to test your changes:

.. code:: bash

    python3 -m manage.py runserver

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   creating_a_game_mode_gui
   creating_a_network_gui
   running_a_session_gui
