import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, List, Optional

import numpy as np
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from yawning_titan import GAME_MODES_DIR
from yawning_titan.config.game_config.game_mode_config import GameModeConfig
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.networks.network import Network
from yawning_titan.networks.network_db import NetworkDB, NetworkSchema
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
        >>> test.txt -> exists
        >>> test(1).txt -> exists
        >>> test(2).txt -> new path
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

default_toolbar = {
    "game-mode-set": {"icon": "bi-gear", "title": "Game mode config"},
    "network-set": {"icon": "bi-diagram-2", "title": "Network config"},
    "run-config-set": {"icon": "bi-collection-play", "title": "Run config"},
    "run-view": {"icon": "bi-play", "title": "Run game"},
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

protected_game_modes = [
    "base_config",
    "default_game_mode",
    "default_new_game_mode",
    "dcbo_config",
    "low_skill_red_with_random_infection_perfect_detection",
    "multiple_high_value_targets",
]

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
        return render(
            request,
            "home.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
        )


class DocsView(OnLoadView):
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
        return render(
            request,
            "docs.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
        )

    def post(self, request, *args, **kwargs):
        """Handle page post requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(
            request,
            "docs.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
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
                "toolbar": default_toolbar,
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

        Args:
            request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        pass


class NetworksView(View):
    """Django page template for network management."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `networks.html` and the server GET / POST request bodies.
        """
        networks = NetworkDB().all()
        range_bound_items = [
            {
                "name": "Entry nodes",
                "min": min(*[len(network.entry_nodes) for network in networks]),
                "max": max(*[len(network.entry_nodes) for network in networks]),
            },
            {
                "name": "High value nodes",
                "min": min(*[len(network.high_value_nodes) for network in networks]),
                "max": max(*[len(network.high_value_nodes) for network in networks]),
            },
            {
                "name": "Network nodes",
                "min": min(*[len(network.matrix[0]) for network in networks]),
                "max": max(*[len(network.matrix[0]) for network in networks]),
            },
        ]
        return render(
            request,
            "networks.html",
            {
                "sidebar": default_sidebar,
                "toolbar": default_toolbar,
                "networks": [network.doc_metadata for network in networks],
                "range_bound_items": range_bound_items,
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        db = NetworkDB()
        min = int(request.POST.get("min"))
        max = int(request.POST.get("max"))
        operations = {
            "Network nodes": lambda min, max: [
                network.doc_metadata.uuid
                for network in db.search(NetworkSchema.MATRIX.len_bt(min, max))
            ],
            "Entry nodes": lambda min, max: [
                network.doc_metadata.uuid
                for network in db.search(NetworkSchema.ENTRY_NODES.len_bt(min, max))
            ],
            "High value nodes": lambda min, max: [
                network.doc_metadata.uuid
                for network in db.search(
                    NetworkSchema.HIGH_VALUE_NODES.len_bt(min, max)
                )
            ],
        }
        return JsonResponse(
            {"ids": operations[request.POST.get("attribute")](min, max)}
        )


class NodeEditor(View):
    """
    Django representation of node_editor.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request, *args, **kwargs):
        """Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(
            request,
            "node_editor.html",
            {
                "sidebar": default_sidebar,
                "toolbar": default_toolbar,
                "network_json": json.dumps(
                    {
                        "nodes": {
                            "test1": {
                                "uuid": "test1",
                                "name": "test1",
                                "high_value_node": False,
                                "entry_node": False,
                                "vulnerability": 0.6,
                                "classes": "standard_node",
                                "x_pos": 1,
                                "y_pos": 7,
                            },
                            "test2": {
                                "uuid": "test2",
                                "name": "test2",
                                "high_value_node": False,
                                "entry_node": False,
                                "vulnerability": 0.79,
                                "classes": "standard_node",
                                "x_pos": 3,
                                "y_pos": 6,
                            },
                            "test3": {
                                "uuid": "test3",
                                "name": "test3",
                                "high_value_node": False,
                                "entry_node": False,
                                "vulnerability": 0.3,
                                "classes": "standard_node",
                                "x_pos": 2,
                                "y_pos": 7,
                            },
                        },
                        "edges": {
                            "test1": {"test2": {}, "test3": {}},
                            "test2": {"test1": {}},
                            "test3": {"test1": {}},
                        },
                        "_doc_metadata": {
                            "uuid": "test-network",
                            "created_at": "2022-12-08T14:56:42.891677",
                            "name": "test-network",
                            "description": "end to end test network",
                            "author": "Czar",
                            "locked": True,
                        },
                    }
                ),
            },
        )

    def post(self, request, *args, **kwargs):
        """Handle page post requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        print(request.body)

        return render(
            request,
            "node_editor.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
        )


class GameModeConfigView(OnLoadView):
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

        if game_mode_file is not None and not any(
            g["filename"] == game_mode_file for g in unfinished_game_modes
        ):
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
                "sidebar": default_sidebar,
                "toolbar": default_toolbar,
                "forms": forms,
                "form": form,
                "section": section,
                "error_message": error_message,
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
    global unfinished_game_modes
    if request.method == "POST":
        load = "reload"

        operation = request.POST.get("operation")
        item_type = request.POST.get("item_type")

        item_names = request.POST.getlist("item_names[]")
        item_ids = request.POST.getlist("item_ids[]")

        item_name = item_names[0] if item_names else None
        item_id = item_ids[0] if item_ids else None

        if item_type == "network":
            db = NetworkDB()

        if operation == "create":
            if item_type == "game mode":
                new_game_mode_path = uniquify(GAME_MODES_DIR / f"{item_name}.yaml")
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
                    "game mode config",
                    kwargs={"game_mode_file": new_game_mode_path.name},
                )
            elif item_type == "network":
                db.insert(
                    network=Network(matrix=np.asarray([]), positions=[]), name=item_name
                )

        elif operation == "delete":
            if item_type == "game mode":
                for name in item_names:
                    path = GAME_MODES_DIR / f"{name}.yaml"
                    if path.exists():
                        path.unlink()
            elif item_type == "network":
                for id in item_ids:
                    db.remove(db.get(id))

        elif operation == "create from":
            if item_type == "game mode":
                source_game_mode_path = (
                    GAME_MODES_DIR / f"{request.POST.get('source_game_mode')}.yaml"
                )
                new_game_mode_path = uniquify(GAME_MODES_DIR / f"{item_name}.yaml")
                shutil.copy(source_game_mode_path, new_game_mode_path)
                load = reverse(
                    "game mode config",
                    kwargs={"game_mode_file": new_game_mode_path.name},
                )
            elif item_type == "network":
                network = db.get(item_id)
                meta = network.doc_metadata.to_dict()
                meta["uuid"] = None
                meta["locked"] = False
                network._doc_metadata = DocMetadata(**meta)
                db.insert(network=network, name=item_name)

        print("LOAD", load)
        return JsonResponse({"load": load})
    return JsonResponse({"message:": "FAILED"}, status=400)
