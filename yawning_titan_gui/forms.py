import copy
from dataclasses import fields
from typing import Any, Dict, Union

import yaml
from django import forms as django_forms
from django.forms import widgets
from yaml import SafeLoader

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import (
    ObservationSpaceConfig,
)
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan_gui import DEFAULT_GAME_MODE
from yawning_titan_gui.helpers import GameModeManager


class RangeInput(widgets.NumberInput):
    """Custom widget for range input range input field."""

    input_type = "range"


red_config_form_map = {
    "groups": {
        "target_mechanism": [
            "red_chooses_target_at_random",
            "red_target_node",
            "red_prioritises_connected_nodes",
            "red_prioritises_un_connected_nodes",
            "red_prioritises_vulnerable_nodes",
            "red_prioritises_resilient_nodes",
        ],
        "target_source": [
            "red_can_only_attack_from_red_agent_node",
            "red_can_attack_from_any_red_node",
        ],
    },
    "dependencies": {
        "red_can_naturally_spread": [
            "chance_to_spread_to_connected_node",
            "chance_to_spread_to_unconnected_node",
        ],
        "red_uses_spread_action": [
            "spread_action_likelihood",
            "chance_for_red_to_spread",
        ],
        "red_uses_random_infect_action": [
            "random_infect_action_likelihood",
            "chance_for_red_to_random_compromise",
        ],
        "red_uses_basic_attack_action": ["basic_attack_action_likelihood"],
        "red_uses_do_nothing_action": ["do_nothing_action_likelihood"],
        "red_uses_move_action": ["move_action_likelihood"],
        "red_uses_zero_day_action": [
            "zero_day_start_amount",
            "days_required_for_zero_day",
        ],
        "red_target_node": ["red_always_chooses_shortest_distance_to_target"],
        "red_uses_skill": ["red_skill"],
    },
}

blue_config_form_map = {"groups": {}, "dependencies": {}}

observation_space_config_form_map = {
    "groups": {},
    "dependencies": {
        "can_discover_failed_attacks": ["chance_to_discover_failed_attack"],
        "can_discover_succeeded_attacks_if_compromise_is_not_discovered": [
            "chance_to_discover_succeeded_attack_compromise_not_known"
        ],
        "can_discover_succeeded_attacks_if_compromise_is_discovered": [
            "chance_to_discover_succeeded_attack_compromise_known"
        ],
        "making_node_safe_modifies_vulnerability": [
            "vulnerability_change_during_node_patch",
            "making_node_safe_gives_random_vulnerability",
        ],
    },
}

game_rules_config_form_map = {
    "groups": {
        "high_value_node_choice": [
            "choose_high_value_nodes_placement_at_random",
            "choose_high_value_nodes_furthest_away_from_entry",
        ],
        "entry_node_choice": [
            "choose_entry_nodes_randomly",
            "prefer_central_nodes_for_entry_nodes",
            "prefer_edge_nodes_for_entry_nodes",
        ],
    },
    "dependencies": {},
}

reset_config_form_map = {}

rewards_config_form_map = {}

miscellaneous_config_form_map = {}

config_form_maps: Dict[str, Dict[str, Any]] = {
    "red": red_config_form_map,
    "blue": blue_config_form_map,
    "game_rules": game_rules_config_form_map,
    "observation_space": observation_space_config_form_map,
    "reset": reset_config_form_map,
    "rewards": rewards_config_form_map,
    "miscellaneous": miscellaneous_config_form_map,
}

subsection_labels = {
    "red": {
        "red_uses_skill": "Red agent attack behavior: Choose at least 1 of the following 3 items (red_ignores_defences: False counts as choosing an item)",
        "red_uses_spread_action": "Red agent actions: Choose at least one of the following 6 'red_uses_***' items (each item has associated weighting)",
        "red_can_naturally_spread": "Red agent natural spread",
    },
    "blue": {
        "blue_uses_reduce_vulnerability": "Blue agent actions: Choose at least one of the following 8 items"
    },
}


