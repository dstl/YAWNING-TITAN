"""Provides a patch to the YawningTitanDB."""
import os
import tempfile
from typing import Final

from tinydb import TinyDB


def yawning_titan_db_init_patch(self, name: str):
    """
    Patch the :func:`yawning_titan.db.yawning_titan_db.YawningTitanDB.__init__`.

    So that TinyDB testing can be done in isolation, the main init method is patched so that
    a temporary .json file used to create the TinyDB db file using :py:func:`tempfile.TemporaryFile`.

    Self and name params only present so that subclasses of
    :class:`~yawning_titan.db.yawning_titan_db.YawningTitanDB` don't break when instantiating
    the patched class.
    """
    self._name: Final[str] = name
    self._temp_file = tempfile.TemporaryFile(suffix=".json", mode="w", delete=True).name
    self._path = str(self._temp_file)

    self._db = TinyDB(self._path)

    def _close_and_delete_temp_db():
        self._db.close()
        os.unlink(self._temp_file)

    self.close_and_delete_temp_db = _close_and_delete_temp_db
