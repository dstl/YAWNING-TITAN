from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from yawning_titan_gui.forms.network_forms import NetworkSearchForm

from yawning_titan_gui.helpers import NetworkManager, get_toolbar


class NetworksView(View):
    """Django page template for network management."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle page get requests.

        :param: request: the Django page `request` object containing the html data for `networks.html` and the server GET / POST request bodies.
        """
        networks = NetworkManager.db.all()

        dialogue_boxes = [
            {
                "id": "delete-dialogue",
                "message": "Are you sure you want to delete the selected network(s)?\n\nThis action cannot be undone.",
                "actions": ["Delete network"],
            },
            {
                "id": "create-dialogue",
                "header": "Create new network",
                "message": "Enter a name for your new network",
                "actions": ["Template network", "Custom network"],
                "input_prompt": "Network name...",
            },
            {
                "id": "create-from-dialogue",
                "header": "Create network from",
                "message": "Enter a name for your new network",
                "actions": ["Create network"],
                "input_prompt": "Network name...",
            },
        ]
        return render(
            request,
            "networks.html",
            {
                "toolbar": get_toolbar("Manage networks"),
                "item_type": "network",
                "networks": [network.doc_metadata for network in networks],
                "search_form": NetworkSearchForm(),
                "dialogue_boxes": dialogue_boxes,
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page get requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        search_form = NetworkSearchForm(request.POST)
        if search_form.is_valid():
            if search_form.filters:
                networks = NetworkManager.filter(search_form.filters)
            else:
                networks = [n.doc_metadata.uuid for n in NetworkManager.db.all()]
            return JsonResponse({"item_ids": networks})

        return JsonResponse({"message": search_form.errors})
