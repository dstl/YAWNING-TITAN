from django.views import View
from django.shortcuts import render
from yawning_titan.config.agents.blue_agent_config import BlueAgentConfig
from yawning_titan.config.agents.red_agent_config import RedAgentConfig
from yawning_titan.config.environment.game_rules_config import GameRulesConfig
from yawning_titan.config.environment.observation_space_config import ObservationSpaceConfig
from yawning_titan.config.environment.reset_config import ResetConfig
from yawning_titan.config.environment.rewards_config import RewardsConfig
from yawning_titan.config.game_config.miscellaneous_config import MiscellaneousConfig
from yawning_titan.config.game_config.game_mode_config import GameModeConfig

from yawning_titan_server.settings import STATIC_URL

from collections import defaultdict

from yawning_titan_gui.forms import (
    ConfigForm, 
    red_config_form_map,
    blue_config_form_map,
    observation_space_config_form_map,
    game_rules_config_form_map,
    rewards_config_form_map,
    miscellaneous_config_form_map,
    reset_config_form_map
)

from yawning_titan import GAME_MODES_DIR

def static_url(type,file_path):
    return  f"{STATIC_URL}/{type}/{file_path.name}"

def game_mode_path(game_mode_filename:str):
    return (GAME_MODES_DIR / game_mode_filename).as_posix()

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
    def get(self, request,*args, game_mode_file:str=None, **kwargs):
        if game_mode_file is not None:
            game_mode = GameModeConfig.create_from_yaml(game_mode_path(game_mode_file))
            game_mode_config = game_mode.to_dict()
        else:
            game_mode_config = defaultdict(dict)

        red_config_form = ConfigForm(red_config_form_map,RedAgentConfig,initial=game_mode_config["red"])
        blue_config_form = ConfigForm(blue_config_form_map,BlueAgentConfig,initial=game_mode_config["blue"])

        observation_space_config_form = ConfigForm(observation_space_config_form_map,ObservationSpaceConfig,initial=game_mode_config["observation_space"])
        game_rules_config_form = ConfigForm(game_rules_config_form_map,GameRulesConfig,initial=game_mode_config["game_rules"])
        reset_config_form = ConfigForm(reset_config_form_map,ResetConfig,initial=game_mode_config["reset"])
        rewards_config_form = ConfigForm(rewards_config_form_map,RewardsConfig,initial=game_mode_config["rewards"])
        miscellaneous_config_form = ConfigForm(miscellaneous_config_form_map,MiscellaneousConfig,initial=game_mode_config["miscellaneous"])

        self.forms = {
            "RED":red_config_form,
            "BLUE":blue_config_form,
            "OBSERVATION SPACE": observation_space_config_form,
            "GAME RULES": game_rules_config_form,
            "REWARDS": rewards_config_form,
            "RESET": reset_config_form,
            "MISCELLANEOUS": miscellaneous_config_form
        }
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        pass

    def render_page(self, request):
        return render(
            request,
            "game_mode_config.html",
            {
                "forms":self.forms
            }
        )
