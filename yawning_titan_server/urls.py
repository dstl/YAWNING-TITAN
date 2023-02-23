from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from yawning_titan_gui.views import (
    DocsView,
    GameModeConfigView,
    GameModesView,
    HomeView,
    NodeEditor,
    db_manager,
    update_game_mode,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("docs/", DocsView.as_view(), name="docs"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    path(
        "game_mode_config/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_id>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_id>/<str:section_name>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path("node_editor/", NodeEditor.as_view(), name="node editor"),
    path("manage_db/", db_manager, name="db manager"),
    path("update_game_mode/", update_game_mode, name="update config"),
]

urlpatterns += staticfiles_urlpatterns()
