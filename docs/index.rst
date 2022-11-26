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

Design Principles
-----------------------

**YT** has been designed with the following key principles in mind:
- Simplicity over complexity
- Minimal Hardware Requirements
- Operating System agnostic
- Support for a wide range of algorithms
- Enhanced agent/policy evaluation support
- Flexible environment and game rule configuration
- Generation of evaluation episode visualisations (gifs)

What is YAWNING-TITAN built with
--------------------------------------
**YT** is built on the shoulders of giants and heavily relies on the following libraries:

 * `OpenAI's Gym <https://gym.openai.com/>`_ is used as the basis for all of the environments
 * `Networkx <https://github.com/networkx/networkx>`_ is used as the underlying data structure used for all environments
 * `Stable Baselines 3 <https://github.com/DLR-RM/stable-baselines3>`_ is used as a source of RL algorithms
 * `Rllib (part of Ray) <https://github.com/ray-project/ray>`_ is used as another source of RL algorithms

Where next?
------------

The best place to start is diving into the :ref:`getting-started`

.. toctree::
   :maxdepth: 8
   :caption: Contents:

   source/getting_started
   source/tutorials
   source/game_mode_config_explained
   source/network_config_explained
   source/experiments
   source/quick_start_experiment_runner
   source/enhancing_yawning_titan
   source/modules
   Yawning-Titan API <source/_autosummary/yawning_titan>
   Yawning-Titan Tests <source/_autosummary/tests>
   Contribute to YT <source/contributing>
   source/glossary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
