import pytest

from yawning_titan.config.toolbox.core import ConfigItem
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.float_item import FloatItem, FloatProperties
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.config.toolbox.item_types.str_item import StrItem, StrProperties
from yawning_titan.exceptions import InvalidPropertyTypeError

InvalidPropertyTypeError

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


@pytest.mark.unit_test
@pytest.mark.parametrize(("item","properties"),(
    (IntItem,BoolProperties),
    (BoolItem,IntProperties),
    (StrItem,FloatProperties),
    (FloatItem,StrProperties)
))
def test_assign_incorrect_properties(item,properties):
    """Test item types raise an :class: `~yawning_titan.exceptions.InvalidPropertyTypeError` error when using incorrect property types."""
    with pytest.raises(InvalidPropertyTypeError):
        item(value=None,properties=properties)


