.. _getting-started:

Getting Started
===============


Pre-Requisites
**************
To get Yawning-Titan installed, you will need to have the following
installed:

**Unix**

* ``python >= 3.8.*, <= 3.10.*``
* ``python3-pip``
* ``virtualenv``

**Windows**

* ``python >= 3.8.*, <= 3.10.*``

Yawning-Titan is designed to be OS-agnostic, and thus should work on most variations/distros of Linux, Windows, and MacOS.

Environment Setup
*****************

Yawning-Titan operates from the users home directory where it has two locations, one hidden for backend stuff, and one user-facing
for user files. To initialise this environment, run:



.. tabs::

    .. code-tab:: bash
        :caption: Unix

        mkdir ~/yawning_titan
        cd ~/yawning_titan
        python3 -m venv .venv
        source .venv/bin/activate
        pip install <path to downloaded yawningtitan .whl file>

    .. code-tab:: powershell
        :caption: Windows

        mkdir ~\yawning_titan
        cd ~\yawning_titan
        python3 -m venv .venv
        attrib +h .venv /s /d # Hides the .venv directory
        .\.venv\Scripts\activate
        pip install <path to downloaded yawningtitan .whl file>



Starting Yawning-Titan
**********************

The best way to begin working with Yawning-Titan is to run Jupyter Lab from the newly created venv.

**Unix**

.. code:: bash

    cd ~/yawning_titan
    source .venv/bin/activate
    cd ~/yawning_titan/notebooks
    jupyter lab

**Windows**

.. code:: powershell

    cd ~\yawning_titan
    .\.venv\Scripts\activate
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



Development Install
*******************

For those wishing to install Yawning-Titan and use it or extend it from within an IDE, perform the following development installation:

1. Navigate to the Yawning-Titan folder and create a new python :term:`Virtual Environment` (**venv**)
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

3. Install Yawning-Titan into the :term:`venv<Virtual Environment>` along with all of its dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   python3 -m pip install -e .[dev]
