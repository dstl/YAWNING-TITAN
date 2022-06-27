yawning\_titan.agents package
=============================

This package provides classes that are used to create different
types of blue and red agents. Most of these Classes are only usable with
the :code:`specific` environments and not supported within the :code:`generic` YAWNING TITAN
environment (which is primarily driven by a configuration file). The compatability of agents versus
environments is summarised in the table below.

.. list-table:: Agent Environment Compatibility
    :header-rows: 1
    :widths: 25 20 10 10 35

    * - Agent Name
      - Type
      - :code:`Generic`
      - :code:`Specific`
      - Comments
    * - Keyboard Agent
      - Blue
      - Y
      - N
      -
    * - Simple Blue
      - Blue
      - N
      - Y
      - Used for the five node and four node specific environments
    * - Fixed Red
      - Red
      - N
      - Y
      - Used only for the four node specific environment
    * - NSA Red
      - Red
      - N
      - Y
      - Used for the five node and nsa node def specific environments
    * - Sinewave Red
      - Red
      - Y
      - N
      - Used as the red agent within the Dynamic Casusal Bayesian Optimisation (DCBO) integration
    * - Random
      - Either
      - Y
      - Y
      -

Blue Agents
-------------

yawning\_titan.agents.keyboard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: yawning_titan.agents.keyboard
   :members:
   :undoc-members:
   :show-inheritance:

yawning\_titan.agents.simple\_blue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: yawning_titan.agents.simple_blue
   :members:
   :undoc-members:
   :show-inheritance:

Red Agents
-------------

yawning\_titan.agents.fixed\_red
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: yawning_titan.agents.fixed_red
   :members:
   :undoc-members:
   :show-inheritance:

yawning\_titan.agents.nsa\_red
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: yawning_titan.agents.nsa_red
   :members:
   :undoc-members:
   :show-inheritance:

yawning\_titan.agents.sinewave\_red
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: yawning_titan.agents.sinewave_red
   :members:
   :undoc-members:
   :show-inheritance:



Generic Agents
--------------

yawning\_titan.agents.random
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: yawning_titan.agents.random
   :members:
   :undoc-members:
   :show-inheritance:
