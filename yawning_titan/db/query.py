"""The :mod:`~yawning_titan.db.query` module provides a Yawning-Titan extension to :class:`tinydb.queries.Query`."""
from typing import Optional

from tinydb import Query
from tinydb.queries import QueryInstance


class YawningTitanQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, rather that
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

    def compatible_with(
        self, n: int, include_null: Optional[bool] = True
    ) -> QueryInstance:
        """Tests the value of a field is greater than the value ``i``.

        Fields whose value is greater than or equal to ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.game_modes.game_mode_db import GameModeDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = GameModeDB()
        >>> db.search(YawningTitanQuery.ENTRY_NODE_COUNT.ge(18)))

        :param i: The target value of a field as an int.
        :return: ``True`` if it does exist, otherwise ``False``. if the field length is greater than or equal to ``i``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt` is called on
            does not have a :func:`len` function.
        """

        def test_compatible_with(val, n, include_null):
            if not isinstance(val,dict) or not all(k in val for k in ["min","max","restrict"]):
                return False

            if not val["restrict"]:
                return True

            check_min = False
            if val["min"] is None and include_null:
                check_min = True
            elif n > val["min"]:
                check_min = True

            check_max = False
            if val["max"] is None and include_null:
                check_max = True
            elif n < val["max"]:
                check_max = True

            return check_min and check_max

        return self.test(test_compatible_with, n, include_null)

# TEST NETWORK COMPATIBILITY NESTED DICT

# ALLOW n parameter to either be a number or network
