from __future__ import annotations

import json
import os.path
import pathlib
import shutil
from datetime import datetime
from logging import Logger, getLogger
from typing import Dict, Final, List, Optional, Union
from uuid import uuid4

import yaml
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from yawning_titan import AGENTS_DIR, PPO_TENSORBOARD_LOGS_DIR
from yawning_titan.agents.fixed_red import FixedRedAgent
from yawning_titan.agents.nsa_red import NSARed
from yawning_titan.agents.simple_blue import SimpleBlue
from yawning_titan.agents.sinewave_red import SineWaveRedAgent
from yawning_titan.config.game_config.game_mode import GameMode
from yawning_titan.config.game_modes import default_game_mode_path
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.exceptions import YawningTitanRunError
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
        game_mode: Optional[GameMode] = None,
        red_agent_class=RedInterface,
        blue_agent_class=BlueInterface,
        print_metrics: bool = False,
        show_metrics_every: int = 1,
        collect_additional_per_ts_data: bool = False,
        eval_freq: int = 10000,
        total_timesteps: int = 200000,
        training_runs: int = 1,
        n_eval_episodes: int = 1,
        deterministic: bool = False,
        warn: bool = True,
        render: bool = False,
        verbose: int = 1,
        logger: Optional[Logger] = None,
        output_dir: Optional[str] = None,
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
        :param training_runs: The number of times the agent is trained.
        :param n_eval_episodes: The number of episodes to evaluate the agent. Default value = 1.
        :param deterministic: Whether the evaluation should use stochastic or deterministic actions. Default value =
            False.
        :param warn: Output additional warnings mainly related to the interaction with stable_baselines if True.
            Default value = True.
        :param render: Renders the environment during evaluation if True. Default value = False.
        :param verbose: Verbosity level: 0 for no output, 1 for info messages (such as device or wrappers used),
            2 for debug messages. Default value = 1.
        :param logger: An optional custom logger to override the use of the default module logger.
        :param output_dir: An optional output path for eval output and saved agent zip file. If none is provided,
            a path is generated using the ``yawning_titan.AGENTS_DIR``, today's date, and the uuid of the instance
            of ``YawningTitanRun``.
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
            self.game_mode: GameMode = game_mode
        else:
            # TODO: Replace with the updated retrieval method from TinyDB once implemented.
            game_mode = GameMode()
            game_mode.set_from_yaml(default_game_mode_path())
            self.game_mode = game_mode

        self._red_agent_class = red_agent_class
        self._blue_agent_class = blue_agent_class

        self.print_metrics = print_metrics
        self.show_metrics_every = show_metrics_every
        self.collect_additional_per_ts_data = collect_additional_per_ts_data
        self.eval_freq = eval_freq
        self.total_timesteps = total_timesteps
        self.training_runs = training_runs
        self.n_eval_episodes = n_eval_episodes
        self.deterministic = deterministic
        self.warn = warn
        self.render = render
        self.verbose = verbose
        self.auto = auto

        self.logger = _LOGGER if logger is None else logger
        self.logger.debug(f"YT run  {self.uuid}: Run initialised")

        self.output_dir = output_dir

        # Automatically setup, train, and evaluate the agent if auto is True.
        if self.auto:
            self.setup()
            self.train()
            self.evaluate()
            self.save()

    def _args_dict(self):
        return {
            "uuid": self.uuid,
            "network": self.network.to_dict(json_serializable=True),
            "game_mode": self.game_mode.to_dict(key_upper=True),
            "red_agent_class": self._red_agent_class.__name__,
            "blue_agent_class": self._blue_agent_class.__name__,
            "print_metrics": self.print_metrics,
            "show_metrics_every": self.show_metrics_every,
            "collect_additional_per_ts_data": self.collect_additional_per_ts_data,
            "eval_freq": self.eval_freq,
            "total_timesteps": self.total_timesteps,
            "training_runs": self.training_runs,
            "n_eval_episodes": self.n_eval_episodes,
            "deterministic": self.deterministic,
            "warn": self.warn,
            "render": self.render,
            "verbose": self.verbose,
            "auto": self.auto,
        }

    def _get_new_ppo(self) -> PPO:
        """Get a new instance of ``stable_baselines.ppo.ppo.PPO``."""
        return PPO(
            PPOMlp,
            self.env,
            verbose=self.verbose,
            tensorboard_log=str(PPO_TENSORBOARD_LOGS_DIR),
            seed=self.env.network_interface.random_seed,
        )

    def _load_existing_ppo(self, ppo_zip_path: str) -> PPO:
        """Load an existing ppo.zip file into ``stable_baselines.ppo.ppo.PPO``."""
        return PPO.load(
            ppo_zip_path,
            self.env,
            verbose=self.verbose,
            tensorboard_log=str(PPO_TENSORBOARD_LOGS_DIR),
            seed=self.env.network_interface.random_seed,
        )

    def setup(self, new: bool = True, ppo_zip_path: Optional[str] = None):
        """
        Performs a setup of the ``NetworkInterface``, ``GenericNetworkEnv``, ``PPO`` algorithm.

        The setup needs to be performed before training can occur.

        :param new: If True, a new instance of PPO is generated. If False, a ppo_zip_path must be passed tooo.
        :param ppo_zip_path: Optional path to a saved ppo.zip file. Required if new = False.

        :raise AttributeError: When new=False and ppo_zip_path hasn't been provided.
        """
        if not new and not ppo_zip_path:
            msg = "Performing setup when new=False requires ppo_zip_path as the path of a saved ppo.zip file."
            try:
                raise AttributeError(msg)
            except AttributeError as e:
                _LOGGER.critical(e)
                raise e

        if self.output_dir:
            if isinstance(self.output_dir, str):
                self.output_dir = pathlib.Path(self.output_dir)
        else:
            self.output_dir = pathlib.Path(
                os.path.join(
                    AGENTS_DIR, "trained", str(datetime.now().date()), f"{self.uuid}"
                )
            )
        self.output_dir.mkdir(parents=True, exist_ok=True)

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
        if new:
            self.agent = self._get_new_ppo()
        else:
            self.agent = self._load_existing_ppo(ppo_zip_path)
        self.logger.debug(f"YT run  {self.uuid}: Agent instantiated")

        self.eval_callback = EvalCallback(
            Monitor(self.env, str(self.output_dir)),
            eval_freq=self.eval_freq,
            deterministic=self.deterministic,
            render=self.render,
            verbose=self.verbose,
        )
        self.logger.debug(f"YT run  {self.uuid}: Eval callback set")

    def train(self) -> Union[PPO, None]:
        """
        Trains the agent.

        :return: The trained instance of ``stable_baselines3.ppo.ppo.PPO``.
        """
        if self.env and self.agent and self.eval_callback:
            self.logger.debug(f"YT run  {self.uuid}: Performing agent training")
            for i in range(self.training_runs):
                self.agent.learn(
                    total_timesteps=self.total_timesteps,
                    n_eval_episodes=self.n_eval_episodes,
                    callback=self.eval_callback,
                )
                self.logger.debug(f"YT run  {self.uuid}: Training run {i + 1} complete")

                self.env.reset()
                self.logger.debug(f"YT run  {self.uuid}: GenericNetworkEnv reset")

            self.logger.debug(f"YT run  {self.uuid}: Agent training complete")
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

    def save(self) -> Union[str, None]:
        """
        Saves the trained agent using the stable_baselines3 save as zip functionality.

        The instance of PPO is saved to ppo.zip.

        The YawningTitanRun args are saved to args.json.

        The YawningTitanRun.uuid is saved to UUID.


        :return: The path the agent has been saved to.
        """
        if self.agent:
            # Save the agent
            agent_path = os.path.join(self.output_dir, "ppo.zip")
            self.agent.save(path=agent_path)

            # Dump the args down to yaml file
            args_path = os.path.join(self.output_dir, "args.json")
            with open(args_path, "w") as file:
                json.dump(self._args_dict(), file, indent=4)

            # Write the UUID file
            uuid_path = os.path.join(self.output_dir, "UUID")
            with open(uuid_path, "w") as file:
                file.write(self.uuid)

            self.logger.debug(
                f"YT run  {self.uuid}: Saved trained agent (Stable Baselines3 PPO) to: {agent_path}"
            )
            return str(agent_path)
        else:
            self.logger.error(
                f"Cannot save the trained agent from YT run  {self.uuid} as the agent has not been "
                f"trained. Call .train() on the instance of {self.__class__.__name__} to train the agent."
            )

    def _build_inventory_file(self):
        # Walk the output_dir to build an inventory file
        inventory_path = os.path.join(self.output_dir, "INVENTORY")
        if os.path.isfile(inventory_path):
            os.remove(inventory_path)
        self.logger.debug(
            f"YT run  {self.uuid}: Building INVENTORY file {inventory_path}."
        )

        with open(inventory_path, "w") as inventory:
            inventory.write("file, ST_SIZE")
            inventory.write("\n")
            for root, dirs, files in os.walk(self.output_dir):
                for file in files:
                    if file != "INVENTORY":
                        file_path = os.path.join(root, file)
                        dir_path = file_path.replace(str(self.output_dir), "")[1:]
                        file_stat = os.stat(file_path)
                        inventory.write(f"{dir_path}, {file_stat.st_size}")
                        inventory.write("\n")
                        self.logger.debug(
                            f"YT run  {self.uuid}: File added to inventory: {dir_path}."
                        )
        self.logger.debug(f"YT run  {self.uuid}: Finished building INVENTORY file.")

    def export(self) -> str:
        """
        Export the YawningTitanRun as a zip.

        The contents of output_dir is archived to the agents_dir exported dir.

        Included is an INVENTORY file that contains all files and their sizes. This is used for file verification when
        an exported YawningTitanRun is imported.

        :return: The exported filepath as a str.
        """
        self.logger.debug(f"YT run  {self.uuid}: Performing export.")
        self.save()

        self._build_inventory_file()

        # Make a zip archive of the output dir
        exported_root = pathlib.Path(os.path.join(AGENTS_DIR, "exported"))
        exported_root.mkdir(parents=True, exist_ok=True)
        export_path = os.path.join(exported_root, f"EXPORTED_YT_RUN_{self.uuid}")
        self.logger.debug(
            f"YT run  {self.uuid}: Making a zip archive of {self.output_dir} and writing to {export_path}."
        )
        shutil.make_archive(export_path, "zip", self.output_dir)
        self.logger.debug(f"YT run  {self.uuid}: Export completed.")
        return export_path

    # TODO: Remove once proper AgentClass sub-classes have been created and mapped as a function in the main module.
    @classmethod
    def _get_agent_class_from_str(cls, agent_class_str):
        """Maps AgentClass string names to their actual class."""
        mapping = {
            "RedInterface": RedInterface,
            "SineWaveRedAgent": SineWaveRedAgent,
            "FixedRedAgent": FixedRedAgent,
            "NSARed": NSARed,
            "BlueInterface": BlueInterface,
            "SimpleBlue": SimpleBlue,
        }
        return mapping[agent_class_str]

    @classmethod
    def _load_args_file(cls, path: str) -> Dict:
        """
        Load an args.json file and returns as a dict.

        :param path: A saved YawningTitanRun path.
        :return: The args.json file as a dict.

        :raise ValueError: When an args.json file doesn't exist in the provided path. Or when it does exist but it's
            keys aren't correct.
        """
        args_path = os.path.join(path, "args.json")
        msg = f"Cannot load trained agent as the args file ({args_path}) "
        if os.path.isfile(args_path):
            with open(args_path, "r") as file:
                args = yaml.safe_load(file)

            if args.keys() == YawningTitanRun(auto=False)._args_dict().keys():
                game_mode = GameMode()
                game_mode.set_from_dict(args["game_mode"])

                network = Network()
                network.set_from_dict(args["network"])

                args["network"] = network
                args["game_mode"] = game_mode
                args["red_agent_class"] = cls._get_agent_class_from_str(
                    args["red_agent_class"]
                )
                args["blue_agent_class"] = cls._get_agent_class_from_str(
                    args["blue_agent_class"]
                )
                return args
            else:
                # Args file keys don't match
                msg = f"{msg} is corrupted."
                _LOGGER.error(msg)
                raise ValueError(msg)
        else:
            # Args file doesn't exist
            msg = f"{msg} does not exist."
            _LOGGER.error(msg)
            raise ValueError(msg)

    @classmethod
    def load(cls, path: str):
        """
        Load and return a saved YawningTitanRun.

        YawningTitanRun's that have auto=True will not be automatically ran on load.

        :param path: A saved YawningTitanRun path.
        :return: An instance of YawningTitanRun.
        """
        args = cls._load_args_file(path)

        uuid = args.pop("uuid")
        args.pop("auto")

        yt_run = YawningTitanRun(**args, auto=False)
        yt_run.uuid = uuid  # We'll allow it here :)
        yt_run.setup(new=False, ppo_zip_path=os.path.join(path, "ppo.zip"))

        return yt_run

    @classmethod
    def _verify_import_export_zip_file(cls, unzip_path) -> bool:
        """
        Verifies an INVENTORY file with the files contained in its parent dir.

        :param unzip_path: An unzipped exported YawningTitanRun path.
        :return: Whether the INVENTORY file matches the files.
        """
        with open(os.path.join(unzip_path, "INVENTORY"), "r") as inventory_file:
            for line in inventory_file.readlines()[1:]:
                line = line.rstrip("\n").split(",")
                print(line)
                file_name, st_size = line[0], int(line[1])
                print(unzip_path, file_name)
                target_file_path = os.path.join(unzip_path, file_name)
                print(target_file_path)
                _LOGGER.debug(f"Attempting to verify file: {target_file_path}")
                if os.path.isfile(target_file_path):
                    file_stat = os.stat(target_file_path)
                    if st_size != file_stat.st_size:
                        # File Size doesn't match
                        _LOGGER.debug(
                            f"   Verification failed, file size {file_stat.st_size} doesn't match {st_size}."
                        )
                        return False
                else:
                    # File doesn't exist
                    _LOGGER.debug("   Verification failed, file doesn't exist.")
                    return False
            _LOGGER.debug("   Verification successful.")
        return True

    @classmethod
    def import_from_export(
        cls, exported_zip_file_path: str, overwrite_existing: bool = False
    ) -> YawningTitanRun:
        """
        Import and return an exported YawningTitanRun.

        YawningTitanRun's that have auto=True will not be automatically ran on import.

        :param exported_zip_file_path: The path of an exported YawningTitanRun.
        :param overwrite_existing: If True, if the uuid of the imported agent already exists in the trainer agents dir
            it is overwritten.
        :return: The imported instance of YawningTitanRun.

        :raise YawningTitanRunError: When the INVENTORY file fails its verification.
        """
        _LOGGER.debug(f"Importing exported agent from {exported_zip_file_path}")
        # Unzip into trained agents folder
        unzip_path = pathlib.Path(
            os.path.join(
                AGENTS_DIR, "trained", str(datetime.now().date()), str(uuid4())
            )
        )
        unzip_path.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(exported_zip_file_path, unzip_path, "zip")

        # Verify the contents
        verified = cls._verify_import_export_zip_file(unzip_path)
        if not verified:
            # TODO: Update the error type raised to a custom type.
            # TODO: Log a critical log message.
            msg = f"Failed to verify the contents while importing YawningTitanRun from {exported_zip_file_path}."
            try:
                raise YawningTitanRunError(msg)
            except YawningTitanRunError as e:
                _LOGGER.critical(e)
                raise e

        # Rename unzip_dir using the UUID
        with open(os.path.join(unzip_path, "UUID")) as file:
            uuid = file.read()
        new_unzip_path = pathlib.Path(
            os.path.join(AGENTS_DIR, "trained", str(datetime.now().date()), uuid)
        )
        if not os.path.isdir(new_unzip_path):
            os.rename(unzip_path, new_unzip_path)
        else:
            # Has already been imported or was created on this machine
            if overwrite_existing:
                # Overwrite
                shutil.rmtree(new_unzip_path)
                os.rename(unzip_path, new_unzip_path)
                _LOGGER.debug(
                    f"Existing YawningTitanRun overwritten at {new_unzip_path}."
                )

        # Pass new_unzip_path to .load and return
        return cls.load(str(new_unzip_path))

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
            f"training_runs={self.training_runs}, "
            f"n_eval_episodes={self.n_eval_episodes}, "
            f"deterministic={self.deterministic}, "
            f"warn={self.warn}, "
            f"render={self.render}, "
            f"verbose={self.verbose}"
            ")"
        )
