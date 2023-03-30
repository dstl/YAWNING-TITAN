import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from yawning_titan.networks import network_creator
from yawning_titan_gui.forms.network_forms import NetworkFormManager, NetworkTemplateForm

from yawning_titan_gui.helpers import NetworkManager, get_toolbar


class NetworkCreator(View):
    """Django page for creating a network from a template."""

    def get(
        self,
        request: HttpRequest,
        *args,
        network_id: str = None,
        **kwargs,
    ):
        """Handle page get requests.

        Args:
            request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        network = NetworkManager.db.get(network_id)
        return render(
            request,
            "network_creator.html",
            {
                "toolbar": get_toolbar("Manage networks"),
                "form": NetworkTemplateForm(),
                "network_json": json.dumps(network.to_dict(json_serializable=True)),
                "network_name": network.doc_metadata.name,
                "network_id": network.doc_metadata.uuid,
            },
        )

    def post(
        self,
        request: HttpRequest,
        *args,
        network_id: str = None,
        **kwargs,
    ):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        creator_type = request.POST.get("type")
        if creator_type == "Mesh":
            network = network_creator.create_mesh(
                size=int(request.POST.get("size")),
                connectivity=float(request.POST.get("connectivity")),
            )
        elif creator_type == "Star":
            network = network_creator.create_star(
                first_layer_size=int(request.POST.get("first_layer_size")),
                group_size=int(request.POST.get("star_group_size")),
                group_connectivity=float(request.POST.get("star_group_connectivity")),
            )
        elif creator_type == "P2P":
            network = network_creator.create_p2p(
                inter_group_connectivity=float(
                    request.POST.get("inter_group_connectivity")
                ),
                group_size=int(request.POST.get("P2P_group_size")),
                group_connectivity=float(request.POST.get("P2P_group_connectivity")),
            )
        elif creator_type == "Ring":
            network = network_creator.create_ring(
                break_probability=float(request.POST.get("break_probability")),
                ring_size=int(request.POST.get("ring_size")),
            )
        current_network = NetworkManager.db.get(network_id)
        network._doc_metadata = (
            current_network.doc_metadata
        )  # copy the metadata from the old to the new network instance
        NetworkManager.db.update(network=network)
        network_form = NetworkFormManager.get_or_create_form(network_id)
        network_form.network = network
        return JsonResponse(
            {
                "network_json": json.dumps(network.to_dict(json_serializable=True)),
                "network_id": network.doc_metadata.uuid,
            }
        )
