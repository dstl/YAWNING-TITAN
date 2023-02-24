import json

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan_gui.forms.game_mode_forms import (
    GameModeForm,
    GameModeFormManager,
    GameModeSection,
)
from yawning_titan_gui.helpers import GameModeManager

default_sidebar = {
    "Documentation": ["Getting started", "Tutorials", "How to configure", "Code"],
    "Configuration": [
        "Manage game modes",
    ],
    "Training runs": ["Setup a training run", "View completed runs"],
    "About": ["Contributors", "Report bug", "FAQ"],
}

default_toolbar = {
    "random-elements": {"icon": "bi-gear", "title": "Set random elements"},
    "network-nodes": {"icon": "bi-diagram-2", "title": "Network nodes"},
    # "run-config-set": {"icon": "bi-collection-play", "title": "Run config"},
    # "run-view": {"icon": "bi-play", "title": "Run game"},
}

protected_game_mode_ids = ["base_config.yaml"]


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
            {"sidebar": default_sidebar},
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
            {"sidebar": default_sidebar},
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
            {"sidebar": default_sidebar},
        )


class GameModesView(View):
    """Django page template for game mode management."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `game_modes.html` and the server GET / POST request bodies.
        """
        dialogue_boxes = [
            {
                "id": "delete-dialogue",
                "message": "Are you sure you want to delete the selected game modes(s)?\n\nThis action cannot be undone.",
                "actions": ["Delete game mode"],
            },
            {
                "id": "create-dialogue",
                "header": "Create new game mode",
                "message": "Enter a name for your new game mode",
                "actions": ["Create"],
                "input_prompt": "Game mode name...",
            },
            {
                "id": "create-from-dialogue",
                "header": "Create game mode from",
                "message": "Enter a name for your new game mode",
                "actions": ["Create game mode"],
                "input_prompt": "Game mode name...",
            },
        ]
        return render(
            request,
            "game_modes.html",
            {
                "sidebar": default_sidebar,
                "dialogue_boxes": dialogue_boxes,
                "game_modes": GameModeManager.get_game_mode_data(),
            },
        )


class NodeEditor(View):
    """
    Django representation of node_editor.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request: HttpRequest, *args, network_id: str = None, **kwargs):
        """Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "node_editor.html", {"sidebar": default_sidebar})

    def post(self, request: HttpRequest, *args, network_id: str = None, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return JsonResponse({"message": "success"})


class GameModeConfigView(View):
    """Django page template for game mode creation and editing."""

    def get(
        self,
        request: HttpRequest,
        *args,
        game_mode_id: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        if game_mode_id is None:
            raise (
                Http404(
                    f"Can't find game mode section {section_name} in game mode {game_mode_id}"
                )
            )

        game_mode_form = GameModeFormManager.get_or_create_form(game_mode_id)
        section = game_mode_form.get_section(section_name)
        return self.render_page(request, section, game_mode_form)

    def post(
        self,
        request: HttpRequest,
        *args,
        game_mode_id: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        game_mode_form = GameModeFormManager.get_or_create_form(game_mode_id)
        section = game_mode_form.get_section(section_name)
        if section.config_class.validation.passed:
            if (
                section_name == game_mode_form.last_section.name
                and game_mode_form.game_mode.validation.passed
            ):
                GameModeFormManager.save_as_game_mode(game_mode_form)
                return redirect("Manage game modes")
            return redirect(
                "game mode config",
                game_mode_id,
                game_mode_form.get_next_section_name(section_name),
            )
        return self.render_page(request, section, game_mode_form)

    def render_page(
        self,
        request: HttpRequest,
        section: GameModeSection,
        game_mode_form: GameModeForm,
    ):
        """
        Process pythonic tags in game_mode_config.html and return formatted page.

        :param request: the Django page `request` object containing the html data and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        :param error_message: an optional error message string to be displayed in the `#error-message` html element

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        return render(
            request,
            "game_mode_config.html",
            {
                "sections": game_mode_form.sections,
                "section": section,
                "current_section_name": section.name,
                "last": False,
                "sidebar": default_sidebar,
                "game_mode_name": game_mode_form.game_mode.doc_metadata.name,
                "protected": game_mode_form.game_mode.doc_metadata.locked,
            },
        )


def db_manager(request: HttpRequest) -> JsonResponse:
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
            game_mode = GameMode()
            GameModeManager.db.insert(game_mode=game_mode, name=item_name)
            return reverse(
                "game mode config",
                kwargs={"game_mode_id": game_mode.doc_metadata.uuid},
            )

        def delete_game_mode():
            for id in item_ids:
                GameModeManager.db.remove(GameModeManager.db.get(id))
            return "reload"

        def create_game_mode_from():
            game_mode = GameModeManager.db.get(request.POST.get("source_item_id"))
            meta = game_mode.doc_metadata.to_dict()
            meta["uuid"] = None
            meta["locked"] = False
            game_mode._doc_metadata = DocMetadata(**meta)
            GameModeManager.db.insert(game_mode=game_mode, name=item_name)
            return reverse(
                "game mode config",
                kwargs={"game_mode_id": game_mode.doc_metadata.uuid},
            )

        operations = {
            "game mode": {
                "create": create_game_mode,
                "delete": delete_game_mode,
                "create from": create_game_mode_from,
            },
        }
        try:
            return JsonResponse({"load": operations[item_type][operation]()})
        except KeyError as e:
            return JsonResponse({"message:": str(e)}, status=400)
    return JsonResponse({"message:": "FAILED"}, status=400)


def update_game_mode(request: HttpRequest) -> JsonResponse:
    """
    Update the :attribute: `edited_forms` dictionary with the current state of the config and check for errors.

    Check the current contents of the :class:`ConfigForm <yawning_titan_gui.forms.ConfigForm>` are valid
    using the criteria defined in the appropriate section of the :class:`~yawning_titan.game_modes.game_mode.GameMode`

    :param request: here the django_request object will be specifically loaded with
        `section_name`,`game_mode_id`parameters as well as the form data.

    :return: response object containing error if config is invalid or redirect parameters if valid
    """
    if request.method == "POST":
        game_mode_id = request.POST.get("_game_mode_id")
        operation = request.POST.get("_operation")
        game_mode_form = GameModeFormManager.get_or_create_form(game_mode_id)
        if operation == "save":
            GameModeFormManager.save_as_game_mode(game_mode_form)
            return JsonResponse({"message": "saved"})
        elif operation == "update":
            section_name = request.POST.get("_section_name")
            form_id = int(request.POST.get("_form_id"))
            section = game_mode_form.update_section(
                section_name=section_name, form_id=form_id, data=request.POST
            )
            if section.config_class.validation.passed:
                return JsonResponse({"message": "updated"})
            else:
                return JsonResponse(
                    {"errors": json.dumps(section.get_form_errors())}, status=400
                )
    return JsonResponse({"message": "Invalid operation"})
