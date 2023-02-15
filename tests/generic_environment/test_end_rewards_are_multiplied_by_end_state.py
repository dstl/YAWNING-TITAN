import os

from tests import TEST_CONFIG_PATH_OLD
from tests.conftest import generate_generic_env_test_run
from tests.generic_environment.test_e2e import RandomGen
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv


def test_end_rewards_multiplier(
    generate_generic_env_test_run
):
    env: GenericNetworkEnv = generate_generic_env_test_run(
        os.path.join(TEST_CONFIG_PATH_OLD, "one_step.yaml"), "18node", 18, entry_node_names=["0"]
    )

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
