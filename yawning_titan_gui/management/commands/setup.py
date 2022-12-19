import shutil

from django.core.management.base import BaseCommand

from yawning_titan import _YT_ROOT_DIR


class Command(BaseCommand):
    """
    Command for setting up directories necessary for yawning titan operation with front end.

    :Example:

    >>> python manage.py setup
    """

    help = "Copy yawning_titan gui dependencies to `DATA_DIR`"

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        print("Running setup...")

        from yawning_titan import GAME_MODES_DIR
        from yawning_titan_gui import _YT_GUI_ROOT_DIR, STATIC_DIR

        # Creates the static ui files copy in the data directory
        shutil.copytree(
            (_YT_GUI_ROOT_DIR / "static").as_posix(),
            STATIC_DIR.as_posix(),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            (_YT_ROOT_DIR / "config/_package_data/game_modes").as_posix(),
            GAME_MODES_DIR.as_posix(),
            dirs_exist_ok=True,
        )
