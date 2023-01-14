import copy
import os
from dataclasses import fields
from typing import Any, Dict, Union

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
from yawning_titan_gui.helpers import GameModeManager


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

        super(ConfigForm, self).__init__(
            *args, initial=config_class.to_dict(values_only=True), **kwargs
        )
        # created dropdowns from grouped elements
        self.fields: Dict[str, django_forms.Field] = fields

    def is_valid(self) -> bool:
        """
        Check that config form is valid for fields and subsections.

        Overrides the `django_forms` `is_valid` method to add checks for field values dependent
        on other fields.

        :return: A bool value True if the form meets the validation criteria and produces a valid
            section of the config group.
        """
        v = super().is_valid()

        for k, v in self.cleaned_data.items():
            setattr(self.config_class, k, v)

        self.config_class.validate()
        if self.config_class.validation.passed:
            return True
        else:
            for k, e in self.config_class.get_config_elements(ConfigItem).items():
                for error in e.validation.fail_reasons:
                    self.add_error(k, error)

        self.group_errors = self.config_class.validation.fail_reasons
        self.config_class.validation.log()
        print("ERRORS", self.errors.as_data(), type(self.errors))
        return False


class GameModeSection:
    def __init__(self, section: ConfigGroup, form_name: str, icon: str) -> None:
        self.forms = []
        self.icon = icon
        self.valid = section.validation.passed
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

        self.forms.append(
            ConfigForm(
                config_class=group, fields=field_elements, name=form_name, tier=tier
            )
        )

        for name, e in group.get_config_elements(ConfigGroup).items():
            self.create_form_from_group(e, form_name=name, tier=tier + 1)


# print("TEST",[(form.name,form.tier) for form in GameModeSection(section=Red(),form_name="red").forms])


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

    @staticmethod
    def get_first_section(game_mode: Dict[str, GameModeSection]) -> str:
        """
        Get the first key of the `FormManager.base_forms` dictionary.

        :return: _description_
        """
        return list(game_mode.keys())[0]

    @classmethod
    def get_section(
        cls, game_mode_filename, section_name=None
    ) -> Dict[str, Union[str, ConfigForm]]:
        """
        Get a specific :param:`section` of a form for an active :param:`game_mode_filename`.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section to get from which to retrieve the value of
        :param initial_options: the initial state of the options for the :param:`game_mode_filename`
        :return: a dictionary containing status and :class:`ConfigForm` of the selected :param:`section_name`
        """
        if section_name is None:
            section_name = cls.get_first_section()

        sections = cls.get_or_create_instance(game_mode_filename)

        return sections[section_name]

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
    def check_section_complete(cls, game_mode_filename, section_name) -> bool:
        """
        Check whether a section of the active :param: `game_mode_filename` is complete.

        checks whether the :class:`ConfigForm` representing the :param:`section_name` of the :param:`game_mode_filename` is complete.
        returns True if the form is valid otherwise returns False. Also updates the forms status in :attr: FormManager.forms.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section for which to check the completion state
        :return: a boolean True/False value representing if the :param:`section_name` of the :param:`game_mode_filename` is complete
        """
        section = cls.get_section(game_mode_filename, section_name)
        form: ConfigForm = section["form"]
        if form.is_valid():
            cls.game_modes[game_mode_filename][section_name]["status"] = "complete"
            return True
        cls.game_modes[game_mode_filename][section_name]["status"] = "incomplete"
        return False

    @classmethod
    def check_game_mode_complete(cls, game_mode_filename) -> bool:
        """
        Checks thats all sections of the active :param: `game_mode_filename` have a status of 'complete' in :class: `FormManager.forms`.

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a boolean True/False value representing if the :param:`game_mode_filename` is complete
        """
        if game_mode_filename in cls.game_modes and all(
            cls.check_section_complete(game_mode_filename, section_name)
            for section_name in cls.game_modes[game_mode_filename].keys()
        ):
            GameModeManager.game_modes[game_mode_filename]["complete"] = True
            return True
        return False

    # Setters

    @classmethod
    def update_section_form(
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
        cls.game_modes[game_mode_filename][section_name].forms[
            form_id
        ] = cls.game_modes[game_mode_filename][section_name].forms[form_id](data=data)
        return cls.game_modes[game_mode_filename][section_name]

    @classmethod
    def save_as_game_mode(cls, game_mode_filename: str) -> GameMode:
        """
        Create a complete config yaml file from a dictionary of form sections.

        :param game_mode_forms: dictionary containing django form objects representing sections of the config.

        :return: a valid instance of :class: `~yawning_titan.config.game_config.game_mode_config.GameModeConfig`
        """
        cls.verify(game_mode_filename=game_mode_filename)
        section_configs = {
            section_name.upper(): section["form"].cleaned_data
            for section_name, section in cls.forms[game_mode_filename].items()
        }
        game_mode = GameMode()
        game_mode.set_from_dict(section_configs)
        game_mode.to_yaml(GAME_MODES_DIR / game_mode_filename)
        # del cls.forms[game_mode_filename]
        return game_mode
