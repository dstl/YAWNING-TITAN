from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from yawning_titan_gui.views import (
    DocsView,
    GameModeConfigView,
    GameModesView,
    HomeView,
    NetworksView,
    NodeEditor,
    config_file_manager,
    update_config,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("docs/", DocsView.as_view(), name="docs"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    path("networks/", NetworksView.as_view(), name="Manage networks"),
    path(
        "game_mode_config/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_filename>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_filename>/<str:section_name>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path("node_editor/", NodeEditor.as_view(), name="node editor"),
    path("node_editor/<str:network_id>", NodeEditor.as_view(), name="node editor"),
    path("manage_files/", config_file_manager, name="file manager"),
    path("update_config/", update_config, name="update config"),
]

urlpatterns += staticfiles_urlpatterns()
