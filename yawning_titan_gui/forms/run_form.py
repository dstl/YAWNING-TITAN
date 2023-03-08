from typing import Dict

from django import forms as django_forms
from django.forms import widgets


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

    render = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={"role": "switch", "class": "form-check-input"}
        ),
        required=False,
        label="Render gif",
        help_text="Whether the output should render a gif action loop",
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
