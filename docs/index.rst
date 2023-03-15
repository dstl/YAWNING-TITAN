Welcome to YAWNING-TITAN's documentation!
=========================================

What is YAWNING-TITAN?
------------------------

YAWNING-TITAN (**YT**) is a collection of abstract, graph based cyber-security simulation environments that supports the training of
intelligent agents for autonomous cyber operations based on OpenAI Gym. **YT** focuses on providing a fast
simulation to support the development of defensive autonomous agents who face off against probabilistic red agents.

**YT** contains a small number of specific, self contained OpenAI Gym environments for autonomous cyber defence research,
which are great for learning and debugging, as well as a flexible, highly configurable generic environment which can be used to represent a range of scenarios
of increasing complexity and scale. The generic environment only needs a network topology and a settings file in order to create
an OpenAI Gym compliant environment which also enables open research and enhanced reproducibility.

How can YAWNING-TITAN be used?
------------------------------

YAWNING_TITAN can be used either through the command line interface or through a bespoke graphical user interface (**GUI**).
The idea of this is to make YT as accessible as possible to all users out of the box whilst not compromising the ability
for users to make in depth modifications to the source code.

Design Principles
-----------------------

**YT** has been designed with the following key principles in mind:
- Simplicity over complexity
- Minimal Hardware Requirements
- Operating System agnostic
- Support for a wide range of algorithms
- Enhanced agent/policy evaluation support
- Flexible environment and game rule configuration
- intuitive representation of all elements
- Generation of evaluation episode visualisations (gifs)

What is YAWNING-TITAN built with
--------------------------------------
**YT** is built on the shoulders of giants and heavily relies on the following libraries:

 * `OpenAI's Gym <https://gym.openai.com/>`_ is used as the basis for all of the environments
 * `Networkx <https://github.com/networkx/networkx>`_ is used as the underlying data structure used for all environments
 * `Stable Baselines 3 <https://github.com/DLR-RM/stable-baselines3>`_ is used as a source of RL algorithms
 * `Rllib (part of Ray) <https://github.com/ray-project/ray>`_ is used as another source of RL algorithms
 * `Django <https://www.djangoproject.com/>`_ is used to provide the management and elements of the GUI
 * `Cytoscape <https://cytoscape.org/>`_ is used to provide a lightweight and intuitive node editor

How is the YAWNING-TITAN-GUI built
-----------------------------------
**YT-GUI** is designed as an optional extension to the underlying **YT** library.
The Yawning Titan GUI primarily uses Django to convert aspects of **YT** into html objects that can be interacted with
in a local browser instance by the user thereby allowing the underlying python to be executed without need for a command
line interface or knowledge of the python language.

The **YT-GUI** also integrates with a customised version cytoscape JS which has been extended to work directly with **YT**.
This allows for users to directly interface with network topologies and edit the position and attributes of network nodes
that actively updates a database of stored networks.

What does Django provide
---------------------------
* Sidebar navigation allows for quick access to key **YT** features
* database managers allow for efficient and intuitive management of GameMode and Network objects
* multiple window outputs to allow users to easily monitor game loops
* ability to create or edit Network and GameMode objects with real time validation and autosave

What does Cytoscape provide
---------------------------
* create customised network topologies which can be used directly with **YT**
* edit attributes of network nodes

How does the YAWNING-TITAN-GUI integrate with YAWNING-TITAN
-----------------------------------------------------------
* The required inputs for **YT** components are represented as Django form elements which pass data to a class on the back end which process the input and updates the values within the **YT** component.
* Individual requirements of **YT** are split into separate Django view objects which represent all **YT** items for a specific page
* Several components of **YT** are assigned *Manager classes* which extend the **YT** object to provide additional functionality for use in the GUI

Where next?
------------

The best place to start is diving into the :ref:`getting-started`

Cite This Work
--------------


If you would like to include a citation for **YT** in your work, please cite the paper published at the ICML 2022 ML4Cyber Workshop.

.. code:: bibtex

    @inproceedings{inproceedings,
     author = {Andrew, Alex and Spillard, Sam and Collyer, Joshua and Dhir, Neil},
     year = {2022},
     month = {07},
     title = {Developing Optimal Causal Cyber-Defence Agents via Cyber Security Simulation},
     maintitle = {International Confernece on Machine Learning (ICML)},
     booktitle = {Workshop on Machine Learning for Cybersecurity (ML4Cyber)}
    }


.. toctree::
   :maxdepth: 8
   :caption: Contents:

   source/getting_started
   source/create_a_network
   source/db
   source/tutorials
   source/experiments
   GameMode UML <source/game_mode_config_explained>
   Yawning-Titan API <source/_autosummary/yawning_titan>
   Yawning-Titan Tests <source/_autosummary/tests>
   Contribute to YT <source/contributing>
   source/glossary
   source/license
   source/dependencies


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
