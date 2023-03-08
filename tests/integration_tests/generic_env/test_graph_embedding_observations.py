import numpy as np
import pytest
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import is_wrapped

from yawning_titan.envs.generic.wrappers.graph_embedding_observations import (
    FeatherGraphEmbedObservation,
)


@pytest.mark.integration_test
@pytest.mark.parametrize(
    ("game_mode_name", "network_name", "n_nodes"),
    [
        ("Default Game Mode", "mesh_18", 18),
        ("red_config_test_2", "mesh_50", 50),
    ],
)
def test_wrapped_env(
    game_mode_name: str, network_name: str, n_nodes: int, create_yawning_titan_run
) -> None:
    """Test that the environment get correctly wrapped with the Feather Observation Wrapper."""
    yt_run = create_yawning_titan_run(game_mode_name, network_name)

    env = FeatherGraphEmbedObservation(yt_run.env, n_nodes)
    assert is_wrapped(env, FeatherGraphEmbedObservation)


@pytest.mark.integration_test
@pytest.mark.parametrize(
    ("game_mode_name", "network_name", "n_nodes"),
    [
        ("Default Game Mode", "mesh_18", 18),
        ("red_config_test_2", "mesh_50", 50),
    ],
)
def test_obs_size(
    game_mode_name: str, network_name: str, n_nodes: int, create_yawning_titan_run
) -> None:
    """Test that the observation size returned by the environment is the correct length."""
    yt_run = create_yawning_titan_run(game_mode_name, network_name)

    env = FeatherGraphEmbedObservation(yt_run.env, n_nodes)
    observation_size = env.calculate_observation_space_size(with_feather=True)

    for i in range(5):
        obs = env.reset()
        assert len(obs) == observation_size


@pytest.mark.integration_test
@pytest.mark.parametrize(
    ("game_mode_name", "network_name", "n_nodes", "num_nodes_check"),
    [
        ("Default Game Mode", "mesh_18", 18, 18),
        ("red_config_test_2", "mesh_50", 50, 52),
    ],
)
def test_obs_range(
    game_mode_name: str,
    network_name: str,
    n_nodes: int,
    num_nodes_check: int,
    create_yawning_titan_run,
):
    """
    Test that each component of the observation space in the environment has the correct length and value range.

    Observation Space is made up of:
        - 500 value graph embedding
        - other features from the env based on input from the settings file
    """
    yt_run = create_yawning_titan_run(game_mode_name, network_name)

    env = FeatherGraphEmbedObservation(yt_run.env, n_nodes)
    for _ in range(5):
        obs = env.reset()
        np.set_printoptions(suppress=True)
        start = 0
        if env.network_interface.game_mode.observation_space.node_connections.value:
            start = 500
            embedding = obs[0:500]

            assert len(embedding) == 500
            assert np.amax(embedding) < 20
            assert np.amin(embedding) > -20

        for j in obs[start:]:
            assert -1 <= j <= 1
        if (
            env.network_interface.game_mode.observation_space.compromised_status.value
            and env.network_interface.game_mode.observation_space.vulnerabilities.value
        ):
            padded_vulns = obs[start + num_nodes_check : (start + num_nodes_check * 2)]
            assert len(padded_vulns) == num_nodes_check
            assert np.amin(padded_vulns) >= -1
            assert np.amax(padded_vulns) <= 1
            padded_compromised = obs[start : start + num_nodes_check]
            assert len(padded_compromised) == num_nodes_check
            for val in padded_compromised:
                assert val in [0, 1, -1]


@pytest.mark.integration_test
def test_env_check(create_yawning_titan_run):
    """Test to Stable Baselines 3 Environment checker compliance once wrapped."""
    yt_run = create_yawning_titan_run("Default Game Mode", "mesh_18")

    check_env(yt_run.env)
