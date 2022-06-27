import gym
import pytest
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp


@pytest.mark.parametrize("n_machines", [10, 50, 16])
def test_n_machines(n_machines: int) -> None:
    """Test environment initialisation with a range of node sizes."""
    env = gym.make("five-node-def-v0", n_machines=n_machines)
    assert env.n_machines == n_machines


@pytest.mark.parametrize(
    (
        "n_machines",
        "attacker_skill",
        "attack_success_threshold",
        "no_compromised_machine_loss",
    ),
    ((10, 60, 0.5, 4), (5, 40, 0.2, 4), (15, 20, 0.9, 3)),
)
def test_environment_init(
    n_machines: int,
    attacker_skill: int,
    attack_success_threshold: float,
    no_compromised_machine_loss: int,
) -> None:
    """
    Test environment creation and value initialisation with a range of values.

    Args:
        n_machines: Number of machines to include within the environment
        attacker_skill: Red Attacker Skill level
        attack_success_threshold: Red Attack Success Threshold
        no_compromised_machine_loss: Number of machines that result in a blue loss
    """
    env = gym.make(
        "five-node-def-v0",
        attacker_skill=attacker_skill,
        n_machines=n_machines,
        attack_success_threshold=attack_success_threshold,
        no_compromised_machine_loss=no_compromised_machine_loss,
    )

    assert env.n_machines == n_machines
    assert env.total_rewards == 0
    assert env.no_compromised_machine_loss == no_compromised_machine_loss
    assert env.no_compromised_machines == 0
    assert env.total_rewards == 0
    assert env.total_no_of_steps == 0
    assert env.done is False

    assert len(env.machine_states) == n_machines
    for entry in env.machine_states:
        assert len(entry) == 2

    assert env.attacker_skill == attacker_skill
    assert env.attack_success_threshold == attack_success_threshold
    assert env.uncompromised_nodes == n_machines
    assert env.compromised_nodes is None


def test_environment_reset() -> None:
    """Test environment reset and value initialisation."""
    env = gym.make("five-node-def-v0")
    agent = PPO(PPOMlp, env, verbose=1)
    agent.learn(total_timesteps=1000)

    env.reset()

    assert env.n_machines == 5
    assert env.total_rewards == 0
    assert env.no_compromised_machine_loss == 4
    assert env.no_compromised_machines == 0
    assert env.total_rewards == 0
    assert env.total_no_of_steps == 0
    assert env.done is False
