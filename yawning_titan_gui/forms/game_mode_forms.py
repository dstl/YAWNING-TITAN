from dataclasses import dataclass
from typing import Dict, List

from django import forms as django_forms
from django.forms import widgets

from yawning_titan.config.core import ConfigGroup, ConfigItem
from yawning_titan.config.item_types.bool_item import BoolItem
from yawning_titan.config.item_types.float_item import FloatItem
from yawning_titan.config.item_types.int_item import IntItem
from yawning_titan.game_modes.game_mode import GameMode
from yawning_titan_gui.forms import RangeInput
from yawning_titan_gui.helpers import GameModeManager, next_key


class ConfigForm(django_forms.Form):
    """
    Base class for represent yawning_titan config classes as html forms.

    - Represent float inputs using range sliders
    - Represent string inputs as text input fields
    - Represent integer inputs as number input fields
    - Represent boolean inputs as styled checkboxes
    - Represent elements that are mutually exclusive as dropdowns

    :param section: The string name of a config section in the Yawning Titan config
    :param ConfigClass: An instance of :class: `~yawning_titan.config.core.ConfigGroup` representing a
        section of the Yawning Titan config
    """

    def __init__(
        self,
        name: str,
        tier: int,
        config_class: ConfigGroup,
        fields: Dict[str, django_forms.Field],
        *args,
        **kwargs,
    ):
        self.config_class: ConfigGroup = config_class
        self.group_errors = None
        self.name = name
        self.tier = tier

        super(ConfigForm, self).__init__(*args, **kwargs)
        # created dropdowns from grouped elements
        self.fields: Dict[str, django_forms.Field] = fields
        if self.is_bound:
            self.update_and_check()

    def update_and_check(self) -> bool:
        """
        Check that config form is valid for fields and subsections.

        Overrides the `django_forms` `is_valid` method to add checks for field values dependent
        on other fields.

        :return: A bool value True if the form meets the validation criteria and produces a valid
            section of the config group.
        """
        super().is_valid()  # noqa: F841

        self.config_class.set_from_dict(self.cleaned_data)

        if self.config_class.validation.passed:
            return True
        else:
            for k, i in self.config_class.get_config_elements(ConfigItem).items():
                for error in i.validation.fail_reasons:
                    self.add_error(k, error)

        self.group_errors = self.config_class.validation.fail_reasons
        return False


