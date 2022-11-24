import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Command to run the yawning titan gui in a window.

    Usage:
    python manage.py run_gui
    """

    help = "sets up yawning titan dependencies"

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        from flaskwebgui import FlaskUI

        from yawning_titan_server.wsgi import application as app

        print(f"running app with {sys.executable}")
        FlaskUI(app=app, server="django").run()
