import inspect
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

from django.http import JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views import View

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
from yawning_titan_gui.forms import (
    BlueAgentForm,
    ConfigForm,
    GameRulesForm,
    MiscellaneousForm,
    ObservationSpaceForm,
    RedAgentForm,
    ResetForm,
    RewardsForm,
    game_mode_from_default,
)
from yawning_titan_server.settings import STATIC_URL


def static_url(type, file_path):
    """Generate URL for file_path in static folder."""
    return f"{STATIC_URL}/{type}/{file_path.name}"


def game_mode_path(game_mode_filename: str):
    """Generate path for game mode file."""
    return (GAME_MODES_DIR / game_mode_filename).as_posix()


def next_key(_dict: dict, key: int):
    """
    Get the next key in a dictionary.

    Use key_index + 1 if there is a subsequent key
    otherwise return first key.
    """
    keys = list(_dict.keys())
    key_index = keys.index(key)
    if key_index < (len(keys) - 1):
        return keys[key_index + 1]
    return keys[0]


def uniquify(path: Path):
    filename = path.stem
    extension = path.suffix

    parent = path.parent
    counter = 1

    while path.exists():
        path = parent / f"{filename}({counter}){extension}"
        print("PATH", path)
        counter += 1

    return path


default_sidebar = {
    "Documentation": ["Getting started", "Tutorials", "How to configure", "Code"],
    "Configuration": [
        "Manage game modes",
        "Manage networks",
    ],
    "Training runs": ["Setup a training run", "View completed runs"],
    "About": ["Contributors", "Report bug", "FAQ"],
}


class HomeView(View):
    """Django page template for landing page."""

    def get(self, request, *args, **kwargs):
        """Handle page get requests."""
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        """Handle page post requests."""
        return self.render_page(request)

    def render_page(self, request):
        """Process pythonic tags in home.html and return formatted page."""
        return render(request, "home.html", {"sidebar": default_sidebar})


class GameModesView(View):
    """Django page template for game mode management."""

    def get(self, request, *args, **kwargs):
        """Handle page get requests."""
        return render(
            request,
            "game_modes.html",
            {
                "sidebar": default_sidebar,
                "game_modes": [
                    {
                        "filename": path.name,
                        "name": path.stem,
                        "description": f"description {i}",
                    }
                    for i, path in enumerate(GAME_MODES_DIR.iterdir())
                ],
            },
        )

    def post(self, request, *args, **kwargs):
        """Handle page post requests."""
        pass


forms = {
    "red": {"form": RedAgentForm, "icon": "bi-lightning"},
    "blue": {"form": BlueAgentForm, "icon": "bi-shield"},
    "game_rules": {"form": GameRulesForm, "icon": "bi-clipboard"},
    "observation_space": {"form": ObservationSpaceForm, "icon": "bi-binoculars"},
    "rewards": {"form": RewardsForm, "icon": "bi-star"},
    "reset": {"form": ResetForm, "icon": "bi-arrow-clockwise"},
    "miscellaneous": {"form": MiscellaneousForm, "icon": "bi-brush"},
}

completed_forms = {}

configs: Dict[str, ConfigABC] = {
    "red": RedAgentConfig,
    "blue": BlueAgentConfig,
    "observation_space": ObservationSpaceConfig,
    "game_rules": GameRulesConfig,
    "rewards": RewardsConfig,
    "reset": ResetConfig,
    "miscellaneous": MiscellaneousConfig,
}


class GameModeConfigView(View):
    """Django page template for game mode creation and editing."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.forms = {
            "red": {"form": RedAgentForm, "icon": "bi-lightning"},
            "blue": {"form": BlueAgentForm, "icon": "bi-shield"},
            "game_rules": {"form": GameRulesForm, "icon": "bi-clipboard"},
            "observation_space": {
                "form": ObservationSpaceForm,
                "icon": "bi-binoculars",
            },
            "rewards": {"form": RewardsForm, "icon": "bi-star"},
            "reset": {"form": ResetForm, "icon": "bi-arrow-clockwise"},
            "miscellaneous": {"form": MiscellaneousForm, "icon": "bi-brush"},
        }

    def get(
        self, request, *args, game_mode_file: str = None, section: str = None, **kwargs
    ):
        """Handle page get requests."""

        game_mode_config = defaultdict(dict)

        if game_mode_file is not None:
            try:
                game_mode = GameModeConfig.create_from_yaml(
                    game_mode_path(game_mode_file)
                )
                game_mode_config = game_mode.to_dict()
            except Exception:
                pass

        for _section, section_form in self.forms.items():
            section_form["form"] = completed_forms.get(
                _section, section_form["form"](initial=game_mode_config[_section])
            )
            self.forms[_section] = section_form
        return self.render_page(request, section, game_mode_file)

    def post(
        self, request, *args, game_mode_file: str = None, section: str = None, **kwargs
    ):
        """Handle page post requests."""
        section = list(forms.keys())[0] if section is None else section
        form = self.forms[section]["form"](request.POST)
        self.forms[section]["form"] = form

        if form.is_valid():
            try:
                configs[section] = configs[section].create(
                    game_mode_from_default(
                        form.cleaned_data,
                        section,
                    )
                )
                completed_forms[section] = form
                return redirect("game mode config",game_mode_file,next_key(forms, section))
            except Exception as e:
                return self.render_page(request, section, game_mode_file, e)

        return self.render_page(request, section, game_mode_file)

    def render_page(self, request, section, game_mode_file, error_message=None):
        """Process pythonic tags in game_mode_config.html and return formatted page."""
        section = list(forms.keys())[0] if section is None else section
        return render(
            request,
            "game_mode_config.html",
            {
                "forms": self.forms,
                "section": section,
                "error_message": error_message,
                "sidebar": default_sidebar,
                "game_mode_file": game_mode_file
            },
        )


def config_file_manager(request):
    """"""
    if request.method == "POST":
        game_mode_name = request.POST.get("game_mode_name")
        operation = request.POST.get("operation")
        print(request.POST.get("game_mode_name"), request.POST)

        if operation == "create":
            default_game_mode_path = GAME_MODES_DIR / DEFAULT_GAME_MODE
            new_game_mode_path = uniquify(GAME_MODES_DIR / f"{game_mode_name}.yaml")
            shutil.copy(default_game_mode_path, new_game_mode_path)

        elif operation == "delete":
            (GAME_MODES_DIR / f"{game_mode_name}.yaml").unlink()

        return JsonResponse({"message:": "SUCCESS"})
    return JsonResponse({"message:": "FAILED"}, status=400)