class GameModeSection:
    """
    A representation of a section of a :class: `~yawning_titan.game_modes.game_mode.GameMode`.

    Each group within the section has its items converted into a django form element and is assigned
    an icon string representing a bootstrap icon.
    """

    def __init__(
        self, section: ConfigGroup = None, form_name: str = None, icon: str = None
    ) -> None:
        self.forms: List[ConfigForm] = []
        self.form_classes: List[ConfigForm] = []
        self.icon = icon
        self.config_class = section
        self.name = form_name
        self.create_form_from_group(section, form_name=form_name)

    def create_form_from_group(
        self, group: ConfigGroup, form_name: str = "", tier: int = 0
    ):
        """Create a representation of a single :class: `~yawning_titan.config.core.ConfigGroup` element as a django form.

        :param group: A config group object
        :param form_name: The name of the group/form element
        :param tier: The nested level of the group element which is also used to set the indentation level in the gui
        """
        field_elements = {}
        for name, e in group.get_config_elements(ConfigItem).items():
            if isinstance(e, BoolItem):
                el = django_forms.BooleanField(
                    widget=widgets.CheckboxInput(
                        attrs={"role": "switch", "class": "form-check-input"}
                    ),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            elif isinstance(e, FloatItem):
                el = django_forms.FloatField(
                    widget=RangeInput(attrs={"class": "form-control", "step": "0.01"}),
                    required=False,
                    help_text=e.doc,
                    min_value=e.properties.min_val,
                    max_value=e.properties.max_val,
                    label=name,
                )
            elif isinstance(e, IntItem):
                el = django_forms.IntegerField(
                    widget=widgets.NumberInput(attrs={"class": "form-control"}),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            else:
                el = django_forms.CharField(
                    widget=widgets.TextInput(attrs={"class": "form-control"}),
                    required=False,
                    help_text=e.doc,
                    label=name,
                )
            field_elements[name] = el

        class ConfigFormSubsection(ConfigForm):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    form_name, tier, group, field_elements, *args, **kwargs
                )

        self.form_classes.append(ConfigFormSubsection)
        self.forms.append(ConfigFormSubsection(data=group.to_dict(values_only=True)))

        for name, e in group.get_config_elements(ConfigGroup).items():
            self.create_form_from_group(e, form_name=name, tier=tier + 1)

    def get_form_errors(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Create a formatted dictionary of the errors in each of the forms that constitute the game mode section.

        The 'group' errors are the errors for each of the constituent groups in the game mode.
        The 'items' errors are the errors attribute to each item with the group.

        only groups where either group specific errors exist or where an item element within the group has failed
        will be included in the output. This excludes groups that have failed due to a child group failing.

        :return: a dict.
        """
        self.config_class.validate()
        return {
            i: {
                "group": form.config_class.validation.fail_reasons,
                "items": {
                    k: v.fail_reasons
                    for k, v in form.config_class.validation.element_validation.items()
                },
            }
            for i, form in enumerate(self.forms)
            if not form.config_class.validation.group_passed
            or any(
                not item.validation.passed
                for item in form.config_class.get_config_elements(ConfigItem).values()
            )
        }


@dataclass
class GameModeForm:
    """A representation of a :class: `~yawning_titan.game_modes.game_mode.GameMode` as a editable form."""

    game_mode: GameMode

    def __post_init__(self) -> None:
        """Initialise the individual sections representing all descendent :class:`~yawning_titan.config.core.ConfigGroup`'s."""
        self.sections: Dict[str, GameModeSection] = {
            "red": GameModeSection(
                section=self.game_mode.red, form_name="red", icon="bi-lightning"
            ),
            "blue": GameModeSection(
                section=self.game_mode.red, form_name="blue", icon="bi-shield"
            ),
            "game_rules": GameModeSection(
                section=self.game_mode.red, form_name="game_rules", icon="bi-clipboard"
            ),
            "observation_space": GameModeSection(
                section=self.game_mode.red,
                form_name="observation_space",
                icon="bi-binoculars",
            ),
            "rewards": GameModeSection(
                section=self.game_mode.red, form_name="rewards", icon="bi-star"
            ),
            "on_reset": GameModeSection(
                section=self.game_mode.red,
                form_name="on_reset",
                icon="bi-arrow-clockwise",
            ),
            "miscellaneous": GameModeSection(
                section=self.game_mode.red, form_name="miscellaneous", icon="bi-brush"
            ),
        }

    def get_section(self, section_name: str = None) -> GameModeSection:
        """
        Get a specific :param:`section` of the form.

        :param section_name: the name of the section to get from which to retrieve the value of
        :return: a dictionary containing status and :class:`ConfigForm` of the selected :param:`section_name`
        """
        if section_name is None:
            return self.first_section
        return self.sections[section_name]

    def get_next_section_name(self, section_name=None) -> str:
        """
        Get a specific :param:`section` of a form for an active :param:`game_mode_id`.

        :param game_mode_id: the file name and extension of the current game mode
        :param section_name: the name of the section to get from which to retrieve the value of
        :return: a dictionary containing status and :class:`ConfigForm` of the selected :param:`section_name`
        """
        if section_name is None:
            return self.first_section

        return next_key(self.sections, section_name)

    def update_section(
        self, section_name: str, form_id: int, data: dict
    ) -> GameModeSection:
        """
        Update the values of a specific component form within a section of the overall game mode form.

        :param section_name: the name of the section for which the values will be updated
        :param form_id: the integer index of the form of the group component to update.
        :param data: a dictionary representation of config form values to use to update the reference for an active :param: `game_mode_id`
        :return: the :param:`section` of the active :param: `game_mode_id` with values updated from :param:`data`
        """
        section = self.get_section(section_name)
        section.forms[form_id] = section.form_classes[form_id](data=data)
        # section.forms[form_id].update_and_check()
        section.config_class.validate()
        return section

    @property
    def first_section(self) -> GameModeSection:
        """Return the first of the game mode sections."""
        return list(self.sections.values())[0]

    @property
    def last_section(self) -> GameModeSection:
        """Return the last of the game mode sections."""
        return list(self.sections.values())[-1]


class GameModeFormManager:
    """
    Create and manage sets of forms for a given :class: `~yawning_titan.game_modes.game_mode.GameMode`.

    allows for game modes to be constructed dynamically from the GUI.
    """

    game_mode_forms: Dict[str, GameModeForm] = {}

    # Getters

    @classmethod
    def get_or_create_form(cls, game_mode_id) -> GameModeForm:
        """
        Get or create the config forms for the current :param:`game_mode_id`.

        If the game mode is from a saved yaml file set the option values to those set in the file otherwise
        set the options based off the default configuration.

        Set the status of the game mode sections based upon whether they pass the validation rules in their corresponding
        :class: `~yawning_titan.config.core.ConfigGroup`

        :param game_mode_filename: the file name and extension of the current game mode
        :return: a dictionary representation of the sections of the :class: `~yawning_titan.game_modes.game_mode.GameMode`
        """
        if game_mode_id in cls.game_mode_forms:
            return cls.game_mode_forms[game_mode_id]
        else:
            form = GameModeForm(GameModeManager.db.get(game_mode_id))
            cls.game_mode_forms[game_mode_id] = form
            return form

    # Setters

    @classmethod
    def save_as_game_mode(cls, game_mode_form: GameModeForm) -> GameMode:
        """
        Create a complete config yaml file from a dictionary of form sections.

        :param game_mode_forms: dictionary containing django form objects representing sections of the config.

        :return: a valid instance of :class: `~yawning_titan.game_modes.game_mode.GameMode`
        """
        if GameModeManager.db.get(game_mode_form.game_mode.doc_metadata.uuid):
            # TODO add description to params
            if not GameModeManager.db.get(
                game_mode_form.game_mode.doc_metadata.uuid
            ).doc_metadata.locked:
                GameModeManager.db.update(game_mode=game_mode_form.game_mode)
        else:
            GameModeManager.db.insert(game_mode=game_mode_form.game_mode)
        return game_mode_form.game_mode
