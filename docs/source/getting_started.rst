.. _getting-started:

Getting Started
===============


Pre-Requisites
**************
To get YAWNING-TITAN (**YT**) installed, you will need to have the following
installed:

Unix
~~~~

* ``python >= 3.8.*, <= 3.10.*``
* ``python3-pip``
* ``virtualenv``

Windows
~~~~

* ``python >= 3.8.*, <= 3.10.*``

**YT** is designed to be OS-agnostic, and thus should work on most
variations/distros of Linux, Windows, and MacOS.

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

1. Navigate to the YAWNING-TITAN folder and create a new python :term:`Virtual Environment` (**venv**)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: unix

   python3 -m venv venv


2. Activate the :term:`venv<Virtual Environment>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Unix**

.. code:: bash

   source venv/bin/activate


**Windows**

.. code:: powershell

   .\venv\Scripts\activate

3. Install :mod:`~yawning_titan` into the :term:`venv<Virtual Environment>` along with all of its dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   python3 -m pip install -e .


This will install all of the dependencies including algorithm libraries. These libraries all use ``torch``. If you’d
like to install ``tensorflow`` for use with Rllib, you can do this manually or install ``tensorflow`` as an optional
dependency by postfixing the command in step 3 above with the ``[tensorflow]`` extra. Example:

.. code:: bash

   python3 -m pip install -e .[tensorflow]

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

To install the development dependencies, postfix the command in step 3
above with the ``[dev]`` extra. Example:

.. code:: bash

   python3 -m pip install -e .[dev]


Starting Yawning-Titan
**********************

The best way to begin working with YT is to run Jupyter Lab from the newly created venv.

**Unix**

.. code:: bash

    cd ~/yawning_titan/notebooks
    jupyter lab

**Windows**

.. code:: powershell

    cd ~\yawning_titan\notebooks
    jupyter lab

Running Yawning-Titan
*********************

From a notebook in Jupyter Lab, import :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` and instantiate it.
This will run the :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` using all default parameters. With
``auto=True``, this will perform the ``.setup()``, ``.train()``, and ``.evaluate()``.

.. code:: python

    from yawning_titan.yawning_titan_run import YawningTitanRun

    yt_run = YawningTitanRun()

The :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` class is fully configurable. Check out the
:class:`~yawning_titan.yawning_titan_run.YawningTitanRun` docs for further customisation.
