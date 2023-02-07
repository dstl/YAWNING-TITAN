import json

import numpy as np
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.networks.network import Network
from yawning_titan_gui.forms import ConfigForm, GameModeFormManager, GameModeSection
from yawning_titan_gui.helpers import GameModeManager, NetworkManager

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


class NetworksView(View):
    """Django page template for network management."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `networks.html` and the server GET / POST request bodies.
        """
        networks = NetworkManager.network_db.all()
        print(networks[0].high_value_nodes.nodes)
        range_bound_items = [
            {
                "name": "entry_nodes",
                "min": min(
                    [
                        len(network.entry_nodes.nodes)
                        if network.entry_nodes.nodes
                        else None
                        for network in networks
                    ]
                ),
                "max": max(
                    [
                        len(network.entry_nodes.nodes)
                        if network.entry_nodes.nodes
                        else None
                        for network in networks
                    ]
                ),
            },
            {
                "name": "high_value_nodes",
                "min": min(
                    [
                        len(network.high_value_nodes.nodes)
                        if network.high_value_nodes.nodes
                        else None
                        for network in networks
                    ]
                ),
                "max": max(
                    [
                        len(network.high_value_nodes.nodes)
                        if network.high_value_nodes.nodes
                        else None
                        for network in networks
                    ]
                ),
            },
            {
                "name": "network_nodes",
                "min": min([len(network.matrix[0]) for network in networks]),
                "max": max([len(network.matrix[0]) for network in networks]),
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

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return JsonResponse(
            {
                "ids": NetworkManager.filter(
                    request.POST.get("attribute"),
                    request.POST.get("min"),
                    request.POST.get("max"),
                )
            }
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

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(
            request,
            "node_editor.html",
            {"sidebar": default_sidebar, "toolbar": default_toolbar},
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
    if request.method == "POST":
        operation = request.POST.get("operation")
        item_type = request.POST.get("item_type")

        item_names = request.POST.getlist("item_names[]")
        item_ids = request.POST.getlist("item_ids[]")

        item_name = item_names[0] if item_names else None
        # item_id = item_ids[0] if item_ids else None

        def create_game_mode():
            GameModeManager.create_game_mode(f"{item_name}.yaml")
            return reverse(
                "game mode config",
                kwargs={"game_mode_filename": f"{item_name}.yaml"},
            )

        def create_network():
            network = NetworkManager.network_db.insert(
                network=Network(matrix=np.asarray([]), positions=[]), name=item_name
            )
            return reverse(
                "node editor",
                kwargs={"network_id": network.doc_metadata.uuid},
            )

        def delete_game_mode():
            GameModeManager.delete_game_mode(f"{item_name}.yaml")
            return "reload"

        def delete_network():
            for id in item_ids:
                NetworkManager.network_db.remove(NetworkManager.network_db.get(id))
            return "reload"

        def create_game_mode_from():
            GameModeManager.create_game_mode_from(
                f"{request.POST.get('source_game_mode')}.yaml", f"{item_name}.yaml"
            )
            return reverse(
                "game mode config",
                kwargs={"game_mode_filename": f"{item_name}.yaml"},
            )

        def create_network_from():
            network = NetworkManager.network_db.get(request.POST.get("source_item_id"))
            meta = network.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            network._doc_metadata = DocMetadata(**meta)
            NetworkManager.network_db.insert(network=network, name=item_name)
            return "reload"

        operations = {
            "game mode": {
                "create": create_game_mode,
                "delete": delete_game_mode,
                "create from": create_game_mode_from,
            },
            "network": {
                "create": create_network,
                "delete": delete_network,
                "create from": create_network_from,
            },
        }
        try:
            return JsonResponse({"load": operations[item_type][operation]()})
        except KeyError as e:
            return JsonResponse({"message:": str(e)}, status=400)
    return JsonResponse({"message:": "FAILED"}, status=400)


def update_config(request: HttpRequest) -> JsonResponse:
    """
    Update the :attribute: `edited_forms` dictionary with the current state of the config and check for errors.

    Check the current contents of the :class:`ConfigForm <yawning_titan_gui.forms.ConfigForm>` are valid
    using the criteria defined in the appropriate section of the :class:`GameModeConfig <yawning_titan.game_modes.game_mode _config.GameModeConfig>`

    :param request:  here the django_request object will be specifically loaded with
        `section_name`,`game_mode_filename`parameters.

    :return: response object containing error if config is invalid or redirect parameters if valid
    """
    if request.method == "POST":
        game_mode_filename = request.POST.get("_game_mode_filename")
        operation = request.POST.get("_operation")
        if operation == "save":
            GameModeFormManager.save_as_game_mode(game_mode_filename)
            return JsonResponse({"message": "saved"})
        elif operation == "update":
            section_name = request.POST.get("_section_name")
            form_id = int(request.POST.get("_form_id"))
            section: GameModeSection = GameModeFormManager.update_section(
                game_mode_filename, section_name, form_id, request.POST
            )
            if section.config_class.validation.passed:
                return JsonResponse({"message": "updated"})
            else:
                return JsonResponse(
                    {"errors": json.dumps(section.get_form_errors())}, status=400
                )
    return JsonResponse({"message": "Invalid operation"})
