from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from yawning_titan_gui.forms.game_mode_forms import GameModeForm, GameModeFormManager, GameModeSection
from yawning_titan_gui.helpers import get_toolbar


class GameModeConfigView(View):
    """Django page template for game mode creation and editing."""

    def get(
        self,
        request: HttpRequest,
        *args,
        game_mode_id: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page get requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        if game_mode_id is None:
            raise (
                Http404(
                    f"Can't find game mode section {section_name} in game mode {game_mode_id}"
                )
            )

        game_mode_form = GameModeFormManager.get_or_create_form(game_mode_id)
        section = game_mode_form.get_section(section_name)
        return self.render_page(request, section, game_mode_form)

    def post(
        self,
        request: HttpRequest,
        *args,
        game_mode_id: str = None,
        section_name: str = None,
        **kwargs,
    ):
        """
        Handle page post requests.

        :param request: the Django page `request` object containing the html data for `game_mode_config.html` and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        game_mode_form = GameModeFormManager.get_or_create_form(game_mode_id)
        section = game_mode_form.get_section(section_name)
        if section.config_class.validation.passed:
            if (
                section_name == game_mode_form.last_section.name
                and game_mode_form.game_mode.validation.passed
            ):
                GameModeFormManager.save_as_game_mode(game_mode_form)
                return redirect("Manage game modes")
            return redirect(
                "game mode config",
                game_mode_id,
                game_mode_form.get_next_section(section),
            )
        return self.render_page(request, section, game_mode_form)

    def render_page(
        self,
        request: HttpRequest,
        section: GameModeSection,
        game_mode_form: GameModeForm,
    ):
        """
        Process pythonic tags in game_mode_config.html and return formatted page.

        :param request: the Django page `request` object containing the html data and the server GET / POST request bodies.
        :param game_mode_id: a game mode filename passed within the page url parameters
        :param section_name: the section of the config file the page was displaying; one of (red,blue,game_rules,observation_space,rewards,reset,miscellaneous)
        :param error_message: an optional error message string to be displayed in the `#error-message` html element

        :return: Html string representing an instance of the`GameModeConfigView`
        """
        return render(
            request,
            "game_mode_config.html",
            {
                "sections": game_mode_form.sections,
                "section": section,
                "doc_metadata_form": game_mode_form.doc_metadata_form,
                "current_section_name": section.name,
                "last": False,
                "toolbar": get_toolbar("Manage game modes"),
                "game_mode_name": game_mode_form.game_mode.doc_metadata.name,
                "game_mode_id": game_mode_form.game_mode.doc_metadata.uuid,
                "game_mode_description": game_mode_form.game_mode.doc_metadata.description
                if game_mode_form.game_mode.doc_metadata.description
                else "",
                "protected": game_mode_form.game_mode.doc_metadata.locked,
            },
        )
