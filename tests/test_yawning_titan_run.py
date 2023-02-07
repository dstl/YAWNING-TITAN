from yawning_titan.yawning_titan_run import YawningTitanRun


def test_yawning_titan_run_with_no_args():
    """Tests that actions undertaken by the red agent are repeatable with a set random_seed value."""
    yt_run = YawningTitanRun(total_timesteps=1000, eval_freq=1000)  # noqa
