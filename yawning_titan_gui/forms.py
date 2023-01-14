import copy
import os
from dataclasses import fields
from typing import Any, Dict, List, Union

import yaml
from django import forms as django_forms
from django.forms import widgets
from yaml import SafeLoader

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.agents.new_blue_agent_config import Blue
from yawning_titan.config.agents.new_red_agent_config import Red
from yawning_titan.config.environment.new_game_rules_config import GameRules
from yawning_titan.config.environment.new_observation_space_config import (
    ObservationSpace,
)
from yawning_titan.config.environment.new_reset_config import Reset
from yawning_titan.config.environment.new_rewards_config import Rewards
from yawning_titan.config.game_config.game_mode import GameMode
from yawning_titan.config.game_config.new_miscellaneous_config import Miscellaneous
from yawning_titan.config.toolbox.core import ConfigGroup, ConfigItem
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem
from yawning_titan.config.toolbox.item_types.float_item import FloatItem
from yawning_titan.config.toolbox.item_types.int_item import IntItem
from yawning_titan.config.toolbox.item_types.str_item import StrItem
from yawning_titan_gui import DEFAULT_GAME_MODE
from yawning_titan_gui.helpers import GameModeManager, next_key


class RangeInput(widgets.NumberInput):
    """Custom widget for range input range input field."""

    input_type = "range"


class ConfigForm(django_forms.Form):
    """
    Base class for represent yawning_titan config classes as html forms.

    - Represent float inputs using range sliders
    - Represent string inputs as text input fields
    - Represent integer inputs as number input fields
    - Represent boolean inputs as styled checkboxes
    - Represent elements that are mutually exclusive as dropdowns

    :param section: The string name of a config section in the Yawning Titan config
    :param ConfigClass: An instance of :class: `~yawning_titan.config.toolbox.core.ConfigGroup` representing a
        section of the Yawning Titan config
    """

    def __init__(
        self,
        name: str,
        tier: int,
        config_class: ConfigGroup,
        fields: Dict[str, django_forms.Field],
        *args,
        **kwargs,
    ):

        self.config_class: ConfigGroup = config_class
        self.group_errors = None
        self.name = name
        self.tier = tier

        super(ConfigForm, self).__init__(*args, **kwargs)
        # created dropdowns from grouped elements
        self.fields: Dict[str, django_forms.Field] = fields
        if self.is_bound:
            self.update_and_check()

    # def update_config_class(self):

    def update_and_check(self) -> bool:
        """
        Check that config form is valid for fields and subsections.

        Overrides the `django_forms` `is_valid` method to add checks for field values dependent
        on other fields.

        :return: A bool value True if the form meets the validation criteria and produces a valid
            section of the config group.
        """
        v = super().is_valid()

        self.config_class.set_from_dict(self.cleaned_data)

        if self.config_class.validation.passed:
            return True
        else:
            for k, v in self.config_class.validation.element_validation.items():
                for error in v.fail_reasons:
                    self.add_error(k, error)

        self.group_errors = self.config_class.validation.fail_reasons
        return False


