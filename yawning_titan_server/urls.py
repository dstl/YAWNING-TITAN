from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from yawning_titan_gui.views import Home,Docs

urlpatterns = [
    path("", Home.as_view(),name="home"),
    path("docs/",Docs.as_view(),name="docs")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
