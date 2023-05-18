Welcome to the Yawning-Titan docs!
==================================

.. toctree::
   :maxdepth: 8
   :caption: Contents:
   :hidden:

   source/getting_started
   source/create_a_network
   source/db
   source/tutorials
   source/experiments
   GameMode UML <source/game_mode_config_explained>
   Yawning-Titan CLI <source/yt_cli>
   source/yt_gui
   Yawning-Titan API <source/_autosummary/yawning_titan>
   Yawning-Titan Tests <source/_autosummary/tests>
   Contribute to Yawning-Titan <source/contributing>
   source/glossary
   source/license
   source/dependencies

.. toctree::
   :caption: Project Links:
   :hidden:

   Code <https://github.com/dstl/Yawning-Titan>
   Issues <https://github.com/dstl/Yawning-Titan/issues>
   Pull Requests <https://github.com/dstl/Yawning-Titan/pulls>
   Discussions <https://github.com/dstl/Yawning-Titan/discussions>


What is Yawning-Titan?
----------------------

Yawning-Titan is a collection of abstract, graph based cyber-security simulation environments that supports the training
of intelligent agents for autonomous cyber operations based on OpenAI Gym. Yawning-Titan focuses on providing a fast
simulation to support the development of defensive autonomous agents who face off against probabilistic red agents.

Yawning-Titan contains a small number of specific, self contained OpenAI Gym environments for autonomous cyber defence
research, which are great for learning and debugging, as well as a flexible, highly configurable generic environment
which can be used to represent a range of scenarios of increasing complexity and scale. The generic environment only
needs a network topology and a settings file in order to create an OpenAI Gym compliant environment which also enables
open research and enhanced reproducibility.


How can Yawning-Titan be used?
------------------------------

Yawning-Titan can be used either through the CLI app or vie the GUI. The idea of this is to make Yawning-Titan as
accessible as possible to all users out of the box whilst not compromising the ability for users to make in-depth
modifications to the source code.


Design Principles
-----------------

Yawning-Titan has been designed with the following key principles in mind:
 - Simplicity over complexity
 - Minimal Hardware Requirements
 - Operating System agnostic
 - Support for a wide range of algorithms
 - Enhanced agent/policy evaluation support
 - Flexible environment and game rule configuration


What is Yawning-Titan built with
--------------------------------
Yawning-Titan is built on the shoulders of giants and heavily relies on the following libraries:

 * `OpenAI's Gym <https://gym.openai.com/>`_ is used as the basis for all of the environments
 * `Networkx <https://github.com/networkx/networkx>`_ is used as the underlying data structure used for all environments
 * `Stable Baselines 3 <https://github.com/DLR-RM/stable-baselines3>`_ is used as a source of RL algorithms
 * `Rllib (part of Ray) <https://github.com/ray-project/ray>`_ is used as another source of RL algorithms
 * `Typer <https://github.com/tiangolo/typer>`_ is used to provide a command-line interface
 * `Django <https://github.com/django/django/>`_ is used to provide the management and elements of the GUI
 * `Cytoscape JS <https://github.com/cytoscape/cytoscape.js/>`_ is used to provide a lightweight and intuitive network editor


Yawning-Titan Quick start
-------------------------

.. code:: bash

    pip install <Yawning-Titan .whl file>
    yawning-titan setup
    yawning-titan gui


Where next?
------------

The best place to start is diving into the :ref:`getting-started`, or just straight into the Yawning-Titan GUI <source/yt_gui>.


Cite This Work
--------------


If you would like to include a citation for Yawning-Titan in your work, please cite the paper published at the ICML 2022 ML4Cyber Workshop.

.. code:: bibtex

    @inproceedings{inproceedings,
     author = {Andrew, Alex and Spillard, Sam and Collyer, Joshua and Dhir, Neil},
     year = {2022},
     month = {07},
     title = {Developing Optimal Causal Cyber-Defence Agents via Cyber Security Simulation},
     maintitle = {International Confernece on Machine Learning (ICML)},
     booktitle = {Workshop on Machine Learning for Cybersecurity (ML4Cyber)}
    }
