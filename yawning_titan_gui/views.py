import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, List, Optional

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
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
    game_mode_from_form_sections,
    subsection_labels,
)


def game_mode_path(game_mode_filename: str):
    """Generate path for game mode file."""
    return (GAME_MODES_DIR / game_mode_filename).as_posix()


def check_game_mode(game_mode_path: Path) -> bool:
    """Check that a game mode path can construct a valid GameModeConfig object."""
    try:
        GameModeConfig.create_from_yaml(game_mode_path)
        return True
    except Exception:
        return False


def get_game_mode_file_paths(valid_only=False) -> List[Path]:
    """
    Select all game modes in the `GAME_MODES_DIR` matching criteria.

    Args:
        valid_only: whether to return only those game modes that pass the `GameModeConfig` validation check

    Returns:
        a list of file Path objects representing game modes.
    """
    game_modes = [
        g for g in GAME_MODES_DIR.iterdir() if g.stem != "everything_off_config"
    ]
    if not valid_only:
        return game_modes
    return [g for g in game_modes if check_game_mode(g)]


def next_key(_dict: dict, key: int) -> Any:
    """
    Get the next key in a dictionary.

    Use key_index + 1 if there is a subsequent key
    otherwise return first key.

    Args:
        _dict: a dictionary object
        key: the current key

    Returns:
        the subsequent key in the dictionary after `key`
    """
    keys = list(_dict.keys())
    key_index = keys.index(key)
    if key_index < (len(keys) - 1):
        return keys[key_index + 1]
    return keys[0]


def uniquify(path: Path) -> Path:
    """
    Create a unique file path from a proposed path by adding a numeral to the filename.

    Transforms the input `Path` object by iteratively adding numerals to the end
    of the filename until the proposed path does not exist.

    Returns:
        The transformed path object.

    Examples:
        >>>test.txt -> exists
        >>>test(1).txt -> exists
        >>>test(2).txt -> new path
    """
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

forms = {
    "red": {"form": RedAgentForm, "icon": "bi-lightning"},
    "blue": {"form": BlueAgentForm, "icon": "bi-shield"},
    "game_rules": {"form": GameRulesForm, "icon": "bi-clipboard"},
    "observation_space": {"form": ObservationSpaceForm, "icon": "bi-binoculars"},
    "rewards": {"form": RewardsForm, "icon": "bi-star"},
    "reset": {"form": ResetForm, "icon": "bi-arrow-clockwise"},
    "miscellaneous": {"form": MiscellaneousForm, "icon": "bi-brush"},
}

completed_game_modes = defaultdict(dict)

protected_game_modes = ["base_config"]


class HomeView(View):
    """Django page template for landing page."""

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        Args:
            request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        """
        Handle page post requests.

        Args:
            request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def render_page(self, request):
        """Process pythonic tags in home.html and return formatted page."""
        return render(request, "home.html", {"sidebar": default_sidebar})

class DocsView(View):
    """
    Django representation of home.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "docs.html", {"sidebar": default_sidebar})

    def post(self, request, *args, **kwargs):
        """Handle page post requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "docs.html", {"sidebar": default_sidebar}
        )

class GameModesView(View):
    """Django page template for game mode management."""

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        Args:
            request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
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
        """
        Handle page get requests.

        Currently there are no POST request on the `game_modes.html` page.

        Args:
            request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        pass

class GameModeConfigView(View):
    """Django page template for game mode creation and editing."""

    def get(
        self, request, *args, game_mode_file: str = None, section: str = None, **kwargs
    ):
        """
        Handle page get requests.

        Args:
            request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
            game_mode_file: a game mode filename passed within the page url parameters
            section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        """
        game_mode_config = defaultdict(dict)
        section = list(forms.keys())[0] if section is None else section

        if game_mode_file is not None:
            try:
                game_mode = GameModeConfig.create_from_yaml(
                    game_mode_path(game_mode_file)
                )
                game_mode_config = game_mode.to_dict()
            except Exception:
                pass

        form = completed_game_modes[game_mode_file].get(
            section, forms[section]["form"](initial=game_mode_config[section])
        )  # get completed form if available
        return self.render_page(request, form, section, game_mode_file)

    def post(
        self, request, *args, game_mode_file: str = None, section: str = None, **kwargs
    ):
        """
        Handle page post requests.

        Args:
            request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
            game_mode_file: a game mode filename passed within the page url parameters
            section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        """
        section = list(forms.keys())[0] if section is None else section
        form = forms[section]["form"](request.POST)

        if form.is_valid():
            completed_game_modes[game_mode_file][section] = form
            if len(completed_game_modes[game_mode_file].keys()) == len(forms):
                game_mode_from_form_sections(
                    completed_game_modes[game_mode_file], game_mode_file
                )
                completed_game_modes[game_mode_file] = {}
                return redirect("Manage game modes")
            return redirect(
                "game mode config", game_mode_file, next_key(forms, section)
            )

        return self.render_page(
            request, form, section, game_mode_file, form.group_errors
        )

    def render_page(
        self,
        request,
        form: ConfigForm,
        section: str,
        game_mode_file: str,
        error_message: Optional[str] = None,
    ):
        """
        Process pythonic tags in game_mode_config.html and return formatted page.

        Args:
            request: the Django page `request` object containing the html data and the server GET / POST request bodies.
            game_mode_file: a game mode filename passed within the page url parameters
            section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
            error_message: an optional error message string to be displayed in the `#error-message` html element
        """
        section = list(forms.keys())[0] if section is None else section
        return render(
            request,
            "game_mode_config.html",
            {
                "forms": forms,
                "form": form,
                "section": section,
                "error_message": error_message,
                "sidebar": default_sidebar,
                "game_mode_file": game_mode_file,
                "protected": Path(game_mode_file).stem in protected_game_modes,
                "completed_sections": completed_game_modes[game_mode_file].keys(),
                "subsection_labels": subsection_labels.get(section, {}),
            },
        )


def config_file_manager(request) -> JsonResponse:
    """
    Create, edit, delete config yaml files.

    Extract `operation`,`game_mode_name` and optional `source_game_mode` from POST request body and
    use the information to perform the appropriate alteration to the
    game mode files contained in the `GAME_MODES_DIR`.

    Args:
        request: here the django_request object will be specifically loaded with
        `operation`,`game_mode_name` and optional `source_game_mode` parameters.

    Returns:
        `JsonResponse` object with either success code 500 (generic success) or
        error code 400 (generic error) containing a message.
    """
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
