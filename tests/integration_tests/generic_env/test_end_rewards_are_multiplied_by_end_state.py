import pytest

from tests.e2e_integration_tests.test_generic_env_e2e import RandomGen


@pytest.mark.integration_test
def test_end_rewards_multiplier(create_yawning_titan_run):
    yt_run = create_yawning_titan_run(
        game_mode_name="one_step",
        network_name="18node_18"
    )
    env = yt_run.env

    env.reset()

    # perform step
    env.step(
        RandomGen(env.BLUE.get_number_of_actions()).get_action()
    )

    # check reward
    """
    Grace period is equal to max steps which means red should have no action
    and that the current reward should be rewards_for_reaching_max_steps
    """
    assert round(env.current_reward, 2) == 100

    env.close()
