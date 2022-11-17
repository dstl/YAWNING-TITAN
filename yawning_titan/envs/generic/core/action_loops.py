"""
The ``ActionLoop`` class helps reduce boilerplate code when evaluating an agent within a target environment.

Serves a similar function to library helpers such as Stable Baselines 3 ``evaluate_policy()".
"""

import os
from datetime import datetime
from uuid import uuid4

import imageio
import matplotlib.pyplot as plt
import pandas as pd

from yawning_titan import APP_IMAGES_DIR, IMAGES_DIR


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

    def gif_action_loop(
        self,
        render_network=True,
        prompt_to_close=False,
        save_gif=False,
        deterministic=True,
        *args,
        **kwargs,
    ):
        """
        Run the agent in evaluation and create a gif from episodes.

        Args:
            render: Bool to toggle rendering on or off. Has a default
                value of True.
            prompt_to_close: Bool to toggle if the output window should
                close immediately on loop ending
            save_gif: Bool to toggle if gif file should be saved to AppData
            deterministic: Bool to toggle if the agents actions should be deterministic
        """
        gif_uuid = str(uuid4())

        complete_results = []
        for i in range(self.episode_count):
            results = pd.DataFrame(
                columns=["action", "rewards", "info"]
            )  # temporary log to satisfy repeatability tests until logging can be full implemented
            obs = self.env.reset()
            done = False
            frame_names = []
            current_image = 0

            while done is False:
                # gets the agents prediction for the best next action to take
                action, _states = self.agent.predict(obs, deterministic=deterministic)

                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                # step the env
                obs, rewards, done, info = self.env.step(action)

                results.loc[len(results.index)] = [action, rewards, info]

                # TODO: setup logging properly here
                # logging.info(f'Observations: {obs.flatten()} Rewards:{rewards} Done:{done}')
                # self.env.render(episode=i+1)

                if save_gif:
                    current_name = os.path.join(
                        APP_IMAGES_DIR, f"{gif_uuid}_{current_image}.png"
                    )
                    current_image += 1
                    frame_names.append(current_name)
                    # save the current image
                    plt.savefig(current_name)

                    current_image += 1
                    frame_names.append(current_name)
                    # save the current image
                    plt.savefig(current_name)

                if render_network:
                    self.env.render(*args, **kwargs)

            if save_gif:
                string_time = datetime.now().strftime("%d%m%Y_%H%M%S")
                gif_path = os.path.join(
                    IMAGES_DIR,
                    f"{self.filename}_{string_time}_{self.episode_count}.gif",
                )
                with imageio.get_writer(gif_path, mode="I") as writer:
                    # create a gif from the images
                    for filename in frame_names:
                        image = imageio.imread(filename)
                        writer.append_data(image)

                    for filename in set(frame_names):
                        os.remove(filename)

            complete_results.append(results)

        if not prompt_to_close:
            self.env.close()
        return complete_results

    def standard_action_loop(self, deterministic=False):
        """Indefinitely act within the environment using a trained agent."""
        complete_results = []
        for i in range(self.episode_count):
            results = pd.DataFrame(
                columns=["action", "rewards", "info"]
            )  # temporary log to satisfy repeatability tests until logging can be full implemented
            obs = self.env.reset()
            done = False
            while not done:
                action, _states = self.agent.predict(obs, deterministic=deterministic)
                # TODO: setup logging properly here
                # logging.info(f'Blue Agent Action: {action}')
                obs, rewards, done, info = self.env.step(action)
                results.loc[len(results.index)] = [action, rewards, info]
            complete_results.append(results)
        return complete_results

    def random_action_loop(self, deterministic=False):
        """Indefinitely act within the environment taking random actions."""
        for i in range(self.episode_count):
            obs = self.env.reset()
            done = False
            reward = 0
            while not done:
                action = self.agent.predict(
                    obs, reward, done, deterministic=deterministic
                )
                ob, reward, done, ep_history = self.env.step(action)
                if done:
                    break
