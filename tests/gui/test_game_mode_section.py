import pytest
from django import forms as django_forms

from tests.conftest import Group, GroupTier2
from yawning_titan_gui.forms.game_mode_forms import GameModeSection


@pytest.mark.gui_test
def test_config_class_instance_persisted(test_group: Group):
    """Test that the same config group instance is referenced throughout the code."""
    section = GameModeSection(test_group, "test")
    section.config_class.a.value = "test"
    assert section.config_class == section.forms[0].config_class


@pytest.mark.gui_test
def test_game_mode_section_single_form(test_group: Group):
    """Test that the config items are correctly converted to django fields when a :class: ~yawning_titan_gui.forms.GameModeSection` is instantiated."""
    section = GameModeSection(test_group, "test")
    fields = {
        "a": django_forms.BooleanField,
        "b": django_forms.IntegerField,
        "c": django_forms.CharField,
    }
    assert all(
        isinstance(field, f)
        for f, field in zip(fields.values(), section.forms[0].fields.values())
    )


@pytest.mark.gui_test
def test_game_mode_section_single_form_errors(test_group: Group):
    """Test that the errors returned from :method: `~yawning_titan_gui.forms.GameModeSection.get_form_errors` are correct and match those of the config class."""
    section = GameModeSection(test_group, "test")
    config_class: Group = section.config_class
    config_class.a.value = "test"
    errors = section.get_form_errors()
    assert errors == {
        0: {
            "group": [],
            "items": {
                "a": ["Value test is of type <class 'str'>, should be <class 'bool'>."],
                "b": [],
                "c": [],
            },
        }
    }
    assert errors[0]["items"]["a"] == config_class.a.validation.fail_reasons


@pytest.mark.gui_test
def test_game_mode_section_only_relevant_errors_returned(
    multi_tier_test_group: GroupTier2,
):
    """Test that only forms with group or item errors directly attributable to that form are returned."""
    section = GameModeSection(multi_tier_test_group, "test")
    config_class: GroupTier2 = section.config_class
    config_class.tier_1.bool.value = True
    config_class.tier_1.float.value = 2
    assert section.get_form_errors() == {
        1: {"group": ["test error tier 1"], "items": {"bool": [], "float": []}}
    }


@pytest.mark.gui_test
def test_game_mode_section_multiple_forms(multi_tier_test_group: GroupTier2):
    """Test that a form is created for each group in a nested set of config groups."""
    section = GameModeSection(multi_tier_test_group, "test")
    field_sets = [
        {"bool": django_forms.BooleanField, "int": django_forms.IntegerField},
        {"bool": django_forms.BooleanField, "float": django_forms.FloatField},
    ]
    assert len(section.forms) == 2
    for form, fields in zip(section.forms, field_sets):
        assert all(
            isinstance(field, f)
            for f, field in zip(fields.values(), form.fields.values())
        )
