Using the Experiment Runner
============================

.. note::
    The experiment runner is currently not supported and does not work with the ``GenericEnv()``.

YAWNING TITAN comes with a command line interface tool called `experiment_runner.py` which allows new users to begin experimenting with Reinforcement learning approaches in the environments
included. The experiment runner is a way to run some of specific environments such as the 4 node environment ::

    > python3 experiment_runner.py --help

    usage: experiment_runner.py
            --agent {random,all,ppo,a2c,dqn}
            --env {five-node-def-v0,four-node-def-v0,network-graph-explore-v0,18-node-env-v0}
            --training-period TRAINING_PERIOD
            [--help]
            [--action-loop {gif,standard}]
            [--algo-backend {sb3,rllib}]
            [--dl-backend DL_BACKEND]
            [--eval-ep-count EVAL_EP_COUNT]
            [--post-train]
            [--debug]
            [--debug-to-file]
            [--save-agent]
            [--output-raw-metrics]

Arguments:

* ``-h, --help``
    Show this help message and exit

* ``--agent {random,all,ppo,a2c,dqn}, -a {random,all,ppo,a2c,dqn}``
    Which algorithm to use to train an agent

* ``--env {five-node-def-v0,four-node-def-v0,network-graph-explore-v0,18-node-env-v0}, -e {five-node-def-v0,four-node-def-v0,network-graph-explore-v0,18-node-env-v0}``
    Which environment to use

* ``--action-loop {gif,standard}, -l {gif,standard}``
    Which non-training loop to use. Render/Gif output or no output

* ``--training-period TRAINING_PERIOD, -tt TRAINING_PERIOD``
    Length of agent training period

* ``--algo-backend {sb3,rllib}, -ab {sb3,rllib}``
    Which Deep Reinforcement Learning library to use

* ``--dl-backend DL_BACKEND, -db DL_BACKEND``
    Which deep learning backend to use, only important for Ray based experiments

* ``--eval-ep-count EVAL_EP_COUNT, -ec EVAL_EP_COUNT``
    Number of episodes to run post train

* ``--post-train``
    Toggle to run the agent once trained and render if available

* ``--debug``
    Toggle to turn on debugging to the terminal

* ``--debug-to-file``
    Toggle to save debugging info to file

* ``--save-agent``
    Toggle to save the trained agent

* ``--output-raw-metrics``
    Toggle to output raw evaluation metrics alongside summary statistics


An example command might look like this: ::

    python3 experiment_runner.py --agent ppo --env 18-node-env-v0 --training-period 10000

This will begin the training of a Proximal Policy Optimisation agent using the Stable Baselines 3 RL algorithm library within the environment outlined within the papers published by the NSA which can be
found at https://www.nsa.gov.Portals/70/documents/resources/everyone/digital-media-center/publications/the-next-wave/TNW-22-1.pdf#page=9 for a total of 10K training timesteps. Once the training
period has completed, the agent will enter an evaluation phase, run through a specified number of evaluation episodes (defaults to 25) and then output some summary statistics.
