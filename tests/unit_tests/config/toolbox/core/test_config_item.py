import pytest

from yawning_titan.config.toolbox.core import ConfigItem
from yawning_titan.config.toolbox.item_types.str_item import StrProperties


@pytest.mark.unit_test
def test_to_dict():
    """Test the ConfigItem can represent itself as a dictionary."""
    item = ConfigItem(doc="test", value="test")

    assert item.to_dict() == {"value": "test", "doc": "test"}


@pytest.mark.unit_test
def test_assignment():
    """Test the ConfigItem calls validation on setting the value and that the value is updated."""
    item = ConfigItem(doc="test", value="test", properties=StrProperties())
    item.value = "changed"
    assert item.value == "changed"
    item.value = 1
    assert not item.validation.passed


@pytest.mark.unit_test
def test_set_value():
    """Test the :method: `~yawning_titan.config.toolbox.core.ConfigItem.set_value` method does not validate the item."""
    item = ConfigItem(doc="test", value="test", properties=StrProperties())
    item.set_value(1)
    assert item.validation.passed
    assert item.value == 1
