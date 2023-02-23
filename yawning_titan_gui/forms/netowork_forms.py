from typing import Dict

from django import forms as django_forms
from django.forms import widgets
from django.http import QueryDict

from yawning_titan.networks.network import (
    Network,
    RandomEntryNodePreference,
    RandomHighValueNodePreference,
)
from yawning_titan_gui.forms import RangeInput
from yawning_titan_gui.helpers import NetworkManager


class NetworkForm(django_forms.Form):
    """Django form representation of a :class:`~yawning_titan.networks.network.Network`."""

    # Random node selection elements
    set_random_entry_nodes = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={
                "role": "switch",
                "class": "form-check-input inline",
                "data-toggle": "random-en",
            }
        ),
        required=False,
        help_text="Set random entry nodes",
        label="set_random_entry_nodes",
    )
    num_of_random_entry_nodes = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control", "random-en": ""}),
        required=False,
        help_text="Number of random entry nodes",
        label="Number of random entry nodes",
    )
    random_entry_node_preference = django_forms.ChoiceField(
        widget=django_forms.Select(attrs={"class": "form-control", "random-en": ""}),
        choices=(
            (t.name, t.name.replace("_", " ").capitalize())
            for t in RandomEntryNodePreference
        ),
        required=False,
        help_text="The way in which random entry nodes are chosen",
        label="Random entry node preference",
    )
    set_random_high_value_nodes = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={
                "role": "switch",
                "class": "form-check-input inline",
                "data-toggle": "random-hvn",
            }
        ),
        required=False,
        help_text="Set random high value nodes",
        label="set_random_high_value_nodes",
    )
    num_of_random_high_value_nodes = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control", "random-hvn": ""}),
        required=False,
        help_text="Number of random high value nodes",
        label="Number of random high value nodes",
    )
    random_high_value_node_preference = django_forms.ChoiceField(
        widget=django_forms.Select(attrs={"class": "form-control", "random-hvn": ""}),
        choices=(
            (t.name, t.name.replace("_", " ").capitalize())
            for t in RandomHighValueNodePreference
        ),
        required=False,
        help_text="The way in which random high value nodes are chosen",
        label="Random high value node preference",
    )
    set_random_vulnerabilities = django_forms.BooleanField(
        widget=widgets.CheckboxInput(
            attrs={
                "role": "switch",
                "class": "form-check-input inline",
                "data-toggle": "random-vuln",
            }
        ),
        required=False,
        help_text="Set vulnerabilities",
        label="set_random_vulnerabilities",
    )
    node_vulnerability_lower_bound = django_forms.FloatField(
        widget=RangeInput(
            attrs={
                "class": "form-control form-range",
                "step": "0.01",
                "random-vuln": "",
            }
        ),
        required=False,
        help_text="The lower bound of the possible vulnerabilities of a node",
        min_value=0,
        max_value=1,
        label="node_vulnerability_lower_bound",
    )
    node_vulnerability_upper_bound = django_forms.FloatField(
        widget=RangeInput(
            attrs={
                "class": "form-control form-range",
                "step": "0.01",
                "random-vuln": "",
            }
        ),
        required=False,
        help_text="The upper bound of the possible vulnerabilities of a node",
        min_value=0,
        max_value=1,
        label="node_vulnerability_upper_bound",
    )

    def __init__(
        self,
        network: Network,
        *args,
        data=None,
        **kwargs,
    ):
        self.name = network.doc_metadata.name
        self.network = network
        if data is None:
            data = network.to_dict()
        super(NetworkForm, self).__init__(*args, data=data, **kwargs)

        if self.is_bound:
            self.is_valid()
            try:
                self.network.set_from_dict(self.cleaned_data)
            except Exception as e:
                self.add_error(None, str(e))


class NetworkFormManager:
    """
    Create and manage sets of forms for a given :class: `~yawning_titan.game_modes.game_mode .GameMode`.

    allows for game modes to be constructed dynamically from the GUI.
    """

    network_forms: Dict[str, NetworkForm] = {}
    current_network_form: NetworkForm = None

    # Getters

    @classmethod
    def get_or_create_form(cls, network_id: str) -> NetworkForm:
        """
        Get or create the form for the current :param:`network_id`.

        If the game mode is from a saved yaml file set the option values to those set in the file otherwise
        set the options based off the default configuration.

        :param network_id: the file name and extension of the current game mode
        :return: a dictionary representation of the sections of the :class: `~yawning_titan.networks.network.Network`
        """
        if network_id in cls.network_forms:
            return cls.network_forms[network_id]
        else:
            network = NetworkManager.db.get(network_id)
            form = NetworkForm(network)
            cls.network_forms[network_id] = form
            return form

    # Setters

    @classmethod
    def save_as_network(cls, network_form: NetworkForm) -> Network:
        """
        Create a complete config yaml file from a dictionary of form sections.

        :param network_form: A `NetworkForm` instance

        :return: a valid instance of :class: `~yawning_titan.networks.network.Network`
        """
        if NetworkManager.db.get(network_form.network):
            # TODO add description to params
            NetworkManager.db.update(network=network_form.network)
        else:
            NetworkManager.db.insert(network=network_form.network)
        return network_form.network

    @classmethod
    def update_network_attributes(cls, network_id: str, data: QueryDict) -> NetworkForm:
        """Set the attributes of a network to reflect updates in the GUI.

        :param network_id: The uuid of a network in the database.
        :param data: The posted form data from the GUI containing details of the network attributes.
        """
        network = NetworkManager.db.get(network_id)
        form = NetworkForm(
            network=network, data=data
        )  # create a new network form an update with the new data
        if form.is_valid():
            NetworkManager.db.update(form.network)  # update the network in the database
        cls.network_forms[network_id] = form

        return form

    @classmethod
    def update_network_elements(cls, network_id: str, data: dict) -> NetworkForm:
        """Set the elements of a network to reflect updates in the GUI.

        :param network_id: The uuid of a network in the database.
        :param data: The python dictionary object containing a full representation of a network
            including nodes and edges.
        """
        form = cls.get_or_create_form(network_id)
        form.network.set_from_dict(config_dict=data)
        NetworkManager.db.update(form.network)  # update the network in the database
        return form
