import tempfile
from pathlib import Path

from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.yawning_titan_run import YawningTitanRun


def test_yawning_titan_run_with_no_args():
    """Tests that actions undertaken by the red agent are repeatable with a set random_seed value."""
    YawningTitanRun(total_timesteps=1000, eval_freq=1000)


def test_rendering_an_action_loop():
    """Test that creating a gif action loop correctly produces a .gif file."""
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = Path(tmp_dir.name)

    yt_run = YawningTitanRun(
        total_timesteps=1000, eval_freq=1000, warn=False, verbose=0
    )
    loop = ActionLoop(yt_run.env, yt_run.agent, episode_count=1)
    loop.gif_action_loop(save_gif=True, render_network=True, output_directory=tmp_path)

    gifs = list(tmp_path.iterdir())
    assert len(gifs) == 1
    assert gifs[-1].suffix == ".gif"
    tmp_dir.cleanup()
