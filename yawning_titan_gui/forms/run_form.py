from typing import Dict

from django import forms as django_forms
from django.forms import widgets

from yawning_titan_gui.forms import RangeInput


class RunForm(django_forms.Form):
    """Django form to represent options required by the :class: `~yawning_titan.yawning_titan_run.YawningTitanRun`."""

    deterministic = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={"role": "switch", "class": "form-check-input"}
        ),
        required=False,
        label="Deterministic",
        help_text="Whether the evaluation should use stochastic or deterministic actions",
    )
    save = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={"role": "switch", "class": "form-check-input"}
        ),
        required=False,
        label="Save trained agent",
        help_text="Saves the trained agent using the stable_baselines3 save as zip functionality.",
    )
    export = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={"role": "switch", "class": "form-check-input"}
        ),
        required=False,
        label="Export run",
        help_text="Export the YawningTitanRun as a zip.",
    )
    total_timesteps = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=False,
        help_text="The number of samples (env steps) to train on",
        label="Total timesteps",
    )
    training_runs = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=False,
        help_text="The number of times the agent is trained",
        label="Training runs",
    )
    n_eval_episodes = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=False,
        help_text="The number of episodes to evaluate the agent",
        label="N eval episodes",
    )
    verbose = django_forms.FloatField(
        widget=RangeInput(attrs={"class": "form-control", "step": "1"}),
        required=False,
        help_text="The verbosity level of the logged output",
        min_value=0,
        max_value=2,
        label="Verbosity level",
    )

    render = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={"role": "switch", "class": "form-check-input"}
        ),
        required=False,
        label="Render gif",
        help_text="Whether the output should render a gif action loop",
    )
    num_episodes = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=False,
        help_text="The number of episodes to run",
        label="Number of episodes",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        hidden_field_elements = {}
        hidden_fields = ["network", "game_mode"]

        for field_name in hidden_fields:
            hidden_field_elements[field_name] = django_forms.CharField(
                widget=django_forms.HiddenInput()
            )

        self.fields.update(hidden_field_elements)

    @property
    def evaluation_fields(self):
        return {k: v for k, v in self.fields.items() if k in ["render", "num_episodes"]}

    @property
    def training_fields(self):
        return {
            k: v
            for k, v in self.fields.items()
            if k
            in ["deterministic", "total_timesteps", "training_runs", "n_eval_episodes"]
        }
