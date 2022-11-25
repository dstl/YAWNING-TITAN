from dataclasses import fields
from typing import Any, Dict

import yaml
from django import forms
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
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig


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

reset_config_form_map = {"groups": {}, "dependencies": {}}

rewards_config_form_map = {"groups": {}, "dependencies": {}}

miscellaneous_config_form_map = {"groups": {}, "dependencies": {}}

config_form_maps = {
    "red": red_config_form_map,
    "blue": blue_config_form_map,
    "game_rules": game_rules_config_form_map,
    "observation_space": observation_space_config_form_map,
    "reset": reset_config_form_map,
    "rewards": rewards_config_form_map,
    "miscellaneous": miscellaneous_config_form_map,
}


class ConfigForm(forms.Form):
    """
    Base class for represent yawning_titan config classes as html forms.

    - Represent float inputs using range sliders
    - Represent string inputs as text input fields
    - Represent integer inputs as number input fields
    - Represent boolean inputs as styled checkboxes
    - Represent elements that are mutually exclusive as dropdowns
    """

    def __init__(
        self, config_form_map: Dict[str, dict], ConfigClass: ConfigABC, *args, **kwargs
    ):
        super(ConfigForm, self).__init__(*args, **kwargs)
        bool_elements = {}
        freetext_elements = {}
        integer_elements = {}
        dropdown_elements = {}

        attrs = {}

        grouped_elements = []

        # created dropdowns from grouped elements
        for name, group in config_form_map["groups"].items():
            dropdown_elements[name] = forms.ChoiceField(
                choices=((val, val.replace("_", " ")) for i, val in enumerate(group)),
                widget=forms.Select(
                    attrs={"class": "form-control"},
                ),
                required=True,
                help_text="this will be replaced with description",
            )
            grouped_elements.extend(group)

        for parent, dependents in config_form_map["dependencies"].items():
            attrs[parent] = f" {parent} grouped parent"
            for field in dependents:
                attrs[field] = f" {parent} grouped hidden"

        for name, _type in {
            field.name.lstrip("_"): field.type for field in fields(ConfigClass)
        }.items():
            _class = attrs.get(name, "")
            if name in grouped_elements:
                continue
            if _type == "bool":
                bool_elements[name] = forms.BooleanField(
                    widget=widgets.CheckboxInput(
                        attrs={"role":"switch","class": "form-check-input" + _class}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )
            elif _type == "float":
                integer_elements[name] = forms.FloatField(
                    widget=RangeInput(
                        attrs={"class": "form-control" + _class, "step": "0.01"}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                    min_value=0,
                    max_value=1,
                )
            elif _type == "int":
                integer_elements[name] = forms.IntegerField(
                    widget=widgets.NumberInput(
                        attrs={"class": "form-control" + _class}
                    ),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )
            else:
                freetext_elements[name] = forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control" + _class}),
                    required=False,
                    help_text=getattr(ConfigClass, name).__doc__,
                )
        self.fields = {
            **dropdown_elements,
            **bool_elements,
            **freetext_elements,
            **integer_elements,
        }


class RedAgentForm(ConfigForm):
    """Representation of RedAgentConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(red_config_form_map, RedAgentConfig, *args, **kwargs)


class BlueAgentForm(ConfigForm):
    """Representation of BlueAgentConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(blue_config_form_map, BlueAgentConfig, *args, **kwargs)


class ObservationSpaceForm(ConfigForm):
    """Representation of ObservationSpaceConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            observation_space_config_form_map, ObservationSpaceConfig, *args, **kwargs
        )


class ResetForm(ConfigForm):
    """Representation of ResetConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(reset_config_form_map, ResetConfig, *args, **kwargs)


class RewardsForm(ConfigForm):
    """Representation of RewardConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(rewards_config_form_map, RewardsConfig, *args, **kwargs)


class GameRulesForm(ConfigForm):
    """Representation of GameRulesConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(rewards_config_form_map, GameRulesConfig, *args, **kwargs)


class MiscellaneousForm(ConfigForm):
    """Representation of MiscellaneousConfig as html form."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            miscellaneous_config_form_map, MiscellaneousConfig, *args, **kwargs
        )


def game_mode_from_default(gui_options: Dict[str, Dict[str, Any]], section: str):
    """
    Update default game mode options with GUI inputted options.

    Create game mode section dictionary by updating default .yaml config file
    with settings inputted in the GUI.

    Args:
        gui_options: dictionary with options configured in GUI
        section: config section to update
    """
    with open(GAME_MODES_DIR / "everything_off_config.yaml") as f:
        new_settings: Dict[str, Dict[str, Any]] = yaml.load(f, Loader=SafeLoader)

    # add settings items for selection values
    for name in config_form_maps[section]["groups"].keys():
        print("NN", section, name, new_settings[section.upper()])
        new_settings[section.upper()][gui_options[name]] = True
        del gui_options[name]

    new_settings[section.upper()].update(gui_options)
    return new_settings[section.upper()]
