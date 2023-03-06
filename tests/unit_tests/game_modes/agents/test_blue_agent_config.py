import pytest

from tests.conftest import not_raises
from yawning_titan.exceptions import ConfigGroupValidationError
from yawning_titan.game_modes.components.blue_agent import (
    Blue,
    BlueActionSetGroup,
    BlueIntrusionDiscoveryGroup,
    DeceptiveNodeGroup,
    MakeNodeSafeGroup,
)


@pytest.fixture
def default_blue(default_game_mode) -> Blue:
    """Get blue from default game mode."""
    return default_game_mode.blue


# --- Tier 1 groups ---


@pytest.mark.unit_test
def test_make_node_safe_increase_and_randomise_vulnerability():
    """Tests that making node safe cannot increase and randomise vulnerability."""
    make_node_safe = MakeNodeSafeGroup()

    make_node_safe.increases_vulnerability.value = True
    make_node_safe.gives_random_vulnerability.value = True

    make_node_safe.validate()
    assert not make_node_safe.validation.group_passed

    # assert that the error message is as expected
    assert (
        "Making a node safe cannot simultaneously increase the nodes vulnerability by a set amount and randomly set the vulnerability"
        in make_node_safe.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise make_node_safe.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_no_max_number_deceptive_nodes():
    """Tests using deceptive nodes but there being 0 as the max number."""
    deceptive_nodes = DeceptiveNodeGroup()
    deceptive_nodes.use.value = True
    deceptive_nodes.max_number.value = 0

    deceptive_nodes.validate()
    assert not deceptive_nodes.validation.group_passed

    # assert that the error message is as expected
    assert (
        "if the blue agent can use deceptive nodes then it must be able to create at least 1."
        in deceptive_nodes.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise deceptive_nodes.validation.fail_exceptions[0]


# --- Tier 2 groups ---


@pytest.mark.unit_test
@pytest.mark.parametrize(
    ("reconnect_node", "isolate_node"), ((True, False), (False, True))
)
def test_reconnect_isolate_config(reconnect_node: bool, isolate_node: bool):
    """Tests use isolate node while reconnect node is False."""
    action_set = BlueActionSetGroup()
    action_set.isolate_node.value = isolate_node
    action_set.reconnect_node.value = reconnect_node

    action_set.validate()
    assert not action_set.validation.group_passed

    # assert that the error message is as expected
    assert (
        "Blue should be able to reconnect or isolate nodes if the other is true."
        in action_set.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise action_set.validation.fail_exceptions[0]


@pytest.mark.unit_test
@pytest.mark.parametrize(
    ("on_scan_deceptive_node", "on_scan"), ((0.5, 0.6), (0.5, 0.5))
)
def test_lower_chance_detecting_deceptive_node_intrusion_on_scan_fail(
    on_scan_deceptive_node, on_scan
):
    """Tests a lower detection chance cannot be set for deceptive nodes than standard nodes when network is scanned."""
    intrusion_discovery = BlueIntrusionDiscoveryGroup()

    # check cannot be lower
    intrusion_discovery.on_scan.deceptive_node.value = on_scan_deceptive_node
    intrusion_discovery.on_scan.standard_node.value = on_scan

    intrusion_discovery.validate()
    assert not intrusion_discovery.validation.group_passed

    # assert that the error message is as expected
    assert (
        "there should be a higher chance at detecting intrusions on deceptive nodes than standard nodes."
        in intrusion_discovery.validation.fail_reasons
    )
    with pytest.raises(ConfigGroupValidationError):
        raise intrusion_discovery.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_lower_chance_detecting_deceptive_node_intrusion_on_scan_pass():
    """Tests that the validation passes when detection chances for deceptive and standard nodes are both 1."""
    intrusion_discovery = BlueIntrusionDiscoveryGroup()

    intrusion_discovery.on_scan.deceptive_node.value = 1
    intrusion_discovery.on_scan.standard_node.value = 1

    intrusion_discovery.validate()
    assert intrusion_discovery.validation.passed


# --- Tier 3 groups ---


@pytest.mark.unit_test
def test_using_scan_with_assured_immediate_detection():
    """Tests that if the 'scan' action is used then an intrusion cannot be immediately detected."""
    blue = Blue()

    blue.action_set.scan.value = True
    blue.intrusion_discovery_chance.immediate.standard_node.value = 1

    blue.validate()

    assert not blue.validation.group_passed

    # assert that the error message is as expected
    assert (
        "The scan action is selected yet blue has 100% chance to spot "
        "detections. There is no need for the blue to have the scan "
        "action in this case."
    ) in blue.validation.fail_reasons
    with pytest.raises(ConfigGroupValidationError):
        raise blue.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_not_using_scan_without_assured_immediate_detection():
    """Tests that if the 'scan' action is not used then an intrusion must be immediately detected."""
    blue = Blue()

    blue.action_set.scan.value = False
    blue.intrusion_discovery_chance.immediate.standard_node.value = 0.1

    blue.validate()

    assert not blue.validation.group_passed

    # assert that the error message is as expected
    assert (
        "If the blue agent cannot scan nodes then it should be able to "
        "automatically detect the intrusions."
    ) in blue.validation.fail_reasons
    with pytest.raises(ConfigGroupValidationError):
        raise blue.validation.fail_exceptions[0]


@pytest.mark.unit_test
def test_default_blue_from_legacy(default_blue: Blue, legacy_default_game_mode_dict):
    """Create a blue agent using the default config file."""
    blue = Blue()

    with not_raises(Exception):
        blue.set_from_dict(legacy_default_game_mode_dict["BLUE"], legacy=True)
