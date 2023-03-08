"""Dummy tests for each mark.

This ensures that build pipeline does not fail if there are no tests marked
with a given marker.

If there's a better way of doing this, please implement it :).
"""
import pytest


def test_no_mark():
    """Tests no mark."""
    assert True


@pytest.mark.unit_test()
def test_unit_test():
    """Tests @pytest.mark.unit_test()."""
    assert True


@pytest.mark.integration_test()
def test_integration_test():
    """Tests @pytest.mark.integration_test()."""
    assert True


@pytest.mark.e2e_integration_test()
def test_e2e_integration_test():
    """Tests @pytest.mark.e2e_integration_test()."""
    assert True
