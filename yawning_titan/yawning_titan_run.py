import os.path
import pathlib
from datetime import datetime
from logging import Logger, getLogger
from typing import Final, List, Optional, Union
from uuid import uuid4

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan import AGENTS_DIR, PPO_TENSORBOARD_LOGS_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import default_18_node_network

_LOGGER = getLogger(__name__)


class YawningTitanRun:
    """
    The ``YawningTitanRun`` class is the run class for training YT agents from a given set of parameters.

    The ``YawningTitanRun`` class can be used 'straight out of the box', as all params have default values.

    .. code::python

        yt_run = YawningTitanRun()

    The ``YawningTitanRun`` class can also be used manually by setting auto=False.

    .. code::python

        yt_run = YawningTitanRun(auto=False)
        yt_run.setup()
        yt_run.train()
        yt_run.evaluate()

    Trained agents can be saved by calling ``.save()``. If no path is provided, a path is generated using the
    AGENTS_DIR, today's date, and the uuid of the instance of ``YawningTitanRun``.

    .. code::python

        yt_run = YawningTitanRun()
        yt_run.save()

    .. todo::

        - Build a reporting functionality that captures all logs and eval and generates a PDF report.
        - Add multiple training runs functionality for the same agent.
        - Add the ability to load a saved agent and continue training it.
    """

    def __init__(
        self,
        network: Optional[Network] = None,
        game_mode: Optional[GameModeConfig] = None,
        red_agent_class=RedInterface,
        blue_agent_class=BlueInterface,
        print_metrics: bool = False,
        show_metrics_every: int = 1,
        collect_additional_per_ts_data: bool = False,
        eval_freq: int = 10000,
        total_timesteps: int = 200000,
        n_eval_episodes: int = 1,
        deterministic: bool = False,
        warn: bool = True,
        render: bool = False,
        verbose: int = 1,
        logger: Optional[Logger] = None,
        auto: bool = True,
    ):
        """
        The YawningTitanRun constructor.

        # TODO: Add proper Sphinx mapping for classes/methods.

        :param network: An instance of ``Network``.
        :param game_mode: An instance of ``GameModeConfig``.
        :param red_agent_class: The agent/action set class used for the red agent.
        :param blue_agent_class: The agent/action set class used for the blue agent.
        :param print_metrics: Print the metrics if True. Default value = True.
        :param show_metrics_every: Prints the metrics every ``show_metrics_every`` time steps. Default value = 10.
        :param collect_additional_per_ts_data: Collects additional per-timestep data if True.Default value = False.
        :param eval_freq: Evaluate the agent every ``eval_freq`` call of the callback. Default value = 10,000.
        :param total_timesteps: The number of samples (env steps) to train on. Default value = 200000.
        :param n_eval_episodes: The number of episodes to evaluate the agent. Default value = 1.
        :param deterministic: Whether the evaluation should use stochastic or deterministic actions. Default value =
            False.
        :param warn: Output additional warnings mainly related to the interaction with stable_baselines if True.
            Default value = True.
        :param render: Renders the environment during evaluation if True. Default value = False.
        :param verbose: Verbosity level: 0 for no output, 1 for info messages (such as device or wrappers used),
            2 for debug messages. Default value = 1.
        :param logger: An optional custom logger to override the use of the default module logger.
        :param auto: If True, ``setup()``, ``train()``, and ``evaluate()`` are called automatically.
        """
        # Give the run an uuid
        self.uuid: Final[str] = str(uuid4())

        # Initialise required instance variables as None
        self.network_interface: Optional[NetworkInterface] = None
        self.red: Optional[RedInterface] = None
        self.blue: Optional[BlueInterface] = None
        self.env: Optional[GenericNetworkEnv] = None
        self.agent: Optional[PPO] = None
        self.eval_callback: Optional[EvalCallback] = None

        # Set the network using the network arg if one was passed,
        # otherwise use the default 18 node network.
        if network:
            self.network: Network = network
        else:
            self.network = default_18_node_network()

        # Set the game_mode using the game_mode arg if one was passed,
        # otherwise use the game mode
        if game_mode:
            self.game_mode: GameModeConfig = game_mode
        else:
            # TODO: Replace with the updated retrieval method from TinyDB once implemented.
            self.game_mode = GameModeConfig.create_from_yaml(default_game_mode_path())
        self._red_agent_class = red_agent_class
        self._blue_agent_class = blue_agent_class

        self.print_metrics = print_metrics
        self.show_metrics_every = show_metrics_every
        self.collect_additional_per_ts_data = collect_additional_per_ts_data
        self.eval_freq = eval_freq
        self.total_timesteps = total_timesteps
        self.n_eval_episodes = n_eval_episodes
        self.deterministic = deterministic
        self.warn = warn
        self.render = render
        self.verbose = verbose
        self.auto = auto

        self.logger = _LOGGER if logger is None else logger

        self.logger.debug(f"YT run  {self.uuid}: Run initialised")

        # Automatically setup, train, and evaluate the agent if auto is True.
        if self.auto:
            self.setup()
            self.train()
            self.evaluate()

    def setup(self):
        """
        Performs a setup of the ``NetworkInterface``, ``GenericNetworkEnv``, ``PPO`` algorithm.

        The setup needs to be performed before training can occur.
        """
        self.network_interface = NetworkInterface(
            game_mode=self.game_mode, network=self.network
        )
        self.logger.debug(f"YT run  {self.uuid}: Network interface created")

        self.red = self._red_agent_class(self.network_interface)
        self.logger.debug(f"YT run  {self.uuid}: Red agent created")

        self.blue = self._blue_agent_class(self.network_interface)
        self.logger.debug(f"YT run  {self.uuid}: Blue agent created")

        self.env = GenericNetworkEnv(
            red_agent=self.red,
            blue_agent=self.blue,
            network_interface=self.network_interface,
            print_metrics=self.print_metrics,
            show_metrics_every=self.show_metrics_every,
            collect_additional_per_ts_data=self.collect_additional_per_ts_data,
        )
        self.logger.debug(f"YT run  {self.uuid}: GenericNetworkEnv created")

        self.logger.debug(f"YT run  {self.uuid}: Performing env check")
        check_env(self.env, warn=self.warn)
        self.logger.debug(f"YT run  {self.uuid}: Env checking complete")

        self.env.reset()
        self.logger.debug(f"YT run  {self.uuid}: GenericNetworkEnv reset")

        self.logger.debug(f"YT run  {self.uuid}: Instantiating agent")
        self.agent = PPO(
            PPOMlp,
            self.env,
            verbose=self.verbose,
            tensorboard_log=str(PPO_TENSORBOARD_LOGS_DIR),
            seed=self.env.network_interface.random_seed,
        )
        self.logger.debug(f"YT run  {self.uuid}: Agent instantiated")

        self.eval_callback = EvalCallback(
            Monitor(self.env),
            eval_freq=self.eval_freq,
            deterministic=self.deterministic,
            render=self.render,
        )
        self.logger.debug(f"YT run  {self.uuid}: Eva callback set")

    def train(self) -> Union[PPO, None]:
        """
        Trains the agent.

        :return: The trained instance of ``stable_baselines3.ppo.ppo.PPO``.
        """
        if self.env and self.agent and self.eval_callback:
            self.logger.debug(f"YT run  {self.uuid}: Performing agent learning")
            self.agent.learn(
                total_timesteps=self.total_timesteps,
                n_eval_episodes=self.n_eval_episodes,
                callback=self.eval_callback,
            )
            self.logger.debug(f"YT run  {self.uuid}: agent learning complete")
            return self.agent
        else:
            self.logger.error(
                f"Cannot train the agent for YT run  {self.uuid} as the run has not been setup. "
                f"Call .setup() on the instance of {self.__class__.__name__} to setup the run."
            )

    def evaluate(self) -> Union[tuple[float, float], tuple[List[float], List[int]]]:
        """
        Evaluates the trained agent.

        :return: Mean reward per episode, std of reward per episode.
        """
        if self.agent:
            return evaluate_policy(
                self.agent, self.env, n_eval_episodes=self.n_eval_episodes
            )
        else:
            self.logger.error(
                f"Cannot evaluate YT run  {self.uuid} as the agent has not been trained. "
                f"Call .train() on the instance of {self.__class__.__name__} to train the agent."
            )

    def save(self, path: Optional[str] = None) -> Union[str, None]:
        """
        Saves the trained agent using the stable_baselines3 save as zip functionality.

        :param path: An optional target path. If none is provided, a path is generated using the
            ``yawning_titan.AGENTS_DIR``, today's date, and the uuid of the instance of ``YawningTitanRun``.
        :return: The path the agent has been saved to.
        """
        if not path:
            path = pathlib.Path(
                os.path.join(
                    AGENTS_DIR,
                    "trained",
                    str(datetime.now().date()),
                    f"{self.uuid}.zip",
                )
            )
            path.parent.mkdir(parents=True, exist_ok=True)
        if self.agent:
            self.agent.save(path=path)
            self.logger.debug(
                f"YT run  {self.uuid}: Saved trained agent (Stable Baselines3 PPO) to: {path}"
            )
            return str(path)
        else:
            self.logger.error(
                f"Cannot save the trained agent from YT run  {self.uuid} as the agent has not been "
                f"trained. Call .train() on the instance of {self.__class__.__name__} to train the agent."
            )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"uuid='{self.uuid}', "
            f"network={self.network}, "
            f"game_mode={self.game_mode}, "
            f"red_agent_class={self._red_agent_class}, "
            f"blue_agent_class={self._blue_agent_class}, "
            f"print_metrics={self.print_metrics}, "
            f"show_metrics_every={self.show_metrics_every}, "
            f"collect_additional_per_ts_data={self.collect_additional_per_ts_data}, "
            f"eval_freq={self.eval_freq}, "
            f"total_timesteps={self.total_timesteps}, "
            f"n_eval_episodes={self.n_eval_episodes}, "
            f"deterministic={self.deterministic}, "
            f"swarn={self.warn}, "
            f"render={self.render}, "
            f"verbose={self.verbose}"
            ")"
        )
