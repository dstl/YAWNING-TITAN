import copy
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
        section: str,
        ConfigClass: ConfigGroup,
        *args,
        **kwargs,
    ):

        self.config_class: ConfigGroup = ConfigClass
        self.section = section
        self.group_errors = None

        fields, self.field_item_map = self.config_items_to_fields(self.config_class)

        initial = {}
        for k, e in self.field_item_map.items():
            initial[k] = e.value

        super(ConfigForm, self).__init__(*args, initial=initial, **kwargs)

        # created dropdowns from grouped elements
        self.fields: Dict[str, django_forms.Field] = fields
        self.titles = self.add_titles_to_fields(self.fields)

    def update_config_values(self, data: dict) -> bool:
        """
        update the values of the :attribute: `ConfigClass`.

        :param data: the key value pairs representing each config item.
        """
        for k, v in data.items():
            self.field_item_map[k].value = v

    def is_valid(self) -> bool:
        """
        Check that config form is valid for fields and subsections.

        Overrides the `django_forms` `is_valid` method to add checks for field values dependent
        on other fields.

        :return: A bool value True if the form meets the validation criteria and produces a valid
            section of the config group.
        """
        v = super().is_valid()
        print("test", v)
        self.update_config_values(self.cleaned_data)
        self.config_class.validate()
        if self.config_class.validation.passed:
            return True
        else:
            for k, e in self.field_item_map.items():
                for error in e.validation.fail_reasons:
                    self.add_error(k, error)
        self.config_class.validation.log()
        print("ERRORS", self.errors.as_data(), type(self.errors))
        return False

    def config_items_to_fields(
        self,
        config: ConfigGroup = None,
        field_elements: Dict[str, django_forms.Field] = None,
        field_item_map: Dict[str, ConfigItem] = None,
        prefix: str = "",
        tier=0,
    ):
        """"""
        if field_elements is None:
            field_elements = {}
        if field_item_map is None:
            field_item_map = {}

        for name, e in config.get_config_elements(ConfigItem).items():
            if isinstance(e, BoolItem):
                el = django_forms.BooleanField(
                    widget=widgets.CheckboxInput(
                        attrs={
                            "role": "switch",
                            "class": f"form-check-input tier-{tier}",
                        }
                    ),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            elif isinstance(e, FloatItem):
                el = django_forms.FloatField(
                    widget=RangeInput(
                        attrs={"class": f"form-control tier-{tier}", "step": "0.01"}
                    ),
                    required=False,
                    help_text=e.doc,
                    min_value=e.properties.min_val,
                    max_value=e.properties.max_val,
                    label=name,
                )
            elif isinstance(e, IntItem):
                el = django_forms.IntegerField(
                    widget=widgets.NumberInput(
                        attrs={"class": f"form-control tier-{tier}"}
                    ),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            else:
                el = django_forms.CharField(
                    widget=widgets.TextInput(
                        attrs={"class": f"form-control tier-{tier}"}
                    ),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )

            field_elements[f"{prefix}__{name}"] = el
            field_item_map[f"{prefix}__{name}"] = e

        for name, e in config.get_config_elements(ConfigGroup).items():
            _field_elements, _field_item_map = self.config_items_to_fields(
                e, field_elements, prefix=f"{prefix}__{name}", tier=tier + 1
            )
            field_elements.update(_field_elements)
            field_item_map.update(_field_item_map)
        return field_elements, field_item_map

    def add_titles_to_fields(self, field_dict: Dict[str, django_forms.Field]) -> dict:
        """"""
        used_titles = []
        titles_dict = {}
        for k in field_dict.keys():
            titles = titles = [t for t in k.split("__")[:-1] if t != ""]

            found = []
            for t in used_titles:
                n = min(len(t), len(titles))
                if t[:n] == titles[:n]:
                    found = titles[:n]
                    break

            if found != titles and titles not in used_titles:
                used_titles.append(titles)
                titles_dict[k] = [
                    {"text": t, "tier": i}
                    for i, t in enumerate(titles)
                    if t not in found
                ]

            for n in range(len(titles) - 1):
                if titles[: n + 1] and titles[:n] not in used_titles:
                    used_titles.append(titles[: n + 1])

        return titles_dict


class RedAgentForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.agents.red_agent_config.RedAgentConfig` as html form."""

    def __init__(self, ConfigClass: Red = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = Red()
        super().__init__("red", ConfigClass, *args, **kwargs)


class BlueAgentForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.agents.blue_agent_config.BlueAgentConfig` as html form."""

    def __init__(self, ConfigClass: Blue = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = Blue()
        super().__init__("blue", ConfigClass, *args, **kwargs)


class ObservationSpaceForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.observation_space_config.ObservationSpaceConfig` as html form."""

    def __init__(self, ConfigClass: ObservationSpace = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = ObservationSpace()
        super().__init__("blue_can_observe", ConfigClass, *args, **kwargs)


class ResetForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.reset_config.ResetConfig` as html form."""

    def __init__(self, ConfigClass: Reset = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = Reset()
        super().__init__("on_reset", ConfigClass, *args, **kwargs)


class RewardsForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.rewards_config.RewardsConfig` as html form."""

    def __init__(self, ConfigClass: Rewards = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = Rewards()
        super().__init__("rewards", ConfigClass, *args, **kwargs)


class GameRulesForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.game_rules_config.GameRulesConfig` as html form."""

    def __init__(self, ConfigClass: GameRules = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = GameRules()
        super().__init__("game_rules", ConfigClass, *args, **kwargs)


class MiscellaneousForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.game_config.miscellaneous_config.MiscellaneousConfig` as html form."""

    def __init__(self, ConfigClass: Miscellaneous = None, *args, **kwargs):
        if ConfigClass is None:
            ConfigClass = Miscellaneous()
        super().__init__("miscellaneous", ConfigClass, *args, **kwargs)


def create_game_mode_from_form_sections(
    game_mode_forms: Dict[str, django_forms.Form], game_mode_filename: str
):
    """
    Create a complete config yaml file from a dictionary of form sections.

    :param game_mode_forms: dictionary containing django form objects representing sections of the config.

    :return: a valid instance of :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`
    """
    section_configs = {
        section_name.upper(): form.cleaned_data
        for section_name, form in game_mode_forms.items()
    }
    game_mode = GameMode()
    game_mode.set_from_dict(section_configs)
    game_mode.to_yaml(GAME_MODES_DIR / game_mode_filename)
    return game_mode


class GameModeFormManager:
    """
    Create and manage sets of forms for a given :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`.

    allows for game modes to be constructed dynamically from the GUI.
    """

    base_forms: Dict[str, Dict[str, Union[str, ConfigForm]]] = {
        "red": {
            "form": RedAgentForm,
            "icon": "bi-lightning",
        },
        "blue": {
            "form": BlueAgentForm,
            "icon": "bi-shield",
        },
        "game_rules": {
            "form": GameRulesForm,
            "icon": "bi-clipboard",
        },
        "blue_can_observe": {
            "form": ObservationSpaceForm,
            "icon": "bi-binoculars",
        },
        "rewards": {"form": RewardsForm, "icon": "bi-star"},
        "on_reset": {
            "form": ResetForm,
            "icon": "bi-arrow-clockwise",
        },
        "miscellaneous": {
            "form": MiscellaneousForm,
            "icon": "bi-brush",
        },
    }
    forms: Dict[str, Dict[str, Dict[str, Any]]] = {}

    # Getters

    @classmethod
    def get_or_create_instance(
        cls, game_mode_filename
    ) -> Dict[str, Dict[str, Union[str, ConfigForm]]]:
        """
        Get or create the config forms for the current :param:`game_mode_filename`.

        If the game mode is from a saved yaml file set the option values to those set in the file otherwise
        set the options based off the default configuration.

        Set the status of the game mode sections based upon whether they pass the validation rules in their corresponding
        :class: `~yawning_titan.config.game_config.config_abc.ConfigABC`

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a dictionary representation of the sections of the  :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`
        """
        if game_mode_filename in cls.forms:
            return cls.forms[game_mode_filename]
        else:
            forms = copy.deepcopy(cls.base_forms)
            game_mode = GameModeManager.get_game_mode(game_mode_filename)

            for section_name, section in forms.items():
                form: ConfigForm = section["form"](
                    ConfigClass=game_mode.get_config_elements(ConfigGroup).get(
                        section_name
                    )
                )
                section.update(
                    {
                        "form": form,
                        "status": "complete"
                        if game_mode.validation.passed
                        else "incomplete",
                    }
                )

            cls.forms[game_mode_filename] = forms
            print("GET or create", cls.forms.keys())
            return forms

    @classmethod
    def get_first_section(cls) -> str:
        """
        Get the first key of the `FormManager.base_forms` dictionary.

        :return: _description_
        """
        return list(cls.base_forms.keys())[0]

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

        forms = cls.get_or_create_instance(game_mode_filename)

        return forms[section_name]

    # Checkers

    @classmethod
    def verify(cls, **kwargs):
        """Verify that the lookup keys provided map to a value in :attr: `GameModeFormManager.forms`."""
        if (
            "game_mode_filename" in kwargs
            and kwargs["game_mode_filename"] not in cls.forms
        ):
            raise ValueError(f"{kwargs['game_mode_filename']} has not been created")
        if (
            "section_name" in kwargs
            and kwargs["section_name"] not in cls.forms[kwargs["game_mode_filename"]]
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
            cls.forms[game_mode_filename][section_name]["status"] = "complete"
            return True
        cls.forms[game_mode_filename][section_name]["status"] = "incomplete"
        return False

    @classmethod
    def check_game_mode_complete(cls, game_mode_filename) -> bool:
        """
        Checks thats all sections of the active :param: `game_mode_filename` have a status of 'complete' in :class: `FormManager.forms`.

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a boolean True/False value representing if the :param:`game_mode_filename` is complete
        """
        if game_mode_filename in cls.forms and all(
            cls.check_section_complete(game_mode_filename, section_name)
            for section_name in cls.forms[game_mode_filename].keys()
        ):
            GameModeManager.game_modes[game_mode_filename]["complete"] = True
            return True
        return False

    # Setters

    @classmethod
    def update_section(cls, game_mode_filename, section_name, data) -> Dict[str, Any]:
        """
        Update the values of a specific :param:`section` of a form for an active :param:`game_mode_filename`.

        :param game_mode_filename: the file name and extension of the current game mode
        :param section_name: the name of the section for which the values will be updated
        :param data: a dictionary representation of config form values to use to update the reference for an active :param: `game_mode_filename`
        :return: the :param:`section` of the active :param: `game_mode_filename` with values updated from :param:`data`
        """
        # cls.verify(game_mode_filename=game_mode_filename, section_name=section_name)
        print("666", game_mode_filename, cls.forms.keys())
        cls.forms[game_mode_filename][section_name]["form"] = cls.base_forms[
            section_name
        ]["form"](data=data)
        return cls.forms[game_mode_filename][section_name]

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
