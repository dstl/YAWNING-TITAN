from django.views import View
from django.shortcuts import render
from yt_front_end.settings import STATIC_URL

def static_url(type,file_path):
    return  f"{STATIC_URL}/{type}/{file_path.name}"

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
class Home(View):
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

class GameModes(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "game_modes.html",
            {
                "sidebar":default_sidebar,
                "game_modes":[
                    {"name":"test 1","description":"description 1"},
                    {"name":"test 2","description":"description 2"},
                    {"name":"test 3","description":"description 3 is really really really really really really really really really really really really really really really really really really really really long"}
                ]
            }
        )

    def post(self, request, *args, **kwargs):
        pass


class GameModeConfig(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "game_modes_config.html",
            {
                "forms":
            }
        )

    def post(self, request, *args, **kwargs):
        pass