import glob
import tempfile
from pathlib import Path

import pytest

from tests.conftest import N_TIME_STEPS
from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.networks.network import Network
from yawning_titan.yawning_titan_run import YawningTitanRun


@pytest.mark.e2e_integration_test
def test_yawning_titan_run_with_corporate_network(corporate_network: Network):
    """Tests YawningTitanRun with the corporate network."""
    yt_run = YawningTitanRun(
        network=corporate_network,
        total_timesteps=N_TIME_STEPS,
        eval_freq=N_TIME_STEPS,
        collect_additional_per_ts_data=True,
        auto=False,
    )

    yt_run.setup()
    yt_run.train()
    yt_run.evaluate()
    loop = ActionLoop(yt_run.env, yt_run.agent, episode_count=1)
    loop.gif_action_loop(save_gif=False, render_network=False)
    assert True


@pytest.mark.e2e_integration_test
def test_rendering_an_action_loop(default_game_mode, default_network):
    """Test that creating a gif action loop correctly produces a .gif file."""
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = Path(tmp_dir.name)

    yt_run = YawningTitanRun(
        game_mode=default_game_mode,
        network=default_network,
        total_timesteps=N_TIME_STEPS,
        eval_freq=N_TIME_STEPS,
        warn=False,
        verbose=0,
    )
    loop = ActionLoop(yt_run.env, yt_run.agent, episode_count=1)
    loop.gif_action_loop(
        save_gif=True,
        render_network=False,
        gif_output_directory=tmp_path,
        webm_output_directory=tmp_path,
    )

    gif_dir = glob.glob(f"{tmp_path}/*.gif")
    webm_dir = glob.glob(f"{tmp_path}/*.webm")

    assert len(gif_dir) == 1
    assert len(webm_dir) == 1
    tmp_dir.cleanup()
