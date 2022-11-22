from dataclasses import fields
from typing import Dict
from django import forms
from django.forms import widgets

#D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\yawning_titan

#TEMP USE OF YAML FORM
import yaml
from yaml import SafeLoader
from yawning_titan.config.game_config.config_abc import ConfigABC
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
    }
}

print(red_config_form_map)

class ConfigForm(forms.Form):
    def __init__(self,config_form_map:Dict[str,dict],ConfigClass:ConfigABC,*args,**kwargs):
        super(ConfigForm,self).__init__(*args,**kwargs)
        bool_elements = {}
        freetext_elements = {}
        integer_elements = {}
        dropdown_elements = {}

        attrs = {}

        grouped_elements = []

        #created dropdowns from grouped elements
        for name,group in config_form_map["groups"].items():
            dropdown_elements[name] = forms.ChoiceField(
                choices=((str(i),val.replace("_"," ")) for i,val in enumerate(group)),
                widget=forms.Select(
                    attrs={"class": "form-control"},                    
                ),
                required=True,
                help_text="this will be replaced with description"
            )
            grouped_elements.extend(group)

       
        for parent,dependents in config_form_map["dependencies"].items():
            for field in dependents:
                attrs[field] = f" {parent} grouped hidden"

        for name,_type in {field.name.lstrip('_'): field.type for field in fields(ConfigClass)}.items():
            _class = attrs.get(name,"")
            if name in grouped_elements:
                continue
            if type(_type) == bool:
                bool_elements[name] = forms.BooleanField(
                    widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
                    required=False,
                    help_text=getattr(ConfigClass,name).__doc__,
                )
            elif type(_type) == float:
                integer_elements[name] = forms.FloatField(
                    widget=RangeInput(attrs={"class": "form-control" + _class,'step': "0.01"}), 
                    required=False,
                    help_text=getattr(ConfigClass,name).__doc__,
                    min_value=0,
                    max_value=1
                )
            elif type(_type) == int:
                integer_elements[name] = forms.IntegerField(
                    widget=widgets.NumberInput(attrs={"class": "form-control" + _class}), 
                    required=False,
                    help_text=getattr(ConfigClass,name).__doc__,
                )
            else:
                freetext_elements[name] = forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control" + _class}), 
                    required=False,
                    help_text=getattr(ConfigClass,name).__doc__,
                )
        self.fields = {**dropdown_elements,**bool_elements,**freetext_elements, **integer_elements}

#         from django import forms
# from django.forms import widgets

# #D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\yawning_titan

# #TEMP USE OF YAML FORM
# import yaml
# from yaml import SafeLoader
# from yawning_titan.config.game_modes import default_game_mode_path

# with open(default_game_mode_path()) as f:
#     settings = yaml.load(f, Loader=SafeLoader)

# class RangeInput(widgets.NumberInput):
#     input_type = "range"

# class ConfigForm(forms.Form):
#     def __init__(self,config_element,*args,**kwargs):
#         super(ConfigForm,self).__init__(*args,**kwargs)
#         bool_elements = {}
#         freetext_elements = {}
#         integer_elements = {}

#         groups = {
#             "actions":[
#                 "red_uses_spread_action",
#                 "red_uses_random_infect_action",
#                 "red_uses_basic_attack_action",
#                 "red_uses_do_nothing_action",
#                 "red_uses_move_action",
#                 "red_uses_zero_day_action",
#             ]
#         }

#         dependencies = {
#             "red_uses_spread_action":["spread_action_likelihood","chance_for_red_to_spread"],
#             "red_uses_random_infect_action":["random_infect_action_likelihood","chance_for_red_to_random_compromise"],
#             "red_uses_basic_attack_action":["basic_attack_action_likelihood"],
#             "red_uses_do_nothing_action":["do_nothing_action_likelihood"],
#             "red_uses_move_action":["move_action_likelihood"],
#             "red_uses_zero_day_action":["zero_day_start_amount","days_required_for_zero_day"],
#         }
#         attrs = {}
#         for key,dependents in dependencies.items():
#             for field in dependents:
#                 attrs[field] = f" {key} grouped hidden"

#         grouped_elements = []
#         group_objects = {}
#         for group_name, group in groups.items():
#             group_objects[group_name] = forms.ChoiceField(
#                 choices=((str(i),val.replace("_"," ")) for i,val in enumerate(group)),
#                 widget=forms.Select(
#                     attrs={"class": "form-control"},                    
#                 ),
#                 required=True,
#                 help_text="this will be replaced with description"
#             )
#             grouped_elements.extend(group)

#         #temporary definition before real validation and rules implemented, can connect to back end validation routine.
#         #also apply range validation etc
#         for key,val in settings[config_element].items():
#             _class = attrs.get(key,"")
#             if key in grouped_elements:
#                 continue
#             if type(val) == bool:
#                 bool_elements[key] = forms.BooleanField(
#                     widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
#                     required=False,
#                     help_text="this will be replaced with description",
#                 )
#             elif type(val) == float:
#                 integer_elements[key] = forms.FloatField(
#                     widget=RangeInput(attrs={"class": "form-control" + _class,'step': "0.01"}), 
#                     required=False,
#                     help_text="this will be replaced with description",
#                     min_value=0,
#                     max_value=1
#                 )
#             elif type(val) == int:
#                 integer_elements[key] = forms.IntegerField(
#                     widget=widgets.NumberInput(attrs={"class": "form-control" + _class}), 
#                     required=False,
#                     help_text="this will be replaced with description",
#                 )
#             else:
#                 freetext_elements[key] = forms.CharField(
#                     widget=widgets.TextInput(attrs={"class": "form-control" + _class}), 
#                     required=False,
#                     help_text="this will be replaced with description",
#                 )
#         self.fields = {**group_objects,**bool_elements,**freetext_elements, **integer_elements}