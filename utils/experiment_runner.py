import argparse
import logging
import sys
import time
import uuid

import ray
from ray import tune
from ray.tune.registry import register_env

from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.envs.specific import FourNodeDef
from yawning_titan.experiment_helpers.constants import (
    SB3_ALL_AGENTS,
    SB3_ALL_AGENTS_DICT,
)
from yawning_titan.experiment_helpers.sb3 import (
    init_env,
    print_policy_eval_metrics,
    train_and_eval,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helps run experiments!")

    parser.add_argument(
        "--agent",
        "-a",
        choices=["random", "all"] + SB3_ALL_AGENTS,
        required=True,
        help="Which algorithm to use to train an agent",
    )
    parser.add_argument(
        "--env",
        "-e",
        choices=[
            "five-node-def-v0",
            "four-node-def-v0",
            "network-graph-explore-v0",
            "18-node-env-v0",
        ],
        required=True,
        help="Which environment to use",
    )
    # TODO: Look at simplyfing this. Something like render or no render
    parser.add_argument(
        "--action-loop",
        "-l",
        choices=["gif", "standard"],
        default="standard",
        help="Which non-training loop to use. Render/Gif output or no output",
    )
    """
        '--training-period' - Need to look at how to make this make more sense. There are differences between Stable Baselines 3 and Rllib that make this annoying.
        Stable Baselines 3 use timesteps to determine training length. Ray's Rllib on the other hand uses number of training episodes to determine
        training legnths.

        This means that using 10000 as an input gives two widely different results. Sb3 would do 10,000 timesteps which is not alot but
        Rllib would do 10,000 each of which could be up to the terminal state of the environment.
    """
    parser.add_argument(
        "--training-period",
        "-tt",
        type=int,
        required=True,
        help="Length of agent training period",
    )
    parser.add_argument(
        "--algo-backend",
        "-ab",
        default="sb3",
        choices=["sb3", "rllib"],
        type=str,
        help="Which Deep Reinforcement Learning library to use",
    )
    parser.add_argument(
        "--dl-backend",
        "-db",
        default="torch",
        type=str,
        help="Which deep learning backend to use, only important for Ray based experiments",
    )

    parser.add_argument(
        "--eval-ep-count",
        "-ec",
        default=25,
        type=int,
        required=False,
        help="Number of episodes to run post train",
    )
    parser.add_argument(
        "--post-train",
        action="store_true",
        default=False,
        help="Toggle to run the agent once trained and render if available",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Toggle to turn on debugging to the terminal",
    )
    parser.add_argument(
        "--debug-to-file",
        action="store_true",
        help="Toggle to save debugging info to file",
    )
    parser.add_argument(
        "--save-agent", action="store_true", help="Toggle to save the trained agent"
    )
    parser.add_argument(
        "--output-raw-metrics",
        action="store_true",
        required=False,
        help="Toggle to output raw evaluation metrics alongside summary statistics",
    )

    args = parser.parse_args()
    experiment_id = str(uuid.uuid4())

    logger = logging.getLogger(__name__)

    if args.debug is True:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(stream=sys.stdout)

    if args.debug_to_file is True:
        logging.basicConfig(filename=f"./logs/debug_{experiment_id}.log")

    logger.debug(
        f"Experiment Args {args.agent} {args.env} {args.action_loop} {args.eval_ep_count} {args.training_period}"
    )

    if args.algo_backend == "sb3":

        env = init_env(args.env, experiment_id)

        # Initialising Agents
        # ----------------------------------
        agents = []
        evals = []
        if args.agent == "all":
            for i in SB3_ALL_AGENTS:
                agent, eval = train_and_eval(
                    i, env, args.training_period, args.eval_ep_count
                )
                agents.append(agent)
                evals.append(eval)
        else:
            agent, eval = train_and_eval(
                args.agent, env, args.training_period, args.eval_ep_count
            )
            agents.append(agent)
            evals.append(eval)

        print_policy_eval_metrics(SB3_ALL_AGENTS_DICT, evals)

        logger.debug("Policy Evaulated")

        if args.save_agent:
            for i in range(len(agents)):
                filename = f"{SB3_ALL_AGENTS_DICT[i]}_{args.env}_{round(time.time())}"
                agent.save(f"./logs/agents/{filename}")

    if args.algo_backend == "rllib":

        training_env = "four-node-def-v0"
        register_env(training_env, lambda config: FourNodeDef())

        ray.init()
        tune.run(
            "PPO",
            stop={"episode_reward_mean": 200},
            config={"env": "four-node-def-v0", "num_gpus": 0, "num_workers": 1},
        )

        # raise NotImplementedError("Rllib Backend currently in development")

    # Agent Action Loops
    # ----------------------------------
    if args.post_train:
        reward = 0
        done = False
        if args.action_loop == "gif":
            if args.agent == "random":
                raise NotImplementedError(
                    "The gif action loop is not supported for a random agent"
                )

            logger.debug("Entering GIF Action Loop")
            for i in range(len(agents)):
                filename = f"{SB3_ALL_AGENTS_DICT[i]}_{args.env}_{round(time.time())}"
                loop = ActionLoop(
                    env, agents[i], filename, episode_count=args.eval_ep_count
                )
                loop.gif_action_loop()

        elif args.action_loop == "standard":
            if args.agent == "random":
                for i in range(len(agents)):
                    logger.debug(f"Entering Action Loop for {SB3_ALL_AGENTS_DICT[i]}")
                    loop = ActionLoop(env, agents[i], episode_count=args.eval_ep_count)
                    loop.random_action_loop()
            else:
                for i in range(len(agents)):
                    logger.debug(f"Entering Action Loop for {SB3_ALL_AGENTS_DICT[i]}")
                    loop = ActionLoop(env, agents[i], episode_count=args.eval_ep_count)
                    loop.standard_action_loop()

        env.close()

    env.close()
