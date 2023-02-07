from typing import Optional, Union

from tinydb import Query
from tinydb.queries import QueryInstance

from yawning_titan.networks.network import Network


def check_element(el_dict: dict, n: int, include_unbounded: bool):
    """Check that a restrict-able element is suitable for a given value.

    I.e the value lies in a given range.

    :param el_dict: The dictionary representing of a ConfigGroup related to a range restricted element
    :param n: The target value of a field as a Network.
    :param include_unbounded: Whether to include fields where part of the range is unbounded.

    :return: A boolean representing of the element is suited for a particular value.
    """
    n = 0 if not n else n
    if (
        n < 0
        or not isinstance(el_dict, dict)
        or not all(k in el_dict for k in ["min", "max", "restrict"])
    ):
        return False

    if not el_dict["restrict"]:
        return True

    check_min = False
    if el_dict["min"] is None:
        if include_unbounded:
            check_min = True
    elif n > el_dict["min"]:
        check_min = True

    check_max = False
    if el_dict["max"] is None:
        if include_unbounded:
            check_max = True
    elif n < el_dict["max"]:
        check_max = True

    return check_min and check_max


class EntryNodeCompatibilityQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, These functions
    are specific to the compatibility of :class: `~yawning_titan.game_modes.game_mode.GameMode`
    and :class: `~yawning_titan.networks.network.Network` objects.
    """

    def works_with(
        self, n: Union[int, Network], include_unbounded: Optional[bool] = False
    ) -> QueryInstance:
        """Tests the game mode can work with a network with the parameter with a value of ``n``.

        Fields whose value is either unrestricted or where ``n`` is in the specified range are returned in the search.

        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.ENTRY_NODES.works_with(18)))

        :param n: The target value of a field as an int or an instance of :class: `~yawning_titan.networks.network.Network`.
        :param include_unbounded: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """
        if isinstance(n, Network):
            n = (
                len(n.entry_nodes.nodes)
                if n.entry_nodes.nodes
                else n.entry_nodes.random_placement.count.value
            )

        def test_works_with(val, n, include_unbounded):
            return check_element(val, n, include_unbounded)

        return self.test(test_works_with, n, include_unbounded)


class HighValueNodeCompatibilityQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, These functions
    are specific to the compatibility of :class: `~yawning_titan.game_modes.game_mode.GameMode`
    and :class: `~yawning_titan.networks.network.Network` objects.
    """

    def works_with(
        self, n: Union[int, Network], include_unbounded: Optional[bool] = False
    ) -> QueryInstance:
        """Tests the game mode can work with a network with the parameter with a value of ``n``.

        Fields whose value is either unrestricted or where ``n`` is in the specified range are returned in the search.

        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.HIGH_VALUE_NODES.works_with(18)))

        :param n: The target value of a field as an int or an instance of :class: `~yawning_titan.networks.network.Network`.
        :param include_unbounded: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """
        if isinstance(n, Network):
            n = (
                len(n.high_value_nodes.nodes)
                if n.high_value_nodes.nodes
                else n.high_value_nodes.random_placement.count.value
            )

        def test_works_with(val, n, include_unbounded):
            return check_element(val, n, include_unbounded)

        return self.test(test_works_with, n, include_unbounded)


class NetworkNodeCompatibilityQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, These functions
    are specific to the compatibility of :class: `~yawning_titan.game_modes.game_mode.GameMode`
    and :class: `~yawning_titan.networks.network.Network` objects.
    """

    def works_with(
        self, n: Union[int, Network], include_unbounded: Optional[bool] = False
    ) -> QueryInstance:
        """Tests the game mode can work with a network with the parameter with a value of ``n``.

        Fields whose value is either unrestricted or where ``n`` is in the specified range are returned in the search.

        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.HIGH_VALUE_NODES.works_with(18)))

        :param n: The target value of a field as an int or an instance of :class: `~yawning_titan.networks.network.Network`.
        :param include_unbounded: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """
        if isinstance(n, Network):
            n = len(n.matrix)

        def test_works_with(val, n, include_unbounded):
            return check_element(val, n, include_unbounded)

        return self.test(test_works_with, n, include_unbounded)


class NetworkCompatibilityQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, These functions
    are specific to the compatibility of :class: `~yawning_titan.game_modes.game_mode.GameMode`
    and :class: `~yawning_titan.networks.network.Network` objects.
    """

    def compatible_with(
        self, n, include_unbounded: Optional[bool] = True
    ) -> QueryInstance:
        """Tests the game mode can work with a specified network ``n``.

        Fields where all network parameter restrictions are satisfied or unrestricted are returned in the search.


        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.GAME_MODE.compatible_with(network)))

        :param n: The target value of a field as an instance of :class: `~yawning_titan.networks.network.Network`.
        :param include_unbounded: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """

        def test_compatible_with(val: dict, n: Network, include_unbounded):
            if (
                not isinstance(val, dict)
                or not isinstance(n, Network)
                or not all(
                    k in val
                    for k in ["entry_node_count", "high_value_node_count", "node_count"]
                )
            ):
                return False
            mapper = {
                "entry_node_count": len(n.entry_nodes.nodes)
                if n.entry_nodes.nodes
                else n.entry_nodes.random_placement.count.value,
                "high_value_node_count": len(n.high_value_nodes.nodes)
                if n.high_value_nodes.nodes
                else n.high_value_nodes.random_placement.count.value,
                "node_count": len(n.matrix),
            }
            results = [
                check_element(e, mapper[k], include_unbounded) for k, e in val.items()
            ]
            return all(results)

        return self.test(test_compatible_with, n, include_unbounded)
