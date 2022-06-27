"""
The ``ActionLoop`` class helps reduce boilerplate code when evaluating an agent within a target environment.

Serves a similar function to library helpers such as Stable Baselines 3 ``evaluate_policy()".
"""
import os
import sys
from pathlib import Path

import imageio
import matplotlib.pyplot as plt


class ActionLoop:
    """A class that represents different post-training action loops for agents."""

    def __init__(self, env, agent, filename=None, episode_count=None):
        """
        Initialise Class.

        Args:
            env: The environment to run through
            agent: The agent to run in the environment
            filename: The save name for the action lop
            episode_count: The number of episodes to go through
        """
        self.env = env
        self.agent = agent
        self.filename = filename
        self.episode_count = episode_count

    def gif_action_loop(self):
        """Run the agent in evaluation and create a gif from episodes."""
        str_path = sys.path[0]
        list_path = str_path.split("/")
        index = len(list_path) - 1 - list_path[::-1].index("yawning-titan")
        new_list = list_path[: index + 1]
        # gets the default settings file path
        image_path_str = "/".join(new_list) + "/yawning_titan/envs/generic/core/images"
        image_path = Path(image_path_str)

        if not image_path.exists():
            # if the path does not exist, create it
            os.mkdir(image_path)

        for i in range(self.episode_count):
            obs = self.env.reset()
            done = False
            frame_names = []
            current_image = 0

            while done is False:
                # gets the agents prediction for the best next action to take
                action, _states = self.agent.predict(obs, deterministic=True)
                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                # step the env
                obs, rewards, done, info = self.env.step(action)

                # TODO: setup logging properly here
                # logging.info(f'Observations: {obs.flatten()} Rewards:{rewards} Done:{done}')
                # self.env.render(episode=i+1)
                self.env.render()

                current_name = f"{image_path_str}/image_{current_image}.png"
                current_image += 1
                frame_names.append(current_name)
                # save the current image
                plt.savefig(current_name)

            with imageio.get_writer(
                self.filename + "_" + str(self.episode_count) + ".gif", mode="I"
            ) as writer:
                # create a gif from the images
                for filename in frame_names:
                    image = imageio.imread(filename)
                    writer.append_data(image)

            for filename in set(frame_names):
                os.remove(filename)

        self.env.close()

    def standard_action_loop(self):
        """Indefintely act within the environment using a trained agent."""
        for i in range(self.episode_count):
            obs = self.env.reset()
            done = False
            while not done:
                action, _states = self.agent.predict(obs)
                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                obs, rewards, done, info = self.env.step(action)

    def random_action_loop(self):
        """Indefintely act within the environment taking random actions."""
        for i in range(self.episode_count):
            obs = self.env.reset()
            done = False
            reward = 0
            while not done:
                action = self.agent.predict(obs, reward, done)
                ob, reward, done, ep_history = self.env.step(action)
                if done:
                    break
