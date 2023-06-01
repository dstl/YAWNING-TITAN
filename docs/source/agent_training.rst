**************
Agent Training
**************

YawningTitanRun class
#####################

The easiest way to train an agent is to use the :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` class.

.. code:: python

    from yawning_titan.yawning_titan_run import YawningTitanRun

    yt_run = YawningTitanRun()

Configurable Param:

- network - An instance of :class:`~yawning_titan.networks.network.Network`.

- game_mode - An instance of :class:`~yawning_titan.game_modes.game_mode.GameMode`.

- red_agent_class - The agent/action set class used for the red agent.

- blue_agent_class - The agent/action set class used for the blue agent.

- print_metrics - Print the metrics if True. Default value = True.

- show_metrics_every - Prints the metrics every show_metrics_every time steps. Default value = 10.

- collect_additional_per_ts_data - Collects additional per-timestep data if True.Default value = False.

- eval_freq - Evaluate the agent every eval_freq call of the callback. Default value = 10,000.

- total_timesteps - The number of samples (env steps) to train on. Default value = 200000.

- training_runs - The number of times the agent is trained.

- n_eval_episodes - The number of episodes to evaluate the agent. Default value = 1.

- deterministic - Whether the evaluation should use stochastic or deterministic actions. Default value = False.

- warn - Output additional warnings mainly related to the interaction with stable_baselines if True. Default value = True.

- render - Renders the environment during evaluation if True. Default value = False.

- verbose - Verbosity level: 0 for no output, 1 for info messages (such as device or wrappers used), 2 for debug messages. Default value = 1.

- logger - An optional custom logger to override the use of the default module logger.

- output_dir - An optional output path for eval output and saved agent zip file. If none is provided, a path is generated using the yawning_titan.AGENTS_DIR, today’s date, and the uuid of the instance of YawningTitanRun.

- auto - If True, setup(), train(), and evaluate() are called automatically.


Import a trained Agent
######################


From Exported YawningTitanRun
*****************************

If you have a .zip file that was generated using the YawningtitanRun class, it can be imported into your Yawning-Titan
environment by using the :func:`~yawning_titan.yawning_titan_run.YawningTitanRun.import_from_export` function:

.. code:: python

    from yawning_titan.yawning_titan_run import YawningTitanRun

    yt_run = YawningTitanRun.import_from_export(
        exported_zip_file_path=<path to your .zip file>
    )

    # From here you can continue training the Agent and/or evaluate the Agent
    yt_run.train()
    yt_run.evaluate()

From Externally Trained SB3 PPO
*******************************

.. note:: This feature is not yet available, but is planned for a future release.

Training Evaluation
###################

When an agent is trained and saved using the :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` class,
two things happen:

1. Subdirectory is created at ``~/yawning_titan/agents/trained/<YYYY-MM-DD>/<UUID>/`` where the saved ``PPO.zip`` is stored
along with the ``UUID`` file, the ``args.json`` file, and a ``monitor.zip`` file.

2. Tensorboard logs are captured at ``~/yawning_titan/agents/logs/PPO_<n>/``

To view the tensorboard metrics in Tensorboard, run:

.. code:: bash

    tensorboard ~/yawning_titan/agents/logs/

.. note:: Using Tensorboard

    To make full use of tensorboard, install Yawning-Titan with the tensorflow extra.


.. warning:: Future Development

    - Currently the tensorboard logs aren't associated the Agent UUID, this will be fixed in a future release.

    - The monitor.csv output isn't being logged to correctly. Future release will see the output of appropriate training and evaluation metrics.
