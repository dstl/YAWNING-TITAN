"""The :mod:`~yawning_titan.db.query` module provides a Yawning-Titan extension to :class:`tinydb.queries.Query`."""
from __future__ import annotations

from tinydb import Query
from tinydb.queries import QueryInstance


class YawningTitanQuery(Query):
    """
    The :class:`~yawning_titan.db.query.YawningTitanQuery` class extends :class:`tinydb.queries.Query`.

    Extended to provide common pre-defined test functions that call :func:`tinydb.queries.Query.test`, rather than
    forcing the user to build a function/lambda function each time and pass it to test.
    """

    def __init__(self):
        super().__init__()

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

    def len_bt(self, i: int, j: int) -> QueryInstance:
        """Tests the length of a field. This could be the length of a string or an array field.

        Fields whose length is greater than or equal to ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_bt(1,18)))

        :param i: The minimum length of a field as an int.
        :param j: The maximum length of a field as an int.
        :return: ``True`` if it does exist, otherwise ``False``. if the field length is greater than or equal to ``i``
            and less than or equal to ``j``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_bt` is called on
            does not have a :func:`len` function.
        """

        def test_len(val, i, j):
            try:
                return len(val) >= i and len(val) <= j
            except TypeError:
                return False

        return self.test(test_len, i, j)

    def bt(self, i: int, j: int) -> QueryInstance:
        """Tests the value of a field. This could be the value of a string or an array field.

        Fields whose value is greater than or equal to ``i`` are returned in the search.

        :Example:

        >>> from yawning_titan.networks.network_db import NetworkDB
        >>> from yawning_titan.db.query import YawningTitanQuery
        >>> db = NetworkDB()
        >>> db.search(YawningTitanQuery.matrix.len_bt(1,18)))

        :param i: The minimum value of a field as an int.
        :param j: The maximum value of a field as an int.
        :return: ``True`` if it does exist, otherwise ``False``. if the field value is greater than or equal to ``i``
            and less than or equal to ``j``, otherwise ``False``.
        :raises TypeError: When the field :func:`~yawning_titan.db.query.YawningTitanQuery.len_bt` is called on
            does not have a :func:`len` function.
        """

        def test_val(val, i, j):
            try:
                return val >= i and val <= j
            except TypeError:
                return False

        return self.test(test_val, i, j)
