from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from yawning_titan_gui.views import (
    GameModeConfigView,
    GameModesView,
    HomeView,
    config_file_manager,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    path(
        "game_mode_config/<str:game_mode_file>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_file>/<str:section>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path("game_mode_config/", GameModeConfigView.as_view(), name="game mode config"),
    path("manage_files/", config_file_manager, name="file manager"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
