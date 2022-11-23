from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from yawning_titan_gui.views import home

urlpatterns = [
    path("", home.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
