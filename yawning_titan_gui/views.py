import json
from typing import Any, Dict
from django.views import View
from django.shortcuts import render

from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.config_abc import ConfigABC
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan.config.game_config.game_mode_config import GameModeConfig

from yawning_titan_gui.forms import (
    RedAgentForm,
    BlueAgentForm,
    ObservationSpaceForm,
    GameRulesForm,
    MiscellaneousForm,
    ResetForm,
    RewardsForm
)

from django.http import QueryDict,JsonResponse

from yawning_titan_server.settings import STATIC_URL

from collections import defaultdict

import yaml
from yaml import SafeLoader

from yawning_titan_gui.forms import (
    ConfigForm
)

from yawning_titan import GAME_MODES_DIR

def static_url(type,file_path):
    return  f"{STATIC_URL}/{type}/{file_path.name}"

def game_mode_path(game_mode_filename:str):
    return (GAME_MODES_DIR / game_mode_filename).as_posix()

def game_mode_from_default(
    base_config_path:str,
    updated_settings:Dict[str,Dict[str,Any]],
    section:str
):
    with open(base_config_path) as f:
        new_settings: Dict[str, Dict[str, Any]] = yaml.load(
            f, Loader=SafeLoader
        )
    new_settings[section.upper()].update(updated_settings)
    return new_settings[section.upper()]
    

default_sidebar = {
    "Documentation":[
        "Getting started",
        "Tutorials",
        "How to configure",
        "Code"
    ],
    "Configuration":[
        "Manage game modes",
        "Manage networks",
    ],
    "Training runs":[
        "Setup a training run",
        "View completed runs"
    ],
    "About":[
        "Contributors",
        "Report bug", 
        "FAQ"
    ]
}
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        return self.render_page(request)

    def render_page(self, request):
        return render(
            request,
            "home.html",
            {
                "sidebar":default_sidebar
            }
        )

class GameModesView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "game_modes.html",
            {
                "sidebar":default_sidebar,
                "game_modes":[
                    {
                        "filename":"base_config.yaml",
                        "name":"test 1",
                        "description":"description 1"
                    },
                    {
                        "filename":"base_config.yaml",
                        "name":"test 2",
                        "description":"description 2"
                    },
                    {
                        "filename":"base_config.yaml",
                        "name":"test 3",
                        "description": "description 3 is really really really really really really really really really really really really really really really really really really really really long"
                    }
                ]
            }
        )

    def post(self, request, *args, **kwargs):
        pass

    
class GameModeConfigView(View):
    def __init__(self, **kwargs) -> None:
        self.configs:Dict[str,ConfigABC] = {
            "red":RedAgentConfig,
            "blue":BlueAgentConfig,
            "observation_space": ObservationSpaceConfig,
            "game_rules": GameRulesConfig,
            "rewards": RewardsConfig,
            "reset": ResetConfig,
            "miscellaneous": MiscellaneousConfig
        }
        self.forms = {
            "red":RedAgentForm,
            "blue":BlueAgentForm,
            "observation_space": ObservationSpaceForm,
            "game_rules": GameRulesForm,
            "rewards": RewardsForm,
            "reset": ResetForm,
            "miscellaneous": MiscellaneousForm
        }

    def get(self, request,*args, game_mode_file:str=None, **kwargs):
        if game_mode_file is not None:
            game_mode = GameModeConfig.create_from_yaml(game_mode_path(game_mode_file))
            game_mode_config = game_mode.to_dict()
        else:
            game_mode_config = defaultdict(dict)


        forms = {
            "red":RedAgentForm(initial=game_mode_config["red"]),
            "blue":BlueAgentForm(initial=game_mode_config["blue"]),
            "observation_space": ObservationSpaceForm(initial=game_mode_config["observation_space"]),
            "game_rules": GameRulesForm(initial=game_mode_config["game_rules"]),
            "rewards": RewardsForm(initial=game_mode_config["rewards"]),
            "reset": ResetForm(initial=game_mode_config["reset"]),
            "miscellaneous": MiscellaneousForm(initial=game_mode_config["miscellaneous"])
        }
       
        return self.render_page(request,forms)

    def post(self, request, *args, **kwargs):  
        data = QueryDict.dict(request.POST)
        del data["csrfmiddlewaretoken"]        
        form_name = data.pop("form_name")
        
        forms = {}
        forms[form_name] = self.forms[form_name](request.POST)

       

        if forms[form_name].is_valid():       
            print("JJJ",forms[form_name].cleaned_data)     
            self.configs[form_name] = self.configs[form_name].create(game_mode_from_default(
                GAME_MODES_DIR / "everything_off_config.yaml",
                forms[form_name].cleaned_data,
                form_name
            ))
            print(self.configs[form_name].to_dict())
            return JsonResponse({"error":False})
        else:
            return self.render_page(request,forms)


    def render_page(self, request, forms):
        return render(
            request,
            "game_mode_config.html",
            {
                "forms":forms
            }
        )
