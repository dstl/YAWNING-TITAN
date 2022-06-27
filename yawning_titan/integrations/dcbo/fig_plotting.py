"""
This script creates a plot given two different JSON files.

The JSON files are expected to be JSON exports from Tensorboard.
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

DATA_1 = "../json(6)"
DATA_2 = "../json(5)"
plt.rcParams.update(
    {"text.usetex": True, "font.family": "sans-serif", "font.sans-serif": ["Helvetica"]}
)
# for Palatino and other serif fonts use:
plt.rcParams.update(
    {"text.usetex": True, "font.family": "serif", "font.serif": ["Palatino"]}
)
# It's also possible to use the reduced notation by directly setting font.family:
plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})

sns.set_theme(
    context="paper", style="ticks", palette="deep", font="sans-serif", font_scale=1.3
)


def running_mean(x, N):
    """Calculate a running mean."""
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


# Both of these json files are tensorboard exports of Stable Baseline 3 agents.
if os.path.exists(DATA_1) is False:
    raise ValueError(
        "The tensorboard outputs for plotting need to exported from tensorboard directly"
    )

with open("../json(6)", "r") as f:
    data = json.load(f)[50:]

with open("utils/json(5)", "r") as f:
    eval_data = json.load(f)

x = []
y = []

max_time = 10.73

cur = 0

for i in data:
    x.append(max_time / len(data) * cur)
    y.append(i[2])
    cur += 1

x_e = []
y_e = []

cur = 0

for i in eval_data:
    x_e.append(max_time / len(eval_data) * cur)
    y_e.append(i[2])
    cur += 1


x_rn_m = running_mean(x, 5)

y_rn_m = running_mean(y, 5)

x_e_rn_m = running_mean(x_e, 3)

y_e_rn_m = running_mean(y_e, 3)

# plt.plot(x, y)
plt.plot(x_rn_m, y_rn_m, label="Training", color="blue", alpha=0.5, linewidth=3)
plt.plot(x_e_rn_m, y_e_rn_m, label="Evaluation", color="green", alpha=0.5, linewidth=3)
plt.plot(
    [i for i in range(-5, 15)],
    [-4.9 for i in range(20)],
    ":",
    label="Optimal Reward",
    color="black",
    linewidth=3,
)

plt.xlabel("Relative time (minutes)")
plt.ylabel("Total reward across all timesteps")
# plt.grid()

plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
plt.yticks([10 * i for i in range(-5, 1)])
plt.xlim([0, 11])

ax = plt.gca()

# ax.spines["left"].set_position("zero")
for i in ["top", "bottom", "left", "right"]:
    ax.spines[i].set_color("black")
    ax.spines[i].set_linewidth(1)
# ax.spines["right"].set_color("none")

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.2),
    shadow=True,
    ncol=3,
    fontsize="large",
    frameon=False,
)

fig = plt.gcf()
fig.set_size_inches(6.5, 4)
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)
fig.subplots_adjust(right=0.9)

plt.show()
