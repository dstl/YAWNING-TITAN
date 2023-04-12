from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from yawning_titan_gui.helpers import get_toolbar, open_jupiter_notebook

class JupyterView(View):
    """
    Django representation of jupyter.html.

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
            "jupyter.html",
            {
                "notebook_url": open_jupiter_notebook(),
                "toolbar": get_toolbar("Jupyter notebooks"),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(
            request, "jupyter.html", {"toolbar": get_toolbar("Jupyter notebooks")}
        )
