Tutorials
==========

Example notebooks
******************
There are several example notebooks that come with Yawning-Titan to demonstrate the correct use of certain
features. The notebooks aim to cover Yawning-Titan from end-to-end, step-by-step.

The original versions of these notebooks stored in [`yawning_titan/notebooks/_package_data`](yawning_titan/notebooks/_package_data)
and are copied over to the newly created users notebooks application directory (`~/yawning_titan/notebooks`) at install.
These are the best place to start if you want to get a feel for Yawning-Titan before builidng the docs and exploring further.
If the notebooks become corrupted in the users notebooks application directory, they can be reset running the following
commands from an interactive Python session on your venv:

.. code:: python

    from yawning_titan.notebooks.jupyter import reset_default_jupyter_notebooks
    reset_default_jupyter_notebooks(overwrite_existing=True)

To get started with Notebooks, run Jupyter Lab:

.. code:: bash

    yawning-titan gui


The supplied example notebooks are:

* Create a Network.ipynb
    Demonstrates how to create a Network using the :class:`~yawning_titan.networks.network.Network` and :class:`~yawning_titan.networks.node.Node` classes.
* Creating and playing as a Keyboard Agent.ipynb
    Demonstrates how to create a Keyboard Agent that will allow you to be able to play the game yourself.
* Using YawningTitanRun.ipynb
    Demonstrates how to use the :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` class.
* End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb
    Shows you how to create a custom environment from the very beginning and takes you through all the way
    to training the agent and then rendering its performance at the end.
* Using an Evaluation Callback to monitor progress during training.ipynb
    Shows you how to create a simple environment and an agent that can give regular updates on its
    performance throughout training.
* Using the Network DB.ipynb
    Demonstrates how to use the :class:`~yawning_titan.networks.network_db.NetworkDB` class.
* Using YawningTitanRun.ipynb
    Demonstrates how to use the :class:`~yawning_titan.yawning)titan_run.YawningTitanRun` class.

If you have a Jupyter notebook that you think would make a good edition to the **Yawning-Titan* default notebooks, please submit it
as feature request by following our [contribution guidelines](https://github.com/dstl/Yawning-Titan/blob/main/CONTRIBUTING.md).
