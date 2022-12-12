from dataclasses import fields
from typing import Any, Dict

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

config_form_maps = {
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
            self.config_class = self.config_class.create(
                game_mode_section_form_from_default(
                    self.cleaned_data,
                    self.section,
                )
            )
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


def game_mode_section_form_from_default(
    gui_section_options: Dict[str, Any], section: str
)->Dict[str,Any]:
    """
    Update default game mode options with GUI inputted options.

    Create game mode section dictionary by updating default .yaml config file
    with settings inputted in the GUI.

    :param gui_section_options: dictionary with options configured in GUI
    :param section: config section to update

    :return: The modified section of the config as a dictionary
    """
    with open(GAME_MODES_DIR / DEFAULT_GAME_MODE) as f:
        new_settings: Dict[str, Dict[str, Any]] = yaml.load(f, Loader=SafeLoader)

    # add settings items for selection values
    for name in config_form_maps[section]["groups"].keys():
        new_settings[section.upper()][gui_section_options[name]] = True
        del gui_section_options[name]

    new_settings[section.upper()].update(gui_section_options)
    return new_settings[section.upper()]


def game_mode_from_form_sections(
    game_mode_forms: Dict[str, django_forms.Form], game_mode_file: str
):
    """
    Create a complete config yaml file from a dictionary of form sections.

    :param game_mode_forms: dictionary containing django form objects representing sections of the config.

    :return: a valid instance of :class: `~yawning_titan.config.game_config.game_mode_config.GameModeConfig`
    """
    section_configs = {
        section_name.upper(): form.cleaned_data
        for section_name, form in game_mode_forms.items()
    }
    game_mode = GameModeConfig.create(section_configs)
    game_mode.to_yaml(GAME_MODES_DIR / game_mode_file)
    return game_mode
