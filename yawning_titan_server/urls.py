from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from yawning_titan_gui.views import GameModesView, HomeView, config_file_manager

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    # TODO: replace below HomeView's with view object for game mode config
    path(
        "game_mode_config/<str:game_mode_file>/",
        HomeView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_file>/<str:section>/",
        HomeView.as_view(),
        name="game mode config",
    ),
    path("game_mode_config/", HomeView.as_view(), name="game mode config"),
    path("manage_config/", config_file_manager, name="manage config"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
