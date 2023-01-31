"""The :mod:`~yawning_titan.db.query` module provides a Yawning-Titan extension to :class:`tinydb.queries.Query`."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tinydb import Query
from tinydb.queries import QueryInstance

if TYPE_CHECKING:
    from yawning_titan.networks.network import Network


class CompatibilityQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, These functions
    are specific to the compatibility of :class: `~yawning_titan.game_modes.game_mode.GameMode`
    and :class: `~yawning_titan.networks.network.Network` objects.
    """

    def works_with(self, n: int, include_null: Optional[bool] = True) -> QueryInstance:
        """Tests the game mode can work with a network with the parameter with a value of ``n``.

        Fields whose value is either unrestricted or where ``n`` is in the specified range are returned in the search.

        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.ENTRY_NODES.works_with(18)))

        :param n: The target value of a field as an int.
        :param include_null: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """

        def test_works_with(val, n, include_null):
            return check_element(val, n, include_null)

        return self.test(test_works_with, n, include_null)

    def compatible_with(self, n, include_null: Optional[bool] = True) -> QueryInstance:
        """Tests the game mode can work with a specified network ``n``.

        Fields where all network parameter restrictions are satisfied or unrestricted are returned in the search.


        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.GAME_MODE.compatible_with(network)))

        :param n: The target value of a field as a Network.
        :param include_null: Whether to include fields where part of the range is unbounded.
        :return: ``True`` if it does exist, otherwise ``False``.
        """

        def test_compatible_with(val: dict, n: Network, include_null):
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
                else n.entry_nodes.random_placement.count,
                "high_value_node_count": len(n.high_value_nodes.nodes)
                if n.high_value_nodes.nodes
                else n.high_value_nodes.random_placement.count,
                "node_count": len(n.matrix),
            }
            results = [
                check_element(e, mapper[k], include_null) for k, e in val.items()
            ]
            return all(results)

        return self.test(test_compatible_with, n, include_null)


class YawningTitanQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, rather than
    forcing the user to build a function/lambda function each time and pass it to test.
    """

    def __init__(self):
        super(YawningTitanQuery, self).__init__()

    def len_eq(self, i: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length matches ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_eq(18)))

        :param i: The target length of a field as an int.
        :return: ``True`` if the field length matches ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_eq` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i):
            try:
                return len(val) == i
            except TypeError:
                return False

        return self.test(test_len, i)

    def len_lt(self, i: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length is less than ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_lt(18)))

        :param i: The target length of a field as an int.
        :return: ``True`` if the field length is less than ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i):
            try:
                return len(val) < i
            except TypeError:
                return False

        return self.test(test_len, i)

    def len_le(self, i: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length is less than or equal to ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_le(18)))

        :param i: The target length of a field as an int.
        :return: ``True`` if the field length is less than or equal to ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i):
            try:
                return len(val) <= i
            except TypeError:
                return False

        return self.test(test_len, i)

    def len_gt(self, i: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length is greater than ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_gt(18)))

        :param i: The target length of a field as an int.
        :return: ``True`` if the field length is greater than ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i):
            try:
                return len(val) > i
            except TypeError:
                return False

        return self.test(test_len, i)

    def len_ge(self, i: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length is greater than or equal to ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_ge(18)))

        :param i: The target length of a field as an int.
        :return: ``True`` if it does exist, otherwise ``False``. if the field length is greater than or equal to ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i):
            try:
                return len(val) >= i
            except TypeError:
                return False

        return self.test(test_len, i)


def check_element(el_dict, n, include_null):
    """Check that a restrict-able element is suitable for a given value.

    I.e the value lies in a given range.

    :param el_dict: The dictionary representing of a ConfigGroup related to a range restricted element
    :param n: The target value of a field as a Network.
    :param include_null: Whether to include fields where part of the range is unbounded.

    :return: A boolean representing of the element is suited for a particular value.
    """
    if not isinstance(el_dict, dict) or not all(
        k in el_dict for k in ["min", "max", "restrict"]
    ):
        return False

    if not el_dict["restrict"]:
        return True

    check_min = False
    if el_dict["min"] is None and include_null:
        check_min = True
    elif n > el_dict["min"]:
        check_min = True

    check_max = False
    if el_dict["max"] is None and include_null:
        check_max = True
    elif n < el_dict["max"]:
        check_max = True

    return check_min and check_max
