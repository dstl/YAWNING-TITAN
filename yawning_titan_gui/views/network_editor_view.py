from io import StringIO
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from yawning_titan_gui.forms.network_forms import NetworkFormManager
from yawning_titan_gui.helpers import get_toolbar


class NetworkEditor(View):
    """
    Django representation of network_editor.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request: HttpRequest, *args, network_id: str = None, **kwargs):
        """Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        network_form = NetworkFormManager.get_or_create_form(network_id)
        return render(
            request,
            "network_editor.html",
            {
                "toolbar": get_toolbar("Manage networks"),
                "form": network_form,
                "doc_metadata_form": network_form.doc_metadata_form,
                "protected": network_form.network.doc_metadata.locked,
                "network_id": network_id,
                "network_json": json.dumps(
                    network_form.network.to_dict(json_serializable=True)
                ),
            },
        )

    def post(self, request: HttpRequest, *args, network_id: str = None, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        body = request.body.decode("utf-8")
        io = StringIO(body)
        dict_n: dict = json.load(io)

        # find network id as not passed
        network_id = dict_n["_doc_metadata"]["uuid"]

        NetworkFormManager.update_network_elements(network_id, dict_n)
        return JsonResponse({"message": "success"})
