import os

import numpy as np
import pytest
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import is_wrapped

from tests import TEST_CONFIG_PATH
from yawning_titan.config.game_modes import (
    low_skill_red_with_random_infection_perfect_detection_path,
)
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.wrappers.graph_embedding_observations import (
    FeatherGraphEmbedObservation,
)


@pytest.mark.parametrize(
    ("path", "creator_type", "num_nodes"),
    [
        (str(low_skill_red_with_random_infection_perfect_detection_path()), "mesh", 18),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_1.yaml"), "18node", 50),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_2.yaml"), "mesh", 100),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_3.yaml"), "mesh", 250),
    ],
)
def test_wrapped_env(
    generate_generic_env_test_reqs, path: str, creator_type: str, num_nodes: int
) -> None:
    """Test that the environment get correctly wrapped with the Feather Observation Wrapper."""
    env: GenericNetworkEnv = FeatherGraphEmbedObservation(
        generate_generic_env_test_reqs(
            path, creator_type, num_nodes, entry_nodes=["0", "1", "2"]
        ),
        num_nodes,
    )
    assert is_wrapped(env, FeatherGraphEmbedObservation)


@pytest.mark.parametrize(
    ("path", "creator_type", "num_nodes"),
    [
        (str(low_skill_red_with_random_infection_perfect_detection_path()), "mesh", 18),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_1.yaml"), "18node", 50),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_2.yaml"), "mesh", 100),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_3.yaml"), "mesh", 250),
    ],
)
def test_obs_size(
    generate_generic_env_test_reqs, path: str, creator_type: str, num_nodes: int
) -> None:
    """Test that the observation size returned by the environment is the correct length."""
    env: GenericNetworkEnv = FeatherGraphEmbedObservation(
        generate_generic_env_test_reqs(
            path, creator_type, num_nodes, entry_nodes=["0", "1", "2"]
        ),
        num_nodes,
    )
    observation_size = env.calculate_observation_space_size(with_feather=True)

    for i in range(5):
        obs = env.reset()
        assert len(obs) == observation_size


@pytest.mark.parametrize(
    ("path", "creator_type", "num_nodes", "num_nodes_check"),
    [
        (
            str(low_skill_red_with_random_infection_perfect_detection_path()),
            "mesh",
            18,
            18,
        ),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_1.yaml"), "18node", 50, 52),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_2.yaml"), "mesh", 100, 100),
        (os.path.join(TEST_CONFIG_PATH, "red_config_test_3.yaml"), "mesh", 250, 252),
    ],
)
def test_obs_range(
    generate_generic_env_test_reqs,
    path: str,
    creator_type: str,
    num_nodes: int,
    num_nodes_check: int,
) -> None:
    """
    Test that each component of the observation space in the environment has the correct length and value range.

    Observation Space is made up of:
        - 500 value graph embedding
        - other features from the env based on input from the settings file
    """
    env: GenericNetworkEnv = FeatherGraphEmbedObservation(
        generate_generic_env_test_reqs(
            path, creator_type, num_nodes, entry_nodes=["0", "1", "2"]
        ),
        num_nodes,
    )
    for i in range(5):
        obs = env.reset()
        np.set_printoptions(suppress=True)
        start = 0
        if env.network_interface.game_mode.observation_space.node_connections:
            start = 500
            embedding = obs[0:500]

            assert len(embedding) == 500
            assert np.amax(embedding) < 20
            assert np.amin(embedding) > -20

        for j in obs[start:]:
            assert -1 <= j <= 1
        if (
            env.network_interface.game_mode.observation_space.compromised_status
            and env.network_interface.game_mode.observation_space.vulnerabilities
        ):
            padded_vulns = obs[start + num_nodes_check : (start + num_nodes_check * 2)]
            assert len(padded_vulns) == num_nodes_check
            assert np.amin(padded_vulns) >= -1
            assert np.amax(padded_vulns) <= 1
            padded_compromised = obs[start : start + num_nodes_check]
            assert len(padded_compromised) == num_nodes_check
            for val in padded_compromised:
                assert val in [0, 1, -1]


def test_env_check(generate_generic_env_test_reqs) -> None:
    """Test to Stable Baselines 3 Environment checker compliance once wrapped."""
    check_env(
        generate_generic_env_test_reqs(
            str(low_skill_red_with_random_infection_perfect_detection_path()),
            "mesh",
            18,
            entry_nodes=["0", "1", "2"],
        )
    )
