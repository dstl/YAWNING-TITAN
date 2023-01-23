import json

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from yawning_titan_gui.forms import ConfigForm, GameModeFormManager, GameModeSection
from yawning_titan_gui.helpers import GameModeManager

GameModeManager.load_game_modes(
    info_only=True
)  # pull all game modes from GAME_MODES_DIR

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

protected_game_mode_filenames = ["base_config.yaml"]


class HomeView(View):
    """Django page template for landing page."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `home.html` and the server GET / POST request bodies.
        """
        return self.render_page(request)

    def render_page(self, request: HttpRequest):
        """Process pythonic tags in home.html and return formatted page."""
        return render(
            request,
            "home.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
        )


class DocsView(View):
    """
    Django representation of home.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(
            request,
            "docs.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
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





class GameModesView(View):
    """Django page template for game mode management."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        return render(
            request,
            "game_modes.html",
            {"sidebar": default_sidebar, "game_modes": GameModeManager.game_modes},
        )


class GameModeConfigView(View):
    """Django page template for game mode creation and editing."""

    def get(
        self,
        request: HttpRequest,
        *args,
        game_mode_filename: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_filename: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        if game_mode_filename is None:
            raise (
                Http404(
                    f"Can't find game mode section {section_name} in game mode {game_mode_filename}"
                )
            )

        section: GameModeSection = GameModeFormManager.get_section(
            game_mode_filename, section_name
        )

        return self.render_page(request, section, game_mode_filename)

    def post(
        self,
        request: HttpRequest,
        *args,
        game_mode_filename: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_filename: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        section: GameModeSection = GameModeFormManager.get_section(
            game_mode_filename, section_name
        )
        game_mode_sections = GameModeFormManager.get_or_create_instance(
            game_mode_filename
        )

        if section.config_class.validation.passed:
            if section_name == list(game_mode_sections.keys())[
                -1
            ] and GameModeFormManager.check_game_mode_complete(game_mode_filename):
                GameModeFormManager.save_as_game_mode(game_mode_filename)
                return redirect("Manage game modes")
            return redirect(
                "game mode config",
                game_mode_filename,
                GameModeFormManager.get_next_section_name(
                    game_mode_filename, section_name
                ),
            )
        return self.render_page(request, section, game_mode_filename)

    def render_page(
        self,
        request: HttpRequest,
        section: ConfigForm,
        game_mode_filename: str,
    ):
        """
        Process pythonic tags in game_mode_config.html and return formatted page.

        :param request: the Django page `request` object containing the html data and the server GET / POST request bodies.
        :param game_mode_filename: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        :param error_message: an optional error message string to be displayed in the `#error-message` html element

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        return render(
            request,
            "game_mode_config.html",
            {
                "sections": GameModeFormManager.get_or_create_instance(
                    game_mode_filename
                ),
                "section": section,
                "current_section_name": section.name,
                "last": False,
                "sidebar": default_sidebar,
                "game_mode_filename": game_mode_filename,
                "protected": game_mode_filename in protected_game_mode_filenames,
            },
        )


def config_file_manager(request: HttpRequest) -> JsonResponse:
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