class GameModeSection:
    def __init__(self, section: ConfigGroup, form_name: str, icon: str) -> None:
        self.forms: List[ConfigForm] = []
        self.form_classes: List[ConfigForm] = []
        self.icon = icon
        self.config_class = section
        self.create_form_from_group(section, form_name=form_name)

    def create_form_from_group(
        self, group: ConfigGroup, form_name: str = "", tier: int = 0
    ):
        field_elements = {}
        for name, e in group.get_config_elements(ConfigItem).items():
            if isinstance(e, BoolItem):
                el = django_forms.BooleanField(
                    widget=widgets.CheckboxInput(
                        attrs={"role": "switch", "class": "form-check-input"}
                    ),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            elif isinstance(e, FloatItem):
                el = django_forms.FloatField(
                    widget=RangeInput(attrs={"class": "form-control", "step": "0.01"}),
                    required=False,
                    help_text=e.doc,
                    min_value=e.properties.min_val,
                    max_value=e.properties.max_val,
                    label=name,
                )
            elif isinstance(e, IntItem):
                el = django_forms.IntegerField(
                    widget=widgets.NumberInput(attrs={"class": "form-control"}),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            else:
                el = django_forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control"}),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            field_elements[name] = el

        class ConfigFormSubsection(ConfigForm):
            def __init__(self, *args, **kwargs):
                # print("INIT SUBSECTION",form_name)
                # TODO: have init auto add config data 'data' to form!!
                super().__init__(
                    form_name, tier, group, field_elements, *args, **kwargs
                )

        self.form_classes.append(ConfigFormSubsection)
        self.forms.append(ConfigFormSubsection(data=group.to_dict(values_only=True)))

        for name, e in group.get_config_elements(ConfigGroup).items():
            self.create_form_from_group(e, form_name=name, tier=tier + 1)

    def get_form_errors(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Create a formatted dictionary of the errors in each of the forms that constitute the game mode section.

        The 'group' errors are the errors for each of the constituent groups in the game mode.
        The 'items' errors are the errors attribute to each item with the group.

        only groups where either group specific errors exist or where an item element within the group has failed
        will be included in the output. This excludes groups that have failed due to a child group failing.

        :return: a dict
        """
        return {
            i: {
                "group": form.config_class.validation.fail_reasons,
                "items": {
                    k: v.fail_reasons
                    for k, v in form.config_class.validation.element_validation.items()
                },
            }
            for i, form in enumerate(self.forms)
            if not form.config_class.validation.group_passed
            or any(
                not item.validation.passed
                for item in form.config_class.get_config_elements(ConfigItem).values()
            )
        }


class GameModeFormManager:
    """
    Create and manage sets of forms for a given :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`.

    allows for game modes to be constructed dynamically from the GUI.
    """

    icons: Dict[str, str] = {
        "red": "bi-lightning",
        "blue": "bi-shield",
        "game_rules": "bi-clipboard",
        "blue_can_observe": "bi-binoculars",
        "rewards": "bi-star",
        "on_reset": "bi-arrow-clockwise",
        "miscellaneous": "bi-brush",
    }
    game_modes: Dict[str, Dict[str, GameModeSection]] = {}

    # Getters

    @staticmethod
    def get_first_section(game_mode_sections: Dict[str, GameModeSection]) -> str:
        """
        Get the first key of the `FormManager.base_forms` dictionary.

        :return: _description_
        """
        return list(game_mode_sections.keys())[0]

    @classmethod
    def get_or_create_instance(cls, game_mode_filename) -> Dict[str, GameModeSection]:
        """
        Get or create the config forms for the current :param:`game_mode_filename`.

        If the game mode is from a saved yaml file set the option values to those set in the file otherwise
        set the options based off the default configuration.

        Set the status of the game mode sections based upon whether they pass the validation rules in their corresponding
        :class: `~yawning_titan.config.game_config.config_abc.ConfigABC`

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a dictionary representation of the sections of the  :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`
        """
        if game_mode_filename in cls.game_modes:
            return cls.game_modes[game_mode_filename]
        else:
            game_mode = GameModeManager.get_game_mode(game_mode_filename)
            sections = {
                k: GameModeSection(v, k, cls.icons[k])
                for k, v in game_mode.get_config_elements(ConfigGroup).items()
            }

            cls.game_modes[game_mode_filename] = sections
            return sections

    @classmethod
    def get_section(
        cls, game_mode_filename, section_name=None
    ) -> Dict[str, GameModeSection]:
        """
        Get a specific :param:`section` of a form for an active :param:`game_mode_filename`.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section to get from which to retrieve the value of
        :return: a dictionary containing status and :class:`ConfigForm` of the selected :param:`section_name`
        """
        game_mode_sections = cls.get_or_create_instance(game_mode_filename)
        if section_name is None:
            section_name = cls.get_first_section(game_mode_sections)

        return game_mode_sections[section_name]

    @classmethod
    def get_next_section_name(cls, game_mode_filename, section_name=None) -> str:
        """
        Get a specific :param:`section` of a form for an active :param:`game_mode_filename`.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section to get from which to retrieve the value of
        :return: a dictionary containing status and :class:`ConfigForm` of the selected :param:`section_name`
        """
        game_mode_sections = cls.get_or_create_instance(game_mode_filename)
        if section_name is None:
            section_name = cls.get_first_section(game_mode_sections)

        return next_key(game_mode_sections, section_name)

    # Checkers

    @classmethod
    def verify(cls, **kwargs):
        """Verify that the lookup keys provided map to a value in :attr: `GameModeFormManager.forms`."""
        if (
            "game_mode_filename" in kwargs
            and kwargs["game_mode_filename"] not in cls.game_modes
        ):
            raise ValueError(f"{kwargs['game_mode_filename']} has not been created")
        if (
            "section_name" in kwargs
            and kwargs["section_name"]
            not in cls.game_modes[kwargs["game_mode_filename"]]
        ):
            raise ValueError(
                f"{kwargs['section_name']} is not in form set for {kwargs['game_mode_filename']}"
            )

    @classmethod
    def check_game_mode_complete(cls, game_mode_filename) -> bool:
        """
        Checks thats all sections of the active :param: `game_mode_filename` have a status of 'complete' in :class: `FormManager.forms`.

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a boolean True/False value representing if the :param:`game_mode_filename` is complete
        """
        if game_mode_filename in cls.game_modes and all(
            section.config_class.validation.passed
            for section in cls.game_modes[game_mode_filename].values()
        ):
            return True
        return False

    # Setters

    @classmethod
    def update_section(
        cls, game_mode_filename: str, section_name: str, form_id: int, data: dict
    ) -> Dict[str, Any]:
        """
        Update the values of a specific :param:`section` of a form for an active :param:`game_mode_filename`.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section for which the values will be updated
        :param data: a dictionary representation of config form values to use to update the reference for an active :param: `game_mode_filename`
        :return: the :param:`section` of the active :param: `game_mode_filename` with values updated from :param:`data`
        """
        # cls.verify(game_mode_filename=game_mode_filename, section_name=section_name)
        section = cls.game_modes[game_mode_filename][section_name]
        section.forms[form_id] = section.form_classes[form_id](data=data)
        section.forms[form_id].update_and_check()
        section.config_class.validate()
        return section

    @classmethod
    def save_as_game_mode(cls, game_mode_filename: str) -> GameMode:
        """
        Create a complete config yaml file from a dictionary of form sections.

        :param game_mode_forms: dictionary containing django form objects representing sections of the config.

        :return: a valid instance of :class: `~yawning_titan.config.game_config.game_mode_config.GameModeConfig`
        """
        game_mode = GameModeManager.get_game_mode(game_mode_filename)
        sections = cls.get_or_create_instance(game_mode_filename)
        for section_name, section in sections.items():
            setattr(game_mode, section_name, section.config_class)
        print("NAME", game_mode_filename)
        import yaml

        print("GM", yaml.dump(game_mode.to_dict(values_only=True)))

        game_mode.to_yaml(GAME_MODES_DIR / game_mode_filename)
        # del cls.sections[game_mode_filename]
        return game_mode
