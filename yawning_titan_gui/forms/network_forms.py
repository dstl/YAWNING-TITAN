from typing import Dict

from django import forms as django_forms
from django.conf import settings
from django.forms import widgets
from django.http import QueryDict

from yawning_titan.networks.network import (
    Network,
    RandomEntryNodePreference,
    RandomHighValueNodePreference,
)
from yawning_titan_gui.forms import RangeInput, create_doc_meta_form
from yawning_titan_gui.helpers import NetworkManager


class NetworkTemplateForm(django_forms.Form):
    """Form to contain the options for creating a network from a template."""

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(NetworkTemplateForm, self).__init__(*args, **kwargs)

        types = {
            "Mesh": {
                "float": [
                    {
                        "label": "connectivity",
                        "description": "The number of nodes to include in the network",
                    }
                ],
                "int": [
                    {
                        "label": "size",
                        "description": "The amount of connections between the nodes. (smaller values mean the connections or more sparse).",
                    }
                ],
            },
            "Star": {
                "float": [
                    {
                        "label": "star_group_connectivity",
                        "description": "The amount of connections between the groups. (smaller values mean the connections or more sparse).",
                    }
                ],
                "int": [
                    {
                        "label": "first_layer_size",
                        "description": "The number of nodes to include in the first layer",
                    },
                    {
                        "label": "star_group_size",
                        "description": "The number of nodes to include in the groups",
                    },
                ],
            },
            "P2P": {
                "float": [
                    {
                        "label": "inter_group_connectivity",
                        "description": "The amount of connections between the groups. (smaller values mean the connections or more sparse).",
                    },
                    {
                        "label": "P2P_group_connectivity",
                        "description": "The amount of connections within the groups. (smaller values mean the connections or more sparse).",
                    },
                ],
                "int": [
                    {
                        "label": "P2P_group_size",
                        "description": "The number of nodes to include in the groups",
                    }
                ],
            },
            "Ring": {
                "float": [
                    {
                        "label": "break_probability",
                        "description": "The likelihood of a break in the connections of the ring.",
                    }
                ],
                "int": [
                    {
                        "label": "ring_size",
                        "description": "The number of nodes to include in the ring",
                    }
                ],
            },
        }

        field_elements = {}
        field_elements["type"] = django_forms.ChoiceField(
            widget=django_forms.Select(
                attrs={"class": "form-control form-select", "type-selector": ""}
            ),
            choices=((t, t) for t in types.keys()),
            required=True,
            help_text="The type of network to create",
            label="Type",
        )

        for name, items in types.items():
            for float_item in items["float"]:
                field_elements[float_item["label"]] = django_forms.FloatField(
                    widget=RangeInput(
                        attrs={
                            "class": "form-control form-range slider-progress " + name,
                            "step": "0.01",
                        }
                    ),
                    required=False,
                    help_text=float_item["description"],
                    min_value=0,
                    max_value=1,
                    label=float_item["label"],
                )
            for int_item in items["int"]:
                field_elements[int_item["label"]] = django_forms.IntegerField(
                    widget=widgets.NumberInput(attrs={"class": "form-control " + name}),
                    required=False,
                    help_text=int_item["description"],
                    label=int_item["label"],
                )

        super(NetworkTemplateForm, self).__init__(*args, **kwargs)
        self.fields: Dict[str, django_forms.Field] = field_elements


DocMetaDataForm: django_forms.Form = create_doc_meta_form("network")


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
        widget=django_forms.Select(
            attrs={"class": "form-control form-select", "random-en": ""}
        ),
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
        widget=django_forms.Select(
            attrs={"class": "form-control form-select", "random-hvn": ""}
        ),
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
                "class": "form-control form-range slider-progress",
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
                "class": "form-control form-range slider-progress",
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
        self.doc_metadata_form: django_forms.Form = DocMetaDataForm(
            data=self.network.doc_metadata.to_dict()
        )

        super(NetworkForm, self).__init__(*args, data=data, **kwargs)

        if self.is_bound:
            if self.is_valid():
                data: dict = self.cleaned_data
                try:
                    self.network.set_from_dict(self.cleaned_data)
                except Exception as e:
                    self.add_error(None, str(e))

    def update_doc_meta(self, data: QueryDict):
        """Update the game modes doc metadata."""
        self.doc_metadata_form = DocMetaDataForm(data=data)
        if self.doc_metadata_form.is_valid():
            self.network.doc_metadata.update(**self.doc_metadata_form.cleaned_data)
            if settings.DYNAMIC_UPDATES:
                NetworkManager.db.update(self.network)


class NetworkSearchForm(django_forms.Form):
    """A Django form object to represent the filterable components of a :class: `~yawning_titan.game_modes.game_mode.GameMode`."""

    def __init__(self, *args, **kwargs):
        """A Django form object to represent the filterable components of a :class: `~yawning_titan.game_modes.game_mode.GameMode`."""
        field_elements = {}

        networks = NetworkManager.db.all()

        if networks:
            for key, name in {
                "entry_nodes": "entry_nodes",
                "high_value_nodes": "high_value_nodes",
                "nodes": "network_nodes",
            }.items():
                selector = {
                    "min": min([len(getattr(n, key)) for n in networks]),
                    "max": max([len(getattr(n, key)) for n in networks]),
                }
                if selector["min"] != selector["max"]:
                    field_elements[f"{name}_min"] = django_forms.FloatField(
                        widget=RangeInput(
                            attrs={"class": f"{name} multi-range-placeholder integer"}
                        ),
                        required=False,
                        min_value=selector["min"],
                        max_value=selector["max"],
                        initial=selector["min"],
                        label=name,
                        help_text=f"Select networks based upon the number of {name} being within a given range.",
                    )
                    field_elements[f"{name}_max"] = django_forms.FloatField(
                        widget=django_forms.HiddenInput(),
                        required=False,
                        min_value=selector["min"],
                        max_value=selector["max"],
                        initial=selector["max"],
                        label=name,
                        help_text="",
                    )
        super(NetworkSearchForm, self).__init__(*args, **kwargs)
        # created dropdowns from grouped elements
        self.fields: Dict[str, django_forms.Field] = field_elements

    @property
    def filters(self):
        """Generate a dictionary of ranges or values that a game mode must have to be a valid query result."""
        filters = {
            n: self.cleaned_data[n] for n in self.changed_data if n != "elements"
        }
        cleaned_filters = {}
        for k, v in filters.items():
            if k.endswith(("_min", "_max")):
                name = k.rstrip("_min").rstrip("_max")
                cleaned_filters[name] = {
                    "min": self.cleaned_data[f"{name}_min"],
                    "max": self.cleaned_data[f"{name}_max"],
                }
            else:
                cleaned_filters[k] = v
        return cleaned_filters


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
        if form.is_valid() and settings.DYNAMIC_UPDATES:
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
        form.network.add_nodes_from_dict(remove_existing=True, nodes_dict=data["nodes"])
        form.network.add_edges_from_dict(remove_existing=True, edges_dict=data["edges"])
        if settings.DYNAMIC_UPDATES:
            NetworkManager.db.update(form.network)  # update the network in the database
        return form
