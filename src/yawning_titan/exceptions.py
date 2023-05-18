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


class ConfigItemValidationError(ValueError):
    """A config value has failed validation against a given ``ItemTypeProperties``."""

    pass


class ConfigGroupValidationError(ValueError):
    """A config group has failed validation."""

    pass


class YawningTitanRunError(ValueError):
    """An error has occurred during the instantiation of the YawningTitanRun class."""

    pass


class NetworkError(ValueError):
    """An error has occurred in the construction to the Network."""
