Tutorials
==========

Example notebooks
******************
There are several example notebooks that come with YAWNING-TITAN (**YT**) to demonstrate the correct use of certain
features. The notebooks aim to cover **YT** from end-to-end, step-by-step.

The original versions of these notebooks stored in [`yawning_titan/notebooks/_package_data`](yawning_titan/notebooks/_package_data)
and are copied over to the newly created users notebooks application directory (`~/yawning_titan/notebooks`) at install.
These are the best place to start if you want to get a feel for **YT** before builidng the docs and exploring further.
If the notebooks become corrupted in the users notebooks application directory, they can be reset running the following
commands from an interactive Python session on your venv:
```python
from yawning_titan.notebooks.jupyter import reset_default_jupyter_notebooks
reset_default_jupyter_notebooks(overwrite_existing=True)
```

The supplied notebooks are:

* Creating and playing as a Keyboard Agent.ipynb
    Shows you how to create a Keyboard Agent that will allow you to be able to play the game yourself.
* sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb
    Shows you how to create a custom environment from the very beginning and takes you through all the way
    to training the agent and then rendering its performance at the end.
* sb3/Using an Evaluation Callback to monitor progress during training.ipynb
    Shows you how to create a simple environment and an agent that can give regular updates on its
    performance throughout training.

If you have a Jupyter notebook that you think would make a good edition to the **YT* default notebooks, please submit is
as  feature request by following our [contribution guidelines](
