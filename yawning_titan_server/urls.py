from django.urls import path
from yawning_titan_gui.views import Home,GameModes
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('game_modes/', GameModes.as_view(),name='Manage game modes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
