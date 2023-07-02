from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView

from yawning_titan_gui.views.docs_view import DocsView
from yawning_titan_gui.views.game_mode_config_view import GameModeConfigView
from yawning_titan_gui.views.game_modes_view import GameModesView
from yawning_titan_gui.views.home_view import HomeView
from yawning_titan_gui.views.jupyter_view import JupyterView
from yawning_titan_gui.views.network_creator_view import NetworkCreator
from yawning_titan_gui.views.network_editor_view import NetworkEditor
from yawning_titan_gui.views.networks_view import NetworksView
from yawning_titan_gui.views.run_view import RunView
from yawning_titan_gui.views.utils.helpers import get_docs_sections
from yawning_titan_gui.views.utils.update_network_layout import update_network_layout
from yawning_titan_gui.views.utils.utils import db_manager, get_output, update_game_mode

urlpatterns = [
    path("", HomeView.as_view(), name="Home"),
    path("docs/", DocsView.as_view(), name="docs"),
    path("run/", RunView.as_view(), name="Run session"),
    path("docs/", DocsView.as_view(), name="Documentation"),
    path("jupyter/", JupyterView.as_view(), name="Jupyter Notebooks"),
    path("docs/<str:section>/", DocsView.as_view(), name="Documentation"),
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
    path("network_editor/", NetworkEditor.as_view(), name="network editor"),
    path("update_network_layout/", update_network_layout, name="update network layout"),
    path(
        "network_editor/<str:network_id>",
        NetworkEditor.as_view(),
        name="network editor",
    ),
    path("manage_db/", db_manager, name="db manager"),
    path("update_game_mode/", update_game_mode, name="update config"),
    path("output/", get_output, name="stderr"),
    path(
        "docs/index.html",
        TemplateView.as_view(template_name="docs/index.html"),
        name="docs index",
    ),
]

urlpatterns += [
    path(
        f"docs/source/{name}.html",
        TemplateView.as_view(template_name=f"docs/source/{name}.html"),
        name=f"docs_{name}",
    )
    for name in get_docs_sections()
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += staticfiles_urlpatterns("docs/_images")
urlpatterns += staticfiles_urlpatterns("docs/_modules")
urlpatterns += staticfiles_urlpatterns("docs/_sources")
urlpatterns += staticfiles_urlpatterns("docs/_static")