class ConfigForm(django_forms.Form):
    """
    Base class for represent yawning_titan config classes as html forms.

    - Represent float inputs using range sliders
    - Represent string inputs as text input fields
    - Represent integer inputs as number input fields
    - Represent boolean inputs as styled checkboxes
    - Represent elements that are mutually exclusive as dropdowns

    :param section: The string name of a config section in the Yawning Titan config
    :param config_form_map: A dictionary representing the structure of the config form
    :param ConfigClass: An instance of :class: `~yawning_titan.config.game_config.config_abc.ConfigABC` representing a
        section of the Yawning Titan config
    """

    def __init__(
        self,
        section: str,
        config_form_map: Dict[str, dict],
        ConfigClass: ConfigABC,
        *args,
        **kwargs,
    ):
        super(ConfigForm, self).__init__(*args, **kwargs)

        self.config_class = ConfigClass
        self.section = section
        self.group_errors = None

        field_elements = {}
        attrs = {}
        grouped_elements = []

        # created dropdowns from grouped elements
        for name, group in config_form_map.get("groups", {}).items():
            field_elements[name] = django_forms.ChoiceField(
                choices=((val, val.replace("_", " ")) for i, val in enumerate(group)),
                widget=django_forms.Select(
                    attrs={"class": "form-control"},
                ),
                required=True,
                help_text="this will be replaced with description",
            )
            grouped_elements.extend(group)

        for parent, dependents in config_form_map.get("dependencies", {}).items():
            attrs[parent] = f" {parent} grouped parent"
            for field in dependents:
                attrs[field] = f" {parent} grouped child hidden"

        for name, _type in {
            field.name.lstrip("_"): field.type for field in fields(ConfigClass)
        }.items():
            _class = attrs.get(name, "")
            if name in grouped_elements:
                continue

            if _type == "bool":
                field_elements[name] = django_forms.BooleanField(
                    widget=widgets.CheckboxInput(
                        attrs={"role": "switch", "class": "form-check-input" + _class}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )
            elif _type == "float":
                field_elements[name] = django_forms.FloatField(
                    widget=RangeInput(
                        attrs={"class": "form-control" + _class, "step": "0.01"}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                    min_value=0,
                    max_value=1,
                )
            elif _type == "int":
                field_elements[name] = django_forms.IntegerField(
                    widget=widgets.NumberInput(
                        attrs={"class": "form-control" + _class}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )
            else:
                field_elements[name] = django_forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control" + _class}),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )

        self.fields = field_elements

    def soft_validate(self, data: dict) -> bool:
        """
        Validate the config form without raising any errors.

        Use the :func: `ConfigABC.validate <yawning_titan.config.game_config.config_abc.ConfigABC.validate>`
        to validate the config catching any exceptions.

        :param data: a dictionary of options to validate.

        :return: True if config section is valid otherwise False
        """
        try:
            self.config_class.validate(data)
            return True
        except Exception:
            return False

    def is_valid(self) -> bool:
        """
        Check that config form is valid for fields and subsections.

        Overrides the `django_forms` `is_valid` method to add checks for field values dependent
        on other fields.

        :return: A bool value True if the form meets the validation criteria and produces a valid
            :class: `~yawning_titan.config.game_config.config_abc.ConfigABC`
        """
        fields_valid = super().is_valid()
        try:
            config = GameModeFormManager.game_mode_section_form_from_default(
                self.cleaned_data,
                self.section,
            )
            self.config_class = self.config_class.create(config)
        except Exception as e:
            self.group_errors = e
        groups_valid = True if self.group_errors is None else False
        return groups_valid and fields_valid


class RedAgentForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.agents.red_agent_config.RedAgentConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__("red", red_config_form_map, RedAgentConfig, *args, **kwargs)


class BlueAgentForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.agents.blue_agent_config.BlueAgentConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__("blue", blue_config_form_map, BlueAgentConfig, *args, **kwargs)


class ObservationSpaceForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.observation_space_config.ObservationSpaceConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            "observation_space",
            observation_space_config_form_map,
            ObservationSpaceConfig,
            *args,
            **kwargs,
        )


class ResetForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.reset_config.ResetConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__("reset", reset_config_form_map, ResetConfig, *args, **kwargs)


class RewardsForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.rewards_config.RewardsConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            "rewards", rewards_config_form_map, RewardsConfig, *args, **kwargs
        )


class GameRulesForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.environment.game_rules_config.GameRulesConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            "game_rules", game_rules_config_form_map, GameRulesConfig, *args, **kwargs
        )


