from dataclasses import fields
from typing import Dict
from django import forms
from django.forms import widgets

#D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\yawning_titan

#TEMP USE OF YAML FORM
import yaml
from yaml import SafeLoader
from yawning_titan.config.game_modes import default_game_mode_path


from yawning_titan.config.agents.red_agent_config import RedAgentConfig

class RangeInput(widgets.NumberInput):
    input_type = "range"


red_config_form_map = {
    "groups":{
        "target_mechanism":[
            "red_chooses_target_at_random",
            "red_target_node",
            "red_prioritises_connected_nodes",
            "red_prioritises_un_connected_nodes",
            "red_prioritises_vulnerable_nodes",
            "red_prioritises_resilient_nodes",
        ],
        "target_source":[
            "red_can_only_attack_from_red_agent_node",
            "red_can_attack_from_any_red_node"
        ]
    },
    "dependencies":{
        "red_can_naturally_spread":[
            "chance_to_spread_to_connected_node",
            "chance_to_spread_to_unconnected_node"
        ],
        "red_uses_spread_action":[
            "spread_action_likelihood",
            "chance_for_red_to_spread"
        ],
        "red_uses_random_infect_action":[
            "random_infect_action_likelihood",
            "chance_for_red_to_random_compromise"
        ],
        "red_uses_basic_attack_action":[
            "basic_attack_action_likelihood"
        ],
        "red_uses_do_nothing_action":[
            "do_nothing_action_likelihood"
        ],
        "red_uses_move_action":[
            "move_action_likelihood"
        ],
        "red_uses_zero_day_action":[
            "zero_day_start_amount",
            "days_required_for_zero_day"
        ],
        "red_target_node":[
            "red_always_chooses_shortest_distance_to_target"
        ]
    },
    "types":{field.name.lstrip('_'): field.type for field in fields(RedAgentConfig)}
}

print(red_config_form_map)

class ConfigForm(forms.Form):
    def __init__(self,config_form_map:Dict[str,dict],*args,**kwargs):
        super(ConfigForm,self).__init__(*args,**kwargs)
        bool_elements = {}
        freetext_elements = {}
        integer_elements = {}

        grouped_elements = []

        #created dropdowns from grouped elements
        for name,group in config_form_map["groups"].items():
            

        for name,_type in config_form_map["types"].items():
            if key in grouped_elements:
                continue
            if type(val) == bool:
                bool_elements[key] = forms.BooleanField(
                    widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
                    required=False,
                    help_text="this will be replaced with description",
                )
            elif type(val) == float:
                integer_elements[key] = forms.FloatField(
                    widget=RangeInput(attrs={"class": "form-control" + _class,'step': "0.01"}), 
                    required=False,
                    help_text="this will be replaced with description",
                    min_value=0,
                    max_value=1
                )
            elif type(val) == int:
                integer_elements[key] = forms.IntegerField(
                    widget=widgets.NumberInput(attrs={"class": "form-control" + _class}), 
                    required=False,
                    help_text="this will be replaced with description",
                )
            else:
                freetext_elements[key] = forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control" + _class}), 
                    required=False,
                    help_text="this will be replaced with description",
                )
        self.fields = {**group_objects,**bool_elements,**freetext_elements, **integer_elements}