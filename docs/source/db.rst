Yawning-Titan DB
================

YAWNING-TITAN (**YT**) comes packages with a lightweight document database (See: `TinyDB <https://tinydb.readthedocs.io/en/latest/>`_).


The YawningTitanDB class
************************

An abstract base class, :class:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB`, exists that
provides abstract :func:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.__init__`,
:func:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.insert`,
:func:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.all`,
:func:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.get`, and
:func:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.search` methods. All abstract methods provides have
some default logic that calls their :class:`~tinydb.database.TinyDB` counterpart. Methods have been defined as
abstract methods to force sub-classes of :class:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB` to
implement them. If functionality does not change, the implementations of the abstract methods can simple
call ``super()`` to trigger the default logic.

When :func:`YawningTitanDB.__init__ <yawning_titan.db.yawning_titan_db_abc.YawningTitanDB.__init__>` is called,
the ``name`` passed to it is used to generate a filepath using :attr:`yawning_titan.DB_DIR`. For example, calling
``YawningTitanDB("demo")`` would generate a :class:`~tinydb.database.TinyDB` db `.json` file at:

- **Linux** - `~/.local/share/yawning_titan/db/demo.json`
- **Windows** - `~/AppData/yawning_titan/yawning_titan/db/demo.json`
- **MacOs** - `~/Library/Application Support/yawning_titan/db/demo.json`

The YawningTitanQuery class
***************************

The :class:`~yawning_titan.db.query.YawningTitanQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~yawning_titan.db.query.YawningTitanQuery.len_eq`, :func:`~yawning_titan.db.query.YawningTitanQuery.len_gt`,
:func:`~yawning_titan.db.query.YawningTitanQuery.len_ge`, :func:`~yawning_titan.db.query.YawningTitanQuery.len_lt`,
and :func:`~yawning_titan.db.query.YawningTitanQuery.len_le` functions to test the length of a field.

The NetworkDB and NetworkSchema classes
***************************************

The :class:`~yawning_titan.db.network.NetworkDB` class, used for inserting, querying, updating, and deleting
instances of :class:`~yawning_titan.config.network_config.NetworkConfig`, extends
:class:`~yawning_titan.db.yawning_titan_db_abc.YawningTitanDB`. It implements the required
:func:`~yawning_titan.db.network.NetworkDB.__init__`,
:func:`~yawning_titan.db.network.NetworkDB.insert`,
:func:`~yawning_titan.db.network.NetworkDB.all`,
:func:`~yawning_titan.db.network.NetworkDB.get`, and
:func:`~yawning_titan.db.network.NetworkDB.search` methods, with the return types overridden to return
:class:`~yawning_titan.config.network_config.network_config.NetworkConfig`.
The :class:`~yawning_titan.db.network.NetworkDB` class is writes to a `network.json` file at:

- **Linux** - `~/.local/share/yawning_titan/db/network.json`
- **Windows** - `~/AppData/yawning_titan/yawning_titan/db/network.json`
- **MacOs** - `~/Library/Application Support/yawning_titan/db/network.json`


First, we must instantiate the :class:`~yawning_titan.db.network.NetworkDB` with:

.. code:: python

    from yawning_titan.db.network import NetworkDB
    db = NetworkDB()

Next, we have the option to query the db with either the standard :class:`tinydb.queries.Query` class, the extended
:class:`~yawning_titan.db.query.YawningTitanQuery` class, or by using the network config specific
:class:`~yawning_titan.db.network.NetworkSchema` class. Here we will use :class:`~yawning_titan.db.network.NetworkSchema`.
The :class:`~yawning_titan.db.network.NetworkSchema` class has an attribute mapped to each attribute of
:class:`~yawning_titan.config.network_config.NetworkConfig` as an instance of :class:`~yawning_titan.db.query.YawningTitanQuery`.
This gives direct access to the specific field within the :class:`~tinydb.database.TinyDB` db file.

The following code blocks demonstrate how to use combinations of the :class:`~yawning_titan.db.network.NetworkSchema`
class to build a :class:`~tinydb.queries.Query` chain to query the :class:`~yawning_titan.db.network.NetworkDB`.

**Search for all network configs that have "1" as an entry node:**

.. code:: python

    results = db.search(NetworkSchema.ENTRY_NODES.all(["1"]))

**Search for all network configs that have "1" as both an entry node and a high value node:**

.. code:: python

    results = db.search(
        NetworkSchema.ENTRY_NODES.all(["1"]))
        and (NetworkSchema.HIGH_VALUE_NODES.all(["1"])
    )

**Search for all network configs that have at least 3 high value nodes**

.. code:: python

    results = db.search(NetworkSchema.ENTRY_NODES.len_ge(3))
