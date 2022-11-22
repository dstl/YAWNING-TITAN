from django import forms
from django.forms import widgets

#D:\Pycharm projects\YAWNING-TITAN-DEV\YAWNING-TITAN\yawning_titan

#TEMP USE OF YAML FORM
import yaml
from yaml import SafeLoader
from yawning_titan.config.game_modes import default_game_mode_path

with open(default_game_mode_path()) as f:
    settings = yaml.load(f, Loader=SafeLoader)

class RangeInput(widgets.NumberInput):
    input_type = "range"

class ConfigForm(forms.Form):
    def __init__(self,config_element,*args,**kwargs):
        super(ConfigForm,self).__init__(*args,**kwargs)
        bool_elements = {}
        freetext_elements = {}
        integer_elements = {}

        for key,val in settings[config_element].items():
            _class = attrs.get(key,"")
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