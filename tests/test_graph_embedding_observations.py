import os

import numpy as np
import pytest
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import is_wrapped

from tests import TEST_CONFIG_PATH
from tests.test_generic_environment import generate_generic_env_test_reqs
from yawning_titan.config.game_modes import \
    low_skill_red_with_random_infection_perfect_detection_path
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.envs.generic.wrappers.graph_embedding_observations import (
    FeatherGraphEmbedObservation,
)

# Setting up Test Environment
test_1_env = generate_generic_env_test_reqs(
    str(low_skill_red_with_random_infection_perfect_detection_path()),
    net_creator_type="18node",
    n_nodes=18,
)
test_2_env = generate_generic_env_test_reqs(
    os.path.join(TEST_CONFIG_PATH, "red_config_test_1.yaml")
    , n_nodes=50
)

# test 5
test_3_env = generate_generic_env_test_reqs(
    os.path.join(TEST_CONFIG_PATH, "red_config_test_2.yaml"),
    n_nodes=100
)

# test 6
test_4_env = generate_generic_env_test_reqs(
    os.path.join(TEST_CONFIG_PATH, "red_config_test_3.yaml"),
    n_nodes=250
)

test_1_env = FeatherGraphEmbedObservation(test_1_env, max_num_nodes=18)
test_2_env = FeatherGraphEmbedObservation(test_2_env, max_num_nodes=52)
test_3_env = FeatherGraphEmbedObservation(test_3_env, max_num_nodes=100)
test_4_env = FeatherGraphEmbedObservation(test_4_env, max_num_nodes=252)


@pytest.mark.parametrize("env", [test_1_env, test_2_env, test_3_env, test_4_env])
def test_wrapped_env(env: GenericNetworkEnv) -> None:
    """Test that the environment get correctly wrapped with the Feather Observation Wrapper."""
    assert is_wrapped(env, FeatherGraphEmbedObservation)


@pytest.mark.parametrize("env", [test_1_env, test_2_env, test_3_env, test_4_env])
def test_obs_size(env: GenericNetworkEnv) -> None:
    """Test that the observation size returned by the environment is the correct length."""
    observation_size = env.calculate_observation_space_size(with_feather=True)

    for i in range(5):
        obs = env.reset()
        assert len(obs) == observation_size


@pytest.mark.parametrize(
    ("env", "num_of_nodes"),
    [(test_1_env, 18), (test_2_env, 52), (test_3_env, 100), (test_4_env, 252)],
)
def test_obs_range(env: GenericNetworkEnv, num_of_nodes: int) -> None:
    """
    Test that each component of the observation space in the environment has the correct length and value range.

    Observation Space is made up of:
        - 500 value graph embedding
        - other features from the env based on input from the settings file
    """
    for i in range(5):
        obs = env.reset()
        np.set_printoptions(suppress=True)
        start = 0
        if env.network_interface.settings.observation_space.obs_node_connections:
            start = 500
            embedding = obs[0:500]

            assert len(embedding) == 500
            assert np.amax(embedding) < 20
            assert np.amin(embedding) > -20

        for j in obs[start:]:
            assert -1 <= j <= 1
        if (
            env.network_interface.settings.observation_space.obs_compromised_status
            and env.network_interface.settings.observation_space.obs_node_vuln_status
        ):
            padded_vulns = obs[start + num_of_nodes : (start + num_of_nodes * 2)]
            assert len(padded_vulns) == num_of_nodes
            assert np.amin(padded_vulns) >= -1
            assert np.amax(padded_vulns) <= 1
            padded_compromised = obs[start : start + num_of_nodes]
            assert len(padded_compromised) == num_of_nodes
            for val in padded_compromised:
                assert val in [0, 1, -1]


def test_env_check() -> None:
    """Test to Stable Baselines 3 Environment checker compliance once wrapped."""
    check_env(test_1_env)
