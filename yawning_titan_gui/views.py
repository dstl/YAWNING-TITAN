import inspect
import shutil
from pathlib import Path

from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan_gui import DEFAULT_GAME_MODE
from yawning_titan_server.settings import STATIC_URL


def static_url(type, file_path):
    """Generate URL for file_path in static folder."""
    return f"{STATIC_URL}/{type}/{file_path.name}"


def game_mode_path(game_mode_filename: str):
    """Generate path for game mode file."""
    return (GAME_MODES_DIR / game_mode_filename).as_posix()


def check_game_mode(game_mode_path: Path):
    """Check that a game mode path can construct a valid GameModeConfig object."""
    try:
        GameModeConfig.create_from_yaml(game_mode_path)
        return True
    except Exception as e:
        return False


def get_game_mode_file_paths(valid_only=False):
    """
    Return a list of file Path objects representing game modes.
    """
    game_modes = [
        g for g in GAME_MODES_DIR.iterdir() if g.stem != "everything_off_config"
    ]
    if not valid_only:
        return game_modes
    return [g for g in game_modes if check_game_mode(g)]


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

protected_game_modes = ["base_config"]


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
                        "protected": path.stem in protected_game_modes,
                        "complete": check_game_mode(path),
                    }
                    for i, path in enumerate(get_game_mode_file_paths(valid_only=False))
                ],
            },
        )

    def post(self, request, *args, **kwargs):
        """Handle page post requests."""
        pass


def config_file_manager(request):
    """Create, edit, delete config yaml files."""
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

        elif operation == "create from":
            source_game_mode_path = (
                GAME_MODES_DIR / f"{request.POST.get('source_game_mode')}.yaml"
            )
            new_game_mode_path = uniquify(GAME_MODES_DIR / f"{game_mode_name}.yaml")
            shutil.copy(source_game_mode_path, new_game_mode_path)

        return JsonResponse({"message:": "SUCCESS"})
    return JsonResponse({"message:": "FAILED"}, status=400)
