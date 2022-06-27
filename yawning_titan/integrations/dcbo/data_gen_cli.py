"""
Data Generation CLI for DCBO.

This file contains a short CLI and the associated code for generating data for downstream training of
Dynamic Casual Bayesian Optimisation (DCBO).
"""

import argparse
import math
import pickle
import random

import numpy as np

from yawning_titan.integrations.dcbo.utils import create_env, init_dcbo_agent

parser = argparse.ArgumentParser()

parser.add_argument(
    "--n_envs",
    default=20,
    help="Number of environments to be used to generate data",
    type=int,
)
parser.add_argument(
    "--max_steps", default=70, help="Max number of steps to collect data for", type=int
)
parser.add_argument(
    "--initial_probabs",
    nargs="*",
    help="The two initial action probabilities",
    type=float,
)
parser.add_argument(
    "-o",
    "--out_name",
    default="yt_data.pkl",
    help="The output file name for the data export",
    type=str,
)

parser.add_argument(
    "--load_and_output",
    action="store_true",
    help="Whether or not to load and print the data generated to terminal",
)
parser.add_argument(
    "--use_standard_net",
    action="store_true",
    help="Whether or not to use the standard DCBO net or generate a random one",
)


args = parser.parse_args()

NUMBER_OF_ENVS = args.n_envs
MAX_STEP = args.max_steps

all_envs = [
    create_env(use_same_net=args.use_standard_net) for i in range(NUMBER_OF_ENVS)
]

agent = init_dcbo_agent(args.initial_probabs)

cost_action_1 = 0.5
cost_action_2 = 3
lookup = {
    "random_move": 0,
    "do_nothing": 1,
    "no_possible_targets": 2,
    "zero_day": 3,
    "basic_attack": 4,
    "spread": 5,
    "intrude": 6,
}

all_data = {"P": [], "V": [], "C": [], "O": []}

for current_env in all_envs:
    current_step = 0
    done = False
    current_var_1 = []
    current_var_2 = []
    current_var_3 = []
    current_var_4 = []
    while current_step < MAX_STEP and not done:
        action = agent.predict(None, 0, done, current_env)
        env_observation, reward, done, notes = current_env.step(action)

        cost = (cost_action_1 * math.floor(agent.probabilities[0])) + (
            cost_action_2 * math.floor(agent.probabilities[1])
        )

        current_var_1.append(agent.probabilities[0])
        current_var_2.append(agent.probabilities[1])
        current_var_3.append(sum(notes["end_state"].values()))
        current_var_4.append(cost + sum(notes["end_state"].values()) ** 1.25)

        a = random.uniform(0, 1)
        b = random.uniform(0, 1)

        agent.update_probabilities([a, b])

        current_step += 1

    all_data["P"].append(current_var_1)
    all_data["V"].append(current_var_2)
    all_data["C"].append(current_var_3)
    all_data["O"].append(current_var_4)

all_data["P"] = np.asarray(all_data["P"], dtype=object)
all_data["V"] = np.asarray(all_data["V"], dtype=object)
all_data["C"] = np.asarray(all_data["C"], dtype=object)
all_data["O"] = np.asarray(all_data["O"], dtype=object)

if args.out_name.endswith(".pkl"):
    with open(args.out_name, "wb") as f:
        pickle.dump(all_data, f)
else:
    print("Filename did not end with .pkl. Adding .pkl to filename...")
    with open(args.out_name + ".pkl", "wb") as f:
        pickle.dump(all_data, f)

if args.load_and_output:
    with open(args.out_name, "rb") as f:
        print(pickle.load(f))