class MiscellaneousForm(ConfigForm):
    """Representation of :class:`~yawning_titan.config.game_config.miscellaneous_config.MiscellaneousConfig` as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            "miscellaneous",
            miscellaneous_config_form_map,
            MiscellaneousConfig,
            *args,
            **kwargs,
        )


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
    game_mode = GameModeConfig.create(section_configs)
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
        "observation_space": {
            "form": ObservationSpaceForm,
            "icon": "bi-binoculars",
        },
        "rewards": {"form": RewardsForm, "icon": "bi-star"},
        "reset": {
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

    @staticmethod
    def get_config_from_default() -> Dict[str, Dict[str, Any]]:
        """
        Create game mode config dictionary by formatting default .yaml config file.

        :return: The modified section of the config as a dictionary
        """
        with open(GAME_MODES_DIR / DEFAULT_GAME_MODE) as f:
            new_settings: Dict[str, Dict[str, Any]] = yaml.load(f, Loader=SafeLoader)

        return {key.lower(): val for key, val in new_settings.items()}

    @classmethod
    def game_mode_section_form_from_default(
        cls, gui_section_options: Dict[str, Any], section: str
    ) -> Dict[str, Any]:
        """
        Update default game mode options with GUI inputted options.

        Create game mode section dictionary by updating default .yaml config file
        with settings inputted in the GUI.

        :param gui_section_options: dictionary with options configured in GUI
        :param section: config section to update

        :return: The modified section of the config as a dictionary
        """
        new_settings = cls.get_config_from_default()
        gui_section_options = {
            key: val for key, val in gui_section_options.items() if val is not None
        }  # remove null options from form

        # add settings items for selection values
        for name in config_form_maps[section].get("groups", {}).keys():
            new_settings[section][gui_section_options[name]] = True
            del gui_section_options[name]

        new_settings[section].update(gui_section_options)
        return new_settings[section]

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
        :param initial_options: the initial state of the options for the :param:`game_mode_filename`
        :return: a dictionary representation of the sections of the  :class:`GameModeConfig <yawning_titan.config.game_config.game_mode_config.GameModeConfig>`
        """
        if game_mode_filename in cls.forms:
            return cls.forms[game_mode_filename]
        else:
            if (
                game_mode_filename in GameModeManager.game_modes.keys()
                and GameModeManager.game_modes[game_mode_filename]["complete"]
            ):
                initial_options = GameModeManager.get_game_mode(
                    game_mode_filename
                ).to_dict()
            else:
                initial_options = cls.get_config_from_default()

            forms = copy.deepcopy(cls.base_forms)
            for section_name, section in forms.items():
                form: ConfigForm = section["form"](
                    initial=initial_options[section_name]
                )
                section.update(
                    {
                        "form": form,
                        "status": "complete"
                        if form.soft_validate(initial_options[section_name])
                        else "incomplete",
                    }
                )

            cls.forms[game_mode_filename] = forms
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
        cls.verify(game_mode_filename=game_mode_filename, section_name=section_name)
        cls.forms[game_mode_filename][section_name]["form"] = cls.base_forms[
            section_name
        ]["form"](data)
        return cls.forms[game_mode_filename][section_name]

    @classmethod
    def save_as_game_mode(cls, game_mode_filename: str) -> GameModeConfig:
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
        game_mode = GameModeConfig.create(section_configs)
        game_mode.to_yaml(GAME_MODES_DIR / game_mode_filename)
        # del cls.forms[game_mode_filename]
        return game_mode
