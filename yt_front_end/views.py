from django.views import View
from django.shortcuts import render

class home(View):
    def get(self, request, *args, **kwargs):
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        return self.render_page(request)

    def render_page(self, request):
        return render(
            request,
            "home.html",
        )