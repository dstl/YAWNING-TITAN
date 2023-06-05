import json
from io import StringIO

from django.http import HttpRequest, JsonResponse

from yawning_titan.networks.network import Network, NetworkLayout


def update_network_layout(request: HttpRequest) -> JsonResponse:
    """Updates the Network Layout."""
    body_dict = {}

    try:
        body = request.body.decode("utf-8")
        io = StringIO(body)
        body_dict: dict = json.load(io)
    except Exception:  # noqa
        return JsonResponse({"errors": "Unable to parse request"}, status=400)

    if body_dict.get("network") is None:
        return JsonResponse({"errors": "No network provided"}, status=400)

    if body_dict.get("layout") is None:
        return JsonResponse({"errors": "No network layout provided"}, status=400)

    # parse network
    network = Network()
    network.set_from_dict(body_dict["network"])
    network.set_node_positions(NetworkLayout(body_dict["layout"]))

    return JsonResponse(network.to_dict(json_serializable=True))
