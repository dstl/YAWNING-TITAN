from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from yawning_titan_gui.forms.run_form import RunForm
from yawning_titan_gui.helpers import (
    GameModeManager,
    NetworkManager,
    RunManager,
    get_toolbar,
)


class RunView(View):
    """Django page template for Yawning Titan Run class."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `run.html` and the server GET / POST request bodies.
        """
        form = RunForm()

        return render(
            request,
            "run.html",
            {
                "form": form,
                "toolbar": get_toolbar("Run session"),
                "game_modes": GameModeManager.get_game_mode_data(valid_only=True),
                "networks": NetworkManager.get_network_data(),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `run.html` and the server GET / POST request bodies.
        """
        form = RunForm(request.POST)
        if form.is_valid():
            fkwargs = form.cleaned_data
            if fkwargs["network"] is not None:
                fkwargs["network"] = NetworkManager.db.get(fkwargs["network"])
            if fkwargs["game_mode"] is not None:
                fkwargs["game_mode"] = GameModeManager.db.get(fkwargs["game_mode"])
            RunManager.start_process(fkwargs=fkwargs)
            return JsonResponse({"message": "complete"})
        return JsonResponse({"message": "error"}, status=400)
