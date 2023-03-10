"""Provides a patch to the YawningTitanDB."""
import tempfile

from tinydb import TinyDB

from tests import TEST_PACKAGE_DATA_PATH


def yawning_titan_db_init_patch(self, name: str):
    """
    Patch the :func:`yawning_titan.db.yawning_titan_db.YawningTitanDB.__init__`.

    So that TinyDB testing can be done in isolation, the main init method is patched so that
    a temporary .json file used to create the TinyDB db file using :py:func:`tempfile.TemporaryFile`.

    Self and name params only present so that subclasses of
    :class:`~yawning_titan.db.yawning_titan_db.YawningTitanDB` don't break when instantiating
    the patched class.
    """
    self._name: str = name
    self._path = tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=True).name

    self._db = TinyDB(self._path)

    def _close_and_delete_temp_db():
        self._db.close()

    self.close_and_delete_temp_db = _close_and_delete_temp_db


def yawning_titan_db_test_defaults_patch(self, name: str):
    """Patch the YawningTitanDB so point to the tests/_package_data directory."""
    self._name: str = name
    self._path = TEST_PACKAGE_DATA_PATH / f"{self._name}.json"

    self._db = TinyDB(self._path)
