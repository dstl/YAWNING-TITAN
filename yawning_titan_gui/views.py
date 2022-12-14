import shutil
from collections import defaultdict
from typing import Any, Optional

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan_gui.forms import (
    BlueAgentForm,
    ConfigForm,
    GameRulesForm,
    MiscellaneousForm,
    ObservationSpaceForm,
    RedAgentForm,
    ResetForm,
    RewardsForm,
    create_game_mode_from_form_sections,
    subsection_labels,
)
from yawning_titan_gui.helpers import (
    check_game_mode,
    game_mode_path,
    get_game_mode_file_paths,
    next_key,
    uniquify,
)

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

protected_game_modes = ["base_config.yaml"]

unfinished_game_modes = []


class OnLoadView(View):
    """Inherit from this `django.views.View` to run additional code when a view is requested."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        global unfinished_game_modes
        unfinished_game_modes = []


class HomeView(OnLoadView):
    """Django page template for landing page."""

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def render_page(self, request):
        """Process pythonic tags in home.html and return formatted page."""
        return render(request, "home.html", {"sidebar": default_sidebar})


class DocsView(OnLoadView):
    """
    Django representation of home.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "docs.html", {"sidebar": default_sidebar})

    def post(self, request, *args, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "docs.html", {"sidebar": default_sidebar})


class GameModesView(View):
    """Django page template for game mode management."""

    def get(self, request, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        return render(
            request,
            "game_modes.html",
            {
                "sidebar": default_sidebar,
                "game_modes": [
                    *unfinished_game_modes,
                    *[
                        {
                            "filename": path.name,
                            "name": path.stem,
                            "description": f"description {i}",
                            "protected": path.stem in protected_game_modes,
                            "complete": check_game_mode(path),
                        }
                        for i, path in enumerate(
                            get_game_mode_file_paths(valid_only=False)
                        )
                    ],
                ],
            },
        )

    def post(self, request, *args, **kwargs):
        """
        Handle page get requests.

        Currently there are no POST request on the `game_modes.html` page.

        :param request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        pass


class GameModeConfigView(OnLoadView):
    """Django page template for game mode creation and editing."""

    def get(
        self, request, *args, game_mode_file: str = None, section: str = None, **kwargs
    ):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_file: a game mode filename passed within the page url parameters
        :param section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        game_mode_config = defaultdict(dict)
        section = list(forms.keys())[0] if section is None else section
        game_mode_file_path = game_mode_path(game_mode_file)
        if game_mode_file_path.exists():
            try:
                game_mode = GameModeConfig.create_from_yaml(game_mode_file_path)
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

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_file: a game mode filename passed within the page url parameters
        :param section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        section = list(forms.keys())[0] if section is None else section
        form: ConfigForm = forms[section]["form"](request.POST)

        if form.is_valid():
            completed_game_modes[game_mode_file][section] = form
            if len(completed_game_modes[game_mode_file].keys()) == len(forms):
                create_game_mode_from_form_sections(
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

        :param request: the Django page `request` object containing the html data and the server GET / POST request bodies.
        :param game_mode_file: a game mode filename passed within the page url parameters
        :param section: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        :param error_message: an optional error message string to be displayed in the `#error-message` html element

        :return: Html string representing an instance of the`GameModeConfigView`
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
                "protected": game_mode_file in protected_game_modes,
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

    :param request: here the django_request object will be specifically loaded with
        `operation`,`game_mode_name` and optional `source_game_mode` parameters.

    :return: `JsonResponse` object with either success code 500 (generic success) or
        error code 400 (generic error) containing a message.
    """
    global unfinished_game_modes
    if request.method == "POST":
        game_mode_name = request.POST.get("game_mode_name")
        operation = request.POST.get("operation")

        if operation == "create":
            new_game_mode_path = uniquify(GAME_MODES_DIR / f"{game_mode_name}.yaml")
            unfinished_game_modes.append(
                {
                    "filename": new_game_mode_path.name,
                    "name": new_game_mode_path.stem,
                    "description": "latest game mode",
                    "protected": new_game_mode_path.stem in protected_game_modes,
                    "complete": False,
                }
            )
            load = reverse(
                "game mode config", kwargs={"game_mode_file": new_game_mode_path.name}
            )

        elif operation == "delete":
            path = GAME_MODES_DIR / f"{game_mode_name}.yaml"
            if path.exists():
                path.unlink()
            load = "reload"

        elif operation == "create from":
            source_game_mode_path = (
                GAME_MODES_DIR / f"{request.POST.get('source_game_mode')}.yaml"
            )
            new_game_mode_path = uniquify(GAME_MODES_DIR / f"{game_mode_name}.yaml")
            shutil.copy(source_game_mode_path, new_game_mode_path)
            load = reverse(
                "game mode config", kwargs={"game_mode_file": new_game_mode_path.name}
            )
        return JsonResponse({"load": load})
    return JsonResponse({"message:": "FAILED"}, status=400)
