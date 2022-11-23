import shutil

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Command for setting up directories necessary for yawning titan operation with front end.

    Usage:
    python manage.py setup
    """

    help = "sets up yawning titan dependencies"

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        print("Running setup...")
        from yawning_titan import DATA_DIR
        from yawning_titan_gui import _YT_GUI_ROOT_DIR

        print(_YT_GUI_ROOT_DIR / "static", DATA_DIR)

        # Creates the static ui files copy in the data directory
        shutil.copytree(
            (_YT_GUI_ROOT_DIR / "static").as_posix(),
            DATA_DIR.as_posix(),
            dirs_exist_ok=True,
        )
