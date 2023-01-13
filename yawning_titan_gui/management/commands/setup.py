import shutil
from pathlib import Path

from django.core.management.base import BaseCommand

from yawning_titan import _YT_ROOT_DIR


class Command(BaseCommand):
    """
    Command for setting up directories necessary for yawning titan operation with front end.

    Examples:
        >>> python manage.py setup
    """

    help = "Copy yawning_titan gui dependencies to `DATA_DIR`"

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        print("Running setup...")

        from yawning_titan import DATA_DIR, GAME_MODES_DIR
        from yawning_titan_gui import _YT_GUI_ROOT_DIR, DEFAULT_GAME_MODE

        # Creates the static ui files copy in the data directory
        shutil.copytree(
            (_YT_GUI_ROOT_DIR / "static").as_posix(),
            DATA_DIR.as_posix(),
            dirs_exist_ok=True,
        )
        shutil.copyfile(
            (
                _YT_ROOT_DIR / "config/_package_data/game_modes" / DEFAULT_GAME_MODE
            ).as_posix(),
            (GAME_MODES_DIR / Path(DEFAULT_GAME_MODE).name).as_posix(),
        )
