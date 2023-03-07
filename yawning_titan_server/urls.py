from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from yawning_titan_gui.views import (
    DocsView,
    GameModeConfigView,
    GameModesView,
    HomeView,
    NetworkCreator,
    NetworksView,
    NodeEditor,
    RunView,
    db_manager,
    update_game_mode,
    update_network,
    get_output
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("docs/", DocsView.as_view(), name="docs"),
    path("run/", RunView.as_view(), name="run"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    path("networks/", NetworksView.as_view(), name="Manage networks"),
    path("network_creator", NetworkCreator.as_view(), name="network creator"),
    path(
        "network_creator/<str:network_id>/",
        NetworkCreator.as_view(),
        name="network creator",
    ),
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
    path("node_editor/<str:network_id>", NodeEditor.as_view(), name="node editor"),
    path("manage_db/", db_manager, name="db manager"),
    path("update_game_mode/", update_game_mode, name="update config"),
    path("update_network/", update_network, name="update network"),
    path("output/", get_output, name="stderr"),
]

urlpatterns += staticfiles_urlpatterns()
