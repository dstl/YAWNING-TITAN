import tempfile
from pathlib import Path

from yawning_titan.envs.generic.core.action_loops import ActionLoop
from yawning_titan.networks.network import Network
from yawning_titan.yawning_titan_run import YawningTitanRun

N_TIME_STEPS = 1000


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
    loop.gif_action_loop(save_gif=True, render_network=False, output_directory=tmp_path)

    gifs = list(tmp_path.iterdir())
    assert len(gifs) == 1
    assert gifs[-1].suffix == ".gif"
    tmp_dir.cleanup()


def test_yawning_titan_run_with_corporate_network(corporate_network: Network):
    """Test that :class: `~yawning_titan.yawning_titan_run.YawningTitanRun` works as expected."""
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
    loop.gif_action_loop(save_gif=False, render_network=True)
    assert True
