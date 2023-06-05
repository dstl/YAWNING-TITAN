import traceback

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan_gui.forms.game_mode_forms import GameModeSearchForm
from yawning_titan_gui.views.utils.helpers import GameModeManager, get_toolbar


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
                "toolbar": get_toolbar("Manage game modes"),
                "item_type": "game_mode",
                "dialogue_boxes": dialogue_boxes,
                "game_modes": GameModeManager.get_game_mode_data(),
                # "search_form": GameModeSearchForm(),
                "game_mode": GameMode(),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page get requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        search_form = GameModeSearchForm(request.POST)
        try:
            if search_form.is_valid():
                if search_form.filters:
                    game_modes = GameModeManager.filter(search_form.filters)
                else:
                    game_modes = GameModeManager.db.all()
                return JsonResponse(
                    {"item_ids": [g.doc_metadata.uuid for g in game_modes]}
                )
        except Exception as e:
            print("ERR", e, traceback.print_exc())
        return JsonResponse({"message": search_form.errors}, status=500)
