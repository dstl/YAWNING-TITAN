import json

from django.http import HttpRequest, JsonResponse
from django.urls import reverse

from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan.networks.network import Network
from yawning_titan_gui.forms.game_mode_forms import GameModeFormManager
from yawning_titan_gui.helpers import GameModeManager, NetworkManager, RunManager

default_sidebar = {
    "Documentation": ["Getting started", "Tutorials", "How to configure", "Code"],
    "Configuration": [
        "Manage game modes",
    ],
    "Training runs": ["Setup a training run", "View completed runs"],
    "About": ["Contributors", "Report bug", "FAQ"],
}

default_toolbar = {
    "home": {"icon": "bi-house-door", "title": "Home"},
    "doc": {"icon": "bi-file-earmark", "title": "Documentation"},
    "manage_game_modes": {"icon": "bi-gear", "title": "Manage game modes"},
    "manage_networks": {"icon": "bi-diagram-2", "title": "Manage networks"},
    "run-view": {"icon": "bi-play", "title": "Run session"},
}

protected_game_mode_ids = ["base_config.yaml"]

run_config = {}


def get_output(request: HttpRequest):
    """Get the output of a :class: `~yawning_titan.yawning_titan_run.YawningTitanRun`."""
    if request.method == "GET":
        return JsonResponse(RunManager.get_output())


def db_manager(request: HttpRequest) -> JsonResponse:
    """
    Create, edit, delete config yaml files.

    Extract `operation`,`game_mode_name` and optional `source_game_mode` from POST request body and
    use the information to perform the appropriate alteration to the
    game mode files contained in the `GAME_MODES_DIR`.

    :param request: here the django_request object will be specifically loaded with
        `operation`,`game_mode_name` and optional `source_game_mode` parameters.

    :return:
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

        def create_network():
            network = NetworkManager.db.insert(network=Network(), name=item_name)
            return reverse(
                "network editor",
                kwargs={"network_id": network.doc_metadata.uuid},
            )

        def create_template_network():
            network = NetworkManager.db.insert(network=Network(), name=item_name)
            return reverse(
                "network creator",
                kwargs={"network_id": network.doc_metadata.uuid},
            )

        def delete_game_mode():
            for id in item_ids:
                GameModeManager.db.remove(GameModeManager.db.get(id))
            return "reload"

        def delete_network():
            for id in item_ids:
                NetworkManager.db.remove(NetworkManager.db.get(id))
            return "reload"

        def create_game_mode_from():
            game_mode = GameModeManager.db.get(request.POST.get("source_item_id"))
            game_mode._doc_metadata = DocMetadata()
            GameModeManager.db.insert(game_mode=game_mode, name=item_name)
            return reverse(
                "game mode config",
                kwargs={"game_mode_id": game_mode.doc_metadata.uuid},
            )

        def create_network_from():
            network = NetworkManager.db.get(request.POST.get("source_item_id"))
            network._doc_metadata = DocMetadata()
            NetworkManager.db.insert(network=network, name=item_name)
            return reverse(
                "network editor",
                kwargs={"network_id": network.doc_metadata.uuid},
            )

        operations = {
            "game_mode": {
                "create": create_game_mode,
                "delete": delete_game_mode,
                "create from": create_game_mode_from,
            },
            "network": {
                "create": create_network,
                "delete": delete_network,
                "create from": create_network_from,
                "template": create_template_network,
            },
        }
        try:
            return JsonResponse({"load": operations[item_type][operation]()})
        except KeyError as e:
            return JsonResponse({"message:": str(e)}, status=400)
    elif request.method == "GET":
        print([n.doc_metadata.uuid for n in NetworkManager.db.all()])
        network = NetworkManager.db.get(request.GET.get("network_id"))
        game_modes = [
            g.doc_metadata.uuid
            for g in GameModeManager.get_game_modes_compatible_with(network)
        ]
        return JsonResponse({"game_mode_ids": game_modes})
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
            if section_name == "doc-meta":
                game_mode_form.update_doc_meta(data=request.POST)
            form_id = int(request.POST.get("_form_id"))
            section = game_mode_form.update_section(
                section_name=section_name, form_id=form_id, data=request.POST
            )
            if game_mode_form.game_mode.validation.passed:
                return JsonResponse(
                    {"valid": game_mode_form.game_mode.validation.passed}
                )  # whether the complete game mode is valid
            else:
                return JsonResponse(
                    {"errors": json.dumps(section.get_form_errors())}, status=400
                )
    return JsonResponse({"message": "Invalid operation"})
