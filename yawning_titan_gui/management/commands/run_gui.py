import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Command to run the yawning titan gui in a window.

    :Examples:

    >>> python manage.py run_gui
    """

    help = "Run yawning titan gui in window."

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        from flaskwebgui import FlaskUI

        from yawning_titan_server.wsgi import application as app

        # Creates the static ui files copy in the data directory
        call_command("setup")

        print(f"running app with {sys.executable}")
        FlaskUI(app=app, server="django").run()
