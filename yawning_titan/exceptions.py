"""Custom Yawning-Titan exceptions."""


class YawningTitanDBError(ValueError):
    """
    Raised during insert fails by :class:`~yawning_titan.db.yawning_titan_db.YawningTitanDB`.

    Should be handled and dealt with without exiting.
    """

    pass


class YawningTitanDBCriticalError(ValueError):
    """
    Raised during update and remove fails by :class:`~yawning_titan.db.yawning_titan_db.YawningTitanDB`.

    Would suggest the DB is corrupted. Should be handled to ensure a 'graceful' exit.
    """

    pass
