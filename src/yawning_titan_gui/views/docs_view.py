from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from yawning_titan_gui.helpers import get_toolbar


class DocsView(View):
    """
    Django representation of home.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request: HttpRequest, *args, section: str = None, **kwargs):
        """
        Handle page get requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        doc_url = reverse(f"docs_{section}") if section else reverse("docs index")
        return render(
            request,
            "docs.html",
            {
                "toolbar": get_toolbar("Documentation"),
                "doc_url": doc_url,
            },
        )

    def post(self, request: HttpRequest, *args, section: str = None, **kwargs):
        """Handle page post requests.

        :param request: A Django `request` object that contains the data passed from
            the html page. A `request` object will always be delivered when a page
            object is accessed.
        """
        return render(request, "docs.html", {"toolbar": get_toolbar("Documentation")})
