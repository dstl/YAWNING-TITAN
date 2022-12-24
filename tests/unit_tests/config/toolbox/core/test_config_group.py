from pathlib import Path
from typing import Optional

import pytest

from yawning_titan.config.toolbox.core import ConfigGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem
from yawning_titan.config.toolbox.item_types.float_item import FloatItem
from yawning_titan.config.toolbox.item_types.str_item import StrItem


@pytest.fixture
def test_group():
    """A test instance of :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""

    class TestGroup(ConfigGroup):
        def __init__(self, doc: Optional[str] = None):
            self.a: BoolItem = BoolItem(value=False)
            self.b: FloatItem = FloatItem(value=1)
            self.c: StrItem = StrItem(value="test")
            super().__init__(doc)

    return TestGroup()


@pytest.mark.unit_test
def test_to_dict(test_group: ConfigGroup):
    """Test the to_dict method produces a dictionary with the values as set."""
    d = test_group.to_dict(values_only=True)
    assert d == {"a": False, "b": 1, "c": "test"}


@pytest.mark.unit_test
def test_yaml_round_trip(test_group: ConfigGroup, tmp_path: Path):
    """Test that the items can be stored in a yaml file and subsequently reloaded."""
    d1 = test_group.to_dict()

    test_group.to_yaml(tmp_path / "yaml_out.yaml")
    test_group.set_from_yaml(tmp_path / "yaml_out.yaml")

    d2 = test_group.to_dict()

    assert d1 == d2
