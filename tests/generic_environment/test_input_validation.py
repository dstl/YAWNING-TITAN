import os

import pytest

from tests import TEST_CONFIG_PATH_OLD


# tests to check invalid config files return errors
def test_input_validation_1(generate_generic_env_test_reqs):
    """Test that incorrect/broken configuration files raise errors."""
    with pytest.raises(ValueError):
        generate_generic_env_test_reqs(
            os.path.join(TEST_CONFIG_PATH_OLD, "red_config_test_broken_1.yaml"),
            n_nodes=23,
            net_creator_type="mesh",
            entry_nodes=["0", "1", "2"],
        )


def test_input_validation_2(generate_generic_env_test_reqs):
    """Test that incorrect/broken configuration files raise errors."""
    with pytest.raises(ValueError):
        generate_generic_env_test_reqs(
            os.path.join(TEST_CONFIG_PATH_OLD, "red_config_test_broken_2.yaml"),
            n_nodes=23,
            net_creator_type="mesh",
            entry_nodes=["0", "1", "2"],
        )


def test_input_validation_3(generate_generic_env_test_reqs):
    """Test that incorrect/broken configuration files raise errors."""
    with pytest.raises(ValueError):
        generate_generic_env_test_reqs(
            os.path.join(TEST_CONFIG_PATH_OLD, "red_config_test_broken_3.yaml"),
            n_nodes=23,
            net_creator_type="mesh",
            entry_nodes=["0", "1", "2"],
        )


def test_input_validation_4(generate_generic_env_test_reqs):
    """Test that incorrect/broken configuration files raise errors."""
    with pytest.warns(UserWarning):
        # error thrown because choose_high_value_nodes_furthest_away_from_entry is True and
        # the high value nodes is manually provided
        generate_generic_env_test_reqs(
            os.path.join(TEST_CONFIG_PATH_OLD, "base_config.yaml"),
            n_nodes=23,
            net_creator_type="mesh",
            high_value_nodes=["0"],
            entry_nodes=["0", "1", "2"],
        )


def test_input_validation_5(generate_generic_env_test_reqs):
    """Test that incorrect/broken configuration files raise errors."""
    with pytest.warns(UserWarning):
        # error thrown because there are more high value nodes than there are nodes in the network
        generate_generic_env_test_reqs(
            os.path.join(TEST_CONFIG_PATH_OLD, "too_many_high_value_nodes.yaml"),
            n_nodes=23,
            net_creator_type="mesh",
            entry_nodes=["0", "1", "2"],
        )
