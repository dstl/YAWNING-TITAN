from django.shortcuts import render
from django.views import View


class home(View):
    """
    Django representation of home.html.

    implements 'get' and 'post' methods to handle page requests.
    """

    def get(self, request, *args, **kwargs):
        """Handle page get requests."""
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        """Handle page post requests."""
        return self.render_page(request)

    def render_page(self, request):
        """Process pythonic tags in home.html and return formatted page."""
        return render(
            request,
            "home.html",
        )
